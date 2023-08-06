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
    'version': '0.1.1',
    'description': "John's Timer - desktop app for tracking time",
    'long_description': '# Timer App\n\nDEVELOPMENT IN PROGRESS\n\nDissatisfied with the selection of timer applications available in linux, I built my own.  It maintains a simple local db in /tmp\n\nThe application is fairly simple:\n    * user can specify a list of different timers.\n    * timers can be renamed.\n    * timers can be started / stopped concurrently.\n    * on startup the timers will resume the count from the last start.\n    * timers should not cross over days. automatic stop times at 23:59:59 for forgotten timers.\n    * daily statistics view\n\n\n\n## Installation\n```bash\npip install jtimer  # not timer\n```\n\n## Usage\n```bash\njtimer\n```\n\n## Planned Future developments\n\n* timer linked triggers\n* timer event view',
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
