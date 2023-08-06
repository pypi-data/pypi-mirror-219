import json
import sys
import pymssql
import inflection
import re
import itertools
import sqlalchemy
import time

from collections.abc import MutableMapping
from singer import get_logger
from typing import cast, Dict, List, Optional


# pylint: disable=missing-function-docstring,missing-class-docstring
def validate_config(config):
    errors = []
    required_config_keys = [
        'host',
        'port',
        'user',
        'password',
        'database',
        'target_schema',
        'target_table',
    ]

    # Check if mandatory keys exist
    for k in required_config_keys:
        if not config.get(k, None):
            errors.append("Required key is missing from config: [{}]".format(k))

    # Check target schema config
    config_default_target_schema = config.get('target_schema', None)
    config_schema_mapping = config.get('schema_mapping', None)
    if not config_default_target_schema and not config_schema_mapping:
        errors.append("Neither 'target_schema' (string) nor 'schema_mapping' (object) keys set in config.")

    return errors


def safe_column_name(name):
    return '"{}"'.format(name).lower()


def flatten_key(k, parent_key, sep):
    full_key = parent_key + [k]
    inflected_key = full_key.copy()
    reducer_index = 0
    while len(sep.join(inflected_key)) >= 63 and reducer_index < len(inflected_key):
        reduced_key = re.sub(r'[a-z]', '', inflection.camelize(inflected_key[reducer_index]))
        inflected_key[reducer_index] = \
            (reduced_key if len(reduced_key) > 1 else inflected_key[reducer_index][0:3]).lower()
        reducer_index += 1

    return sep.join(inflected_key)


# pylint: disable=dangerous-default-value,invalid-name
def flatten_schema(d, parent_key=[], sep='__', level=0, max_level=0):
    items = []

    if 'properties' not in d:
        return {}

    for k, v in d['properties'].items():
        new_key = flatten_key(k, parent_key, sep)
        if 'type' in v.keys():
            if 'object' in v['type'] and 'properties' in v and level < max_level:
                items.extend(flatten_schema(v, parent_key + [k], sep=sep, level=level + 1, max_level=max_level).items())
            else:
                items.append((new_key, v))
        else:
            if len(v.values()) > 0:
                if list(v.values())[0][0]['type'] == 'string':
                    list(v.values())[0][0]['type'] = ['null', 'string']
                    items.append((new_key, list(v.values())[0][0]))
                elif list(v.values())[0][0]['type'] == 'array':
                    list(v.values())[0][0]['type'] = ['null', 'array']
                    items.append((new_key, list(v.values())[0][0]))
                elif list(v.values())[0][0]['type'] == 'object':
                    list(v.values())[0][0]['type'] = ['null', 'object']
                    items.append((new_key, list(v.values())[0][0]))

    key_func = lambda item: item[0]
    sorted_items = sorted(items, key=key_func)
    for k, g in itertools.groupby(sorted_items, key=key_func):
        if len(list(g)) > 1:
            raise ValueError('Duplicate column name produced in schema: {}'.format(k))

    return dict(sorted_items)


# pylint: disable=redefined-outer-name
def _should_json_dump_value(key, value, flatten_schema=None):
    if isinstance(value, (dict, list)):
        return True

    if flatten_schema and key in flatten_schema and 'type' in flatten_schema[key]\
            and set(flatten_schema[key]['type']) == {'null', 'object', 'array'}:
        return True

    return False


# pylint: disable-msg=too-many-arguments
def flatten_record(d, flatten_schema=None, parent_key=[], sep='__', level=0, max_level=0):
    items = []
    for k, v in d.items():
        new_key = flatten_key(k, parent_key, sep)
        if isinstance(v, MutableMapping) and level < max_level:
            items.extend(flatten_record(v, flatten_schema, parent_key + [k], sep=sep, level=level + 1,
                                        max_level=max_level).items())
        else:
            items.append((new_key, json.dumps(v) if _should_json_dump_value(k, v, flatten_schema) else v))
    return dict(items)


def primary_column_names(stream_schema_message):
    return [safe_column_name(p) for p in stream_schema_message['key_properties']]


