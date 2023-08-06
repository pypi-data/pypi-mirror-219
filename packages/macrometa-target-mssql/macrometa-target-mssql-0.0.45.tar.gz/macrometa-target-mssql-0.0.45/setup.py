# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['macrometa_target_mssql']

package_data = \
{'': ['*']}

install_requires = \
['c8connector>=0.0.29',
 'inflection==0.3.1',
 'joblib==1.2.0',
 'pipelinewise-singer-python==1.2.0',
 'prometheus-client==0.16.0',
 'pymssql>=2.2.5',
 'sqlalchemy>=1.4,<2.0']

entry_points = \
{'console_scripts': ['macrometa-target-mssql = macrometa_target_mssql:main']}

setup_kwargs = {
    'name': 'macrometa-target-mssql',
    'version': '0.0.45',
    'description': 'Macrometa target connector for writing data into Microsoft SQL Server.',
    'long_description': 'None',
    'author': 'Macrometa',
    'author_email': 'info@macrometa.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
