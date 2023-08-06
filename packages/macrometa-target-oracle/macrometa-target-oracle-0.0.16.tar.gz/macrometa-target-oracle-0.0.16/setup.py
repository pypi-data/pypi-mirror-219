# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['macrometa_target_oracle']

package_data = \
{'': ['*']}

install_requires = \
['c8connector>=0.0.29',
 'inflection==0.3.1',
 'joblib==1.2.0',
 'oracledb>=1.2.2,<2.0.0',
 'pipelinewise-singer-python==1.2.0',
 'prometheus-client==0.16.0',
 'sqlalchemy>=1.4,<2.0']

entry_points = \
{'console_scripts': ['macrometa-target-oracle = macrometa_target_oracle:main']}

setup_kwargs = {
    'name': 'macrometa-target-oracle',
    'version': '0.0.16',
    'description': 'Macrometa target connector for writing data into Oracle DB.',
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
