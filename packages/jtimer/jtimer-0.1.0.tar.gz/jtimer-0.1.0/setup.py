# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jtimer', 'jtimer.controller', 'jtimer.dao', 'jtimer.model', 'jtimer.view']

package_data = \
{'': ['*']}

modules = \
['schema']
install_requires = \
['PyQt6>=6.5.1,<7.0.0']

setup_kwargs = {
    'name': 'jtimer',
    'version': '0.1.0',
    'description': "John's Timer - desktop app for tracking time",
    'long_description': '# Timer App\n\nThis app \n\n## General usage\n\n## Feature Roadmap\n* github workflow\n* store timer data\n* stats view\n* on-exit behaviour\n* timer and relation\n* timer mutual exclusion\n',
    'author': 'John Watson',
    'author_email': 'jmwdev@pm.me',
    'maintainer': 'John Watson',
    'maintainer_email': 'jmwdev@pm.me',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10.6,<4.0.0',
}


setup(**setup_kwargs)
