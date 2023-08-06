# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonblocking_logging',
 'nonblocking_logging.handlers',
 'nonblocking_logging.integrations',
 'nonblocking_logging.integrations.django',
 'nonblocking_logging.integrations.django.handlers']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'nonblocking-logging',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Ersain Dinmukhamed',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
