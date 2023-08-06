# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloud_api_signer']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.2']

setup_kwargs = {
    'name': 'cloud-api-signer',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Huang Shaoyan',
    'author_email': 'huangshaoyan1982@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.8,<4.0.0',
}


setup(**setup_kwargs)
