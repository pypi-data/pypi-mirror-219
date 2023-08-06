# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cgepy', 'cgepy.ext', 'cgepy.ext.beta']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cgepy',
    'version': '0.7.2',
    'description': 'Tools for developing graphical programs inside the console.',
    'long_description': "### cgepy // 0.7.2\n##### A lightweight 8-bit graphics engine\n***\n###### Documentation: https://cgepy.github.io/docs\nLooking for something simple to use? Want to use a reliable package for once?\\\ncgepy's got you covered.\n\nFeaturing a powerful, but easy-to-use system, you can make fun games with cgepy.\\\nThough cgepy lacks many things like mouse support and native keyboard support, it is ever growing and will soon have so many features in place of those, while maintaining that same speed and reliablility.\n",
    'author': 'catbox305',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
