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
['black==23.3.0',
 'chromadb==0.3.21',
 'dill==0.3.6',
 'docstring-parser==0.15',
 'fake-useragent==1.1.3',
 'fastapi==0.95.2',
 'fire==0.5.0',
 'google-api-python-client==2.86.0',
 'google-search-results==2.4.2',
 'huggingface-hub==0.13.4',
 'jinja2',
 'jinja2schema==0.1.4',
 'langchain==0.0.141',
 'langflow==0.0.54',
 'lxml==4.9.2',
 'networkx==3.1',
 'openai==0.27.4',
 'pandas==1.5.3',
 'passlib==1.7.4',
 'psycopg2-binary==2.9.6',
 'pyarrow==11.0.0',
 'pyjwt[crypto]',
 'pymysql',
 'pypdf==3.8.1',
 'pysrt==1.1.2',
 'rich==13.3.4',
 'sqlalchemy',
 'typer==0.7.0',
 'types-pyyaml',
 'unstructured==0.6.1',
 'uvicorn==0.20.0']

entry_points = \
{'console_scripts': ['cf_server = chainfury_server.server:main',
                     'chainfury_server = chainfury_server.server:main']}

setup_kwargs = {
    'name': 'chainfury-server',
    'version': '1.0.2',
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
