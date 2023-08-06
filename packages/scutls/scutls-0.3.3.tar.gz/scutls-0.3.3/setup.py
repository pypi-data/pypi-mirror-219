# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scutls']

package_data = \
{'': ['*'], 'scutls': ['assets/*']}

install_requires = \
['GEOparse>=2.0.3,<3.0.0',
 'biopython>=1.80,<2.0',
 'bs4>=0.0.1,<0.0.2',
 'importlib-resources>=5.8.0,<6.0.0',
 'pysam>=0.21.0,<0.22.0',
 'regex>=2023.5.5,<2024.0.0',
 'urllib3>=1.26.10,<2.0.0',
 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['scutls = scutls.arguments:main']}

setup_kwargs = {
    'name': 'scutls',
    'version': '0.3.3',
    'description': 'Single-cell data processing utility tools',
    'long_description': 'None',
    'author': 'Kai Hu',
    'author_email': 'kai.hu@umassmed.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
