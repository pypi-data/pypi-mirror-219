# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chainfury_server',
 'chainfury_server.api',
 'chainfury_server.commons',
 'chainfury_server.database_utils',
 'chainfury_server.plugins',
 'chainfury_server.plugins.echo',
 'chainfury_server.plugins.nbx',
 'chainfury_server.schemas',
 'chainfury_server.stories']

package_data = \
{'': ['*'],
 'chainfury_server': ['examples/*',
                      'static/*',
                      'static/assets/*',
                      'static/script/*',
                      'templates/*']}

install_requires = \
['Jinja2==3.1.2', 'fire==0.5.0', 'jinja2schema==0.1.4']

entry_points = \
{'console_scripts': ['cf_server = chainfury_server.server:main',
                     'chainfury_server = chainfury_server.server:main']}

setup_kwargs = {
    'name': 'chainfury-server',
    'version': '1.0.1',
    'description': 'ChainFury Server is the open source server for running ChainFury Engine!',
    'long_description': '# ChainFury Server\n\nThis is a package separate from `chainfury` which provides the python execution engine.\n',
    'author': 'NimbleBox Engineering',
    'author_email': 'engineering@nimblebox.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/NimbleBoxAI/ChainFury',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
