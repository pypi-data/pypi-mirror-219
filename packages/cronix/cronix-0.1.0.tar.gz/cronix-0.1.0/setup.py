# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cronix']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cronix',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Sean Collings',
    'author_email': 'seanrcollings@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
