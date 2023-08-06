# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentiml']

package_data = \
{'': ['*']}

install_requires = \
['weaver-json>=0.0.2']

setup_kwargs = {
    'name': 'sentiml',
    'version': '0.0.1',
    'description': 'Sentinel for ML Models',
    'long_description': '# Installation\n\nUpdate your pypoetry to point towards the currently non-versioned Weaver repo.',
    'author': 'Lissa Hyacinth',
    'author_email': 'lissa@shareableai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
