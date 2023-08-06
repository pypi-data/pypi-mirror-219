# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smits']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'smits',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'hukai916',
    'author_email': '31452631+hukai916@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