def stream_name_to_dict(stream_name, separator='-', table_name=''):
    catalog_name = None
    schema_name = None
    explicit_table_name = not ''.__eq__(table_name)
    table_name = table_name if explicit_table_name else stream_name

    # Schema and table name can be derived from stream if it's in <schema_nama>-<table_name> format
    s = stream_name.split(separator)
    if len(s) == 2:
        schema_name = s[0]
        table_name = table_name if explicit_table_name else s[1]
    if len(s) > 2:
        catalog_name = s[0]
        schema_name = s[1]
        table_name = table_name if explicit_table_name else '_'.join(s[2:])

    return {
        'catalog_name': catalog_name,
        'schema_name': schema_name,
        'table_name': table_name
    }


# pylint: disable=too-many-public-methods,too-many-instance-attributes
class DbSync:
    def __init__(self, connection_config, stream_schema_message=None):
        """
            connection_config:      Mssql connection details

            stream_schema_message:  An instance of the DbSync class is typically used to load
                                    data only from a certain singer tap stream.

                                    The stream_schema_message holds the destination schema
                                    name and the JSON schema that will be used to
                                    validate every RECORDS messages that comes from the stream.
                                    Schema validation happening before creating CSV and before
                                    uploading data into Mssql.

                                    If stream_schema_message is not defined then we can use
                                    the DbSync instance as a generic purpose connection to
                                    Mssql and can run individual queries. For example
                                    collecting catalog information from Mssql for caching
                                    purposes.
        """
        self.connection_config = connection_config
        self.stream_schema_message = stream_schema_message

        # logger to be used across the class's methods
        self.logger = get_logger('macrometa_target_mssql')

        # Validate connection configuration
        config_errors = validate_config(connection_config)

        # Exit if config has errors
        if len(config_errors) > 0:
            error_msg = "Invalid configuration:\n   * {}".format('\n   * '.join(config_errors))
            self.logger.error(error_msg)
            raise Exception(error_msg)

        self.schema_name = None
        self.grantees = None

        # Init stream schema
        if stream_schema_message is not None:
            # Define initial list of indices to created
            self.hard_delete = self.connection_config.get('hard_delete', False)
            if self.hard_delete:
                self.indices = ['_sdc_deleted_at']
            else:
                self.indices = []

            #  Define target schema name.
            #  --------------------------
            #  Target schema name can be defined in multiple ways:
            #
            #   1: 'default_target_schema' key  : Target schema is the same for every incoming stream if
            #       not specified explicitly for a given stream in the `schema_mapping` object
            #   2: 'schema_mapping' key : Target schema defined explicitly for a given stream.
            #       Example config.json:
            #           "schema_mapping": {
            #               "my_tap_stream_id": {
            #                   "target_schema": "my_mssql_schema",
            #                   "target_schema_select_permissions": [ "role_with_select_privs" ],
            #                   "indices": ["column_1", "column_2s"]
            #               }
            #           }
            config_default_target_schema = self.connection_config.get('target_schema', '').strip()
            config_schema_mapping = self.connection_config.get('schema_mapping', {})
            config_target_table = self.connection_config.get('target_table', '').strip()

            stream_name = stream_schema_message['stream']
            stream_schema_name = stream_name_to_dict(stream_name, table_name=config_target_table)['schema_name']
            stream_table_name = stream_name_to_dict(stream_name, table_name=config_target_table)['table_name']
            if config_schema_mapping and stream_schema_name in config_schema_mapping:
                self.schema_name = config_schema_mapping[stream_schema_name].get('target_schema')

                # Get indices to create for the target table
                indices = config_schema_mapping[stream_schema_name].get('indices', {})
                if stream_table_name in indices:
                    self.indices.extend(indices.get(stream_table_name, []))

            elif config_default_target_schema:
                self.schema_name = config_default_target_schema

            if not self.schema_name:
                raise Exception("Target schema name not defined in config. Neither 'target_schema' (string)"
                                "nor 'schema_mapping' (object) defines target schema for {} stream."
                                .format(stream_name))

            #  Define grantees
            #  ---------------
            #  Grantees can be defined in multiple ways:
            #
            #   1: 'default_target_schema_select_permissions' key  : USAGE and SELECT privileges will be granted on
            #       every table to a given role for every incoming stream if not specified explicitly in the
            #       `schema_mapping` object
            #   2: 'target_schema_select_permissions' key : Roles to grant USAGE and SELECT privileges defined
            #       explicitly for a given stream.
            #           Example config.json:
            #               "schema_mapping": {
            #                   "my_tap_stream_id": {
            #                       "target_schema": "my_mssql_schema",
            #                       "target_schema_select_permissions": [ "role_with_select_privs" ]
            #                   }
            #               }
            self.grantees = self.connection_config.get('default_target_schema_select_permissions')
            if config_schema_mapping and stream_schema_name in config_schema_mapping:
                self.grantees = config_schema_mapping[stream_schema_name].get('target_schema_select_permissions',
                                                                              self.grantees)

            self.data_flattening_max_level = self.connection_config.get('data_flattening_max_level', 0)
            self.flatten_schema = flatten_schema(stream_schema_message['schema'],
                                                 max_level=self.data_flattening_max_level)

    def open_connection(self):
        args = {
            "user": self.connection_config.get("user"),
            "password": self.connection_config.get("password"),
            "server": self.connection_config["host"],
            "database": self.connection_config.get("database", "master"),
            "charset": self.connection_config.get("characterset", "utf8"),
            "autocommit": True,
            "port": self.connection_config.get("port", "1433"),
            "tds_version": self.connection_config.get("tds_version", "7.3")
        }
        return pymssql.connect(**args)

    def query(self, query, params=None, ignore_rowcount=False):
        self.logger.debug("Running query: %s , params: %s", query, params)
        with self.open_connection() as connection:
            with connection.cursor(as_dict=True) as cur:
                cur.execute(
                    query,
                    params
                )
                if cur.rowcount > 0 or ignore_rowcount:
                    try:
                        return cur.fetchall()
                    except pymssql.OperationalError as e:
                        self.logger.warn(f"Exception raised while fetching from cursor. {e}")
                return []

    def table_name(self, stream_name, is_temporary=False, without_schema=False):
        config_target_table = self.connection_config.get('target_table', '').strip()
        stream_dict = stream_name_to_dict(stream_name, table_name=config_target_table)
        table_name = stream_dict['table_name']
        mssql_table_name = table_name.replace('.', '_').replace('-', '_').lower()

        if is_temporary:
            return f'{self.schema_name}."#{mssql_table_name.lower()}"'

        if without_schema:
            return f'"{mssql_table_name.lower()}"'

        return f'{self.schema_name}."{mssql_table_name.lower()}"'

    def record_primary_key_string(self, record):
        if len(self.stream_schema_message['key_properties']) == 0:
            return None
        flatten = flatten_record(record, self.flatten_schema, max_level=self.data_flattening_max_level)
        try:
            key_props = [str(flatten[p]) for p in self.stream_schema_message['key_properties']]
        except Exception as exc:
            self.logger.info("Cannot find %s primary key(s) in record: %s",
                             self.stream_schema_message['key_properties'],
                             flatten)
            raise exc
        return ','.join(key_props)

    def bulk_insert_records(
        self,
        full_table_name: str,
        schema: dict,
        records,
    ):
        """Bulk insert records to an existing destination table."""

        columns = list(self.flatten_schema.keys())
        self.logger.info(f"Bulk inserting records into table {full_table_name} with columns {columns}.")
        # Create the list of tuples for bulk insert
        values = []
        for record in records.values():
            record_values = []
            for column in columns:
                value = record.get(column)
                # Serialize dictionaries and lists to JSON strings
                if isinstance(value, (dict, list)):
                    value = json.dumps(value)
                record_values.append(value)
            values.append(tuple(record_values))
        return values

    def _jsonschema_type_check(
        self, jsonschema_type: dict, type_check: tuple[str]
    ) -> bool:
        """Return True if the jsonschema_type supports the provided type.
        Args:
            jsonschema_type: The type dict.
            type_check: A tuple of type strings to look for.
        Returns:
            True if the schema suports the type.
        """
        if "type" in jsonschema_type:
            if isinstance(jsonschema_type["type"], (list, tuple)):
                for t in jsonschema_type["type"]:
                    if t in type_check:
                        return True
            else:
                if jsonschema_type.get("type") in type_check:
                    return True

        if any(t in type_check for t in jsonschema_type.get("anyOf", ())):
            return True

        return False

    def _is_string_with_format(self, type_dict):
        if "string" in type_dict.get("type", []) and type_dict.get("format") in {
            "date-time",
            "time",
            "date",
        }:
            return True

    def get_datelike_property_type(self, property_schema: Dict) -> Optional[str]:
        """Return one of 'date-time', 'time', or 'date' if property is date-like.

        Otherwise return None.
        """
        if self._is_string_with_format(property_schema):
            return cast(str, property_schema["format"])
        elif "anyOf" in property_schema:
            for type_dict in property_schema["anyOf"]:
                if self._is_string_with_format(type_dict):
                    return cast(str, type_dict["format"])
        return None

    def to_sql_type(self, jsonschema_type: dict) -> sqlalchemy.types.TypeEngine:  # noqa
        """Convert JSON Schema type to a SQL type.
        Args:
            jsonschema_type: The JSON Schema object.
        Returns:
            The SQL type.
        """
        maxlength = jsonschema_type.get("maxLength")
        if not maxlength:
            maxlength = 8000
        if self._jsonschema_type_check(jsonschema_type, ("string",)):
            datelike_type = self.get_datelike_property_type(jsonschema_type)
            if datelike_type:
                if datelike_type == "date-time":
                    return cast(
                        sqlalchemy.types.TypeEngine, sqlalchemy.types.DATETIME()
                    )
                if datelike_type in "time":
                    return cast(sqlalchemy.types.TypeEngine, sqlalchemy.types.TIME())
                if datelike_type == "date":
                    return cast(sqlalchemy.types.TypeEngine, sqlalchemy.types.DATE())

            if maxlength is not None:
                if maxlength > 8000:
                    return cast(sqlalchemy.types.TypeEngine, sqlalchemy.types.TEXT())

            return cast(
                sqlalchemy.types.TypeEngine, sqlalchemy.types.VARCHAR(maxlength)
            )

        if self._jsonschema_type_check(jsonschema_type, ("integer",)):
            return cast(sqlalchemy.types.TypeEngine, sqlalchemy.types.BIGINT())

        if self._jsonschema_type_check(jsonschema_type, ("number",)):
            return cast(sqlalchemy.types.TypeEngine, sqlalchemy.types.FLOAT())

        if self._jsonschema_type_check(jsonschema_type, ("boolean",)):
            return cast(sqlalchemy.types.TypeEngine, sqlalchemy.types.VARCHAR(5))

        if self._jsonschema_type_check(jsonschema_type, ("object",)):
            return "VARCHAR(MAX)"

        if self._jsonschema_type_check(jsonschema_type, ("array",)):
            return "VARCHAR(MAX)"

        return cast(sqlalchemy.types.TypeEngine, sqlalchemy.types.VARCHAR(maxlength))

    def column_clause(self, name, schema_property):
        return '{} {}'.format(safe_column_name(name), self.to_sql_type(schema_property))

    def create_temp_table_from_table(self, from_table_name, tmp_full_table_name):
        """Temp table from another table."""
        droptable = f"DROP TABLE IF EXISTS {tmp_full_table_name}"

        ddl = f"""
            SELECT TOP 0 *
            into {tmp_full_table_name}
            FROM {from_table_name}
        """  # nosec
        return droptable, ddl

    def process_batch(self, records) -> None:
        """Process a batch with the given batch context.
        Writes a batch to the SQL target. Developers may override this method
        in order to provide a more efficient upload/upsert process.
        Args:
            records: List of records to load into database.
        """

        key_properties = self.stream_schema_message['key_properties']
        join_keys = primary_column_names(self.stream_schema_message)
        schema = self.stream_schema_message['schema']

        stream_schema_message = self.stream_schema_message
        full_table_name = self.table_name(stream_schema_message['stream'], is_temporary=False)
        tmp_table_name = self.table_name(stream_schema_message['stream'], is_temporary=True)

        with self.open_connection() as connection:
            with connection.cursor(as_dict=True) as cur:
                if key_properties:
                    # Create a temp table (Creates from the table above)
                    self.logger.info(f"Creating temp table {tmp_table_name}")
                    droptable, ddl = self.create_temp_table_from_table(
                                            from_table_name=full_table_name,
                                            tmp_full_table_name=tmp_table_name
                                        )
                    cur.execute(droptable)
                    cur.execute(ddl)

                    values = self.bulk_insert_records(
                                                full_table_name=tmp_table_name,
                                                schema=schema,
                                                records=records,
                                            )
                    connection.bulk_copy(tmp_table_name, values)

                    # Merge data from Temp table to main table
                    self.logger.info(f"Bulk insert done. Merging data from temp table to {full_table_name}")
                    merge_sql, droptable = self.merge_upsert_from_table(
                                                from_table_name=tmp_table_name,
                                                to_table_name=full_table_name,
                                                schema=schema,
                                                join_keys=join_keys,
                                            )
                    cur.execute(merge_sql)
                    cur.execute(droptable)
                    self.logger.info("Merge complete.")
                else:
                    values = self.bulk_insert_records(
                                                full_table_name=full_table_name,
                                                schema=schema,
                                                records=records,
                                            )
                    connection.bulk_copy(full_table_name, values)
                    self.logger.info("Bulk insert done.")

    def merge_upsert_from_table(
        self,
        from_table_name: str,
        to_table_name: str,
        schema: dict,
        join_keys: List[str],
    ):
        """Merge upsert data from one table to another.
        Args:
            from_table_name: The source table name.
            to_table_name: The destination table name.
            join_keys: The merge upsert keys, or `None` to append.
            schema: Singer Schema message.
        Return:
            The number of records copied, if detectable, or `None` if the API does not
            report number of records affected/inserted.
        """

        columns = self.column_names()
        join_condition = " and ".join(
            [f"temp.{key} = target.{key}" for key in join_keys]
        )

        update_stmt = ", ".join(
            [
                f"target.{key} = temp.{key}"
                for key in columns
                if key not in join_keys
            ]
        )  # noqa

        merge_sql = f"""
            MERGE INTO {to_table_name} AS target
            USING {from_table_name} AS temp
            ON {join_condition}
            WHEN MATCHED THEN
                UPDATE SET
                    { update_stmt }
            WHEN NOT MATCHED THEN
                INSERT ({", ".join(columns)})
                VALUES ({", ".join([f"temp.{key}" for key in columns])});
        """  # nosec

        droptable = f"DROP TABLE IF EXISTS {from_table_name}"
        return merge_sql, droptable

    def column_names(self):
        return [safe_column_name(name) for name in self.flatten_schema]

    def create_table_query(self, table_name=None, is_temporary=False):
        stream_schema_message = self.stream_schema_message
        columns = [
            self.column_clause(
                name,
                schema
            )
            for (name, schema) in self.flatten_schema.items()
        ]

        primary_key = ["PRIMARY KEY ({})".format(', '.join(primary_column_names(stream_schema_message)))] \
            if len(stream_schema_message['key_properties']) > 0 else []

        if not table_name:
            gen_table_name = self.table_name(stream_schema_message['stream'], is_temporary=is_temporary)

        return 'CREATE TABLE {} ({})'.format(
            table_name if table_name else gen_table_name,
            ', '.join(columns + primary_key)
        )

    def grant_usage_on_schema(self, schema_name, grantee):
        query = "GRANT USAGE ON SCHEMA {} TO GROUP {}".format(schema_name, grantee)
        self.logger.info("Granting USAGE privilege on '%s' schema to '%s'... %s", schema_name, grantee, query)
        self.query(query)

    def grant_select_on_all_tables_in_schema(self, schema_name, grantee):
        query = "GRANT SELECT ON ALL TABLES IN SCHEMA {} TO GROUP {}".format(schema_name, grantee)
        self.logger.info("Granting SELECT ON ALL TABLES privilege on '%s' schema to '%s'... %s",
                         schema_name,
                         grantee,
                         query)
        self.query(query)

    @classmethod
    def grant_privilege(cls, schema, grantees, grant_method):
        if isinstance(grantees, list):
            for grantee in grantees:
                grant_method(schema, grantee)
        elif isinstance(grantees, str):
            grant_method(schema, grantees)

    def create_index(self, stream, column):
        table = self.table_name(stream)
        table_without_schema = self.table_name(stream, without_schema=True)
        index_name = 'i_{}_{}'.format(table_without_schema[:30].replace(' ', '').replace('"', ''),
                                      column.replace(',', '_'))
        query = f"""IF NOT EXISTS (
                SELECT 1
                FROM sys.indexes
                WHERE object_id = OBJECT_ID('{table}')
                    AND name = '{index_name}'
            )
            BEGIN
                CREATE INDEX {index_name} ON {table} ({column});
            END"""
        self.logger.info("Creating index on '%s' table on '%s' column(s)", table, column)
        try:
            self.query(query)
        except Exception as e:
            self.logger.warn(f"Failed to create index, error: {e}")

    def create_indices(self, stream):
        if isinstance(self.indices, list):
            for index in self.indices:
                self.create_index(stream, index)

    def delete_rows(self, stream):
        table = self.table_name(stream)
        query = "DELETE FROM {} WHERE _sdc_deleted_at IS NOT NULL".format(table)
        self.logger.info("Deleting rows from '%s' table... %s", table, query)
        with self.open_connection() as connection:
            with connection.cursor(as_dict=True) as cur:
                cur.execute(query)
        self.logger.info("Delete query completed.")

    def create_schema_if_not_exists(self, table_columns_cache=None):
        schema_name = self.schema_name
        schema_rows = 0

        # table_columns_cache is an optional pre-collected list of available objects in mssql
        if table_columns_cache:
            schema_rows = list(filter(lambda x: x['TABLE_SCHEMA'] == schema_name, table_columns_cache))
        # Query realtime if not pre-collected
        else:
            schema_rows = self.query(
                f"SELECT LOWER(schema_name) schema_name FROM information_schema.schemata WHERE LOWER(schema_name) = '{schema_name.lower()}'",
                ignore_rowcount=True
            )

        if len(schema_rows) == 0:
            query = "CREATE SCHEMA {}".format(schema_name)
            self.logger.info("Schema '%s' does not exist. Creating... %s", schema_name, query)
            self.query(query)

            self.grant_privilege(schema_name, self.grantees, self.grant_usage_on_schema)

    def get_tables(self):
        return self.query(
            f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.schema_name}'",
            ignore_rowcount=True
        )

    def get_table_columns(self, table_name):
        return self.query("""SELECT column_name, data_type
      FROM information_schema.columns
      WHERE lower(table_name) = %s AND lower(table_schema) = %s""", params=(table_name.replace("\"", "").lower(),
                                                                     self.schema_name.lower()),
                                                                     ignore_rowcount=True)

    def update_columns(self):
        stream_schema_message = self.stream_schema_message
        stream = stream_schema_message['stream']
        table_name = self.table_name(stream, without_schema=True)
        columns = self.get_table_columns(table_name)
        columns_dict = {column['column_name'].lower(): column for column in columns}

        columns_to_add = [
            self.column_clause(
                name,
                properties_schema
            )
            for (name, properties_schema) in self.flatten_schema.items()
            if name.lower() not in columns_dict
        ]

        for column in columns_to_add:
            self.add_column(column, stream)

        columns_to_replace = [
            (safe_column_name(name), self.column_clause(
                name,
                properties_schema
            ))
            for (name, properties_schema) in self.flatten_schema.items()
            if name.lower() in columns_dict and
            columns_dict[name.lower()]['data_type'].lower() not in str(self.to_sql_type(properties_schema)).lower()
        ]

        for (column_name, column) in columns_to_replace:
            self.version_column(column_name, stream)
            self.add_column(column, stream)

    def drop_column(self, column_name, stream):
        drop_column = "ALTER TABLE {} DROP COLUMN {}".format(self.table_name(stream), column_name)
        self.logger.info('Dropping column: %s', drop_column)
        self.query(drop_column)

    def version_column(self, column_name, stream):
        version_column = "EXEC sp_rename '{}.{}', '{}_{}', 'COLUMN';".format(self.table_name(stream, False),
                                                                               column_name,
                                                                               column_name.replace("\"", ""),
                                                                               time.strftime("%Y%m%d_%H%M"))
        self.logger.info('Versioning column: %s', version_column)
        self.query(version_column)

    def add_column(self, column, stream):
        add_column = "ALTER TABLE {} ADD COLUMN {}".format(self.table_name(stream), column)
        self.logger.info('Adding column: %s', add_column)
        self.query(add_column)

    def sync_table(self):
        stream_schema_message = self.stream_schema_message
        stream = stream_schema_message['stream']
        table_name = self.table_name(stream, without_schema=True)
        found_tables = [table for table in (self.get_tables()) if f'"{table["table_name"].lower()}"' == table_name]
        if len(found_tables) == 0:
            query = self.create_table_query()
            self.logger.info("Table '%s' does not exist. Creating... %s", table_name, query)
            self.query(query)

            self.grant_privilege(self.schema_name, self.grantees, self.grant_select_on_all_tables_in_schema)
        else:
            self.logger.info("Table '%s' exists", table_name)
            self.update_columns()
