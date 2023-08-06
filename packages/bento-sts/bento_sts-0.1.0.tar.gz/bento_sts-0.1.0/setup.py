# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bento_sts',
 'bento_sts.api',
 'bento_sts.config_sts',
 'bento_sts.errors',
 'bento_sts.main']

package_data = \
{'': ['*'], 'bento_sts': ['static/*', 'templates/*', 'templates/errors/*']}

install_requires = \
['Bootstrap-Flask>=1.5.2',
 'Flask-Moment>=0.5.2',
 'Flask-Paginate>=2021.10.29',
 'Flask-WTF>=0.14.3',
 'Jinja2>=2.11.3',
 'MarkupSafe>=1.1.1',
 'PyYAML>=5.4.1',
 'WTForms-Components>=0.10.5',
 'WTForms>=2.1',
 'Werkzeug>=1.0.1',
 'bento-meta>=0.0.32',
 'guess-language-spirit>=0.5.3',
 'gunicorn>=20.1.0',
 'idna>=2.6',
 'importlib_resources>=5.4.0',
 'itsdangerous>=0.24',
 'neo4j>=4.1',
 'python-dateutil>=2.6.1',
 'python-dotenv>=0.15.0',
 'python-editor>=1.0.3',
 'pytz>=2017.2',
 'requests>=2.20.0',
 'six>=1.15.0',
 'urllib3>=1.26.5',
 'visitor>=0.1.3']

setup_kwargs = {
    'name': 'bento-sts',
    'version': '0.1.0',
    'description': 'Bento Simple Terminology Server',
    'long_description': '# Welcome to bento-sts\n\nThis is a flask-based implementation of the Simple Terminology Service (STS) for the Bento Metadatabase (MDB).\n\n## Install\n\n\t$ git clone https://github.com/CBIIT/bento-sts.git\n\t$ cd pysts\n\t$ virtualenv sts-venv\n\t$ source sts-venv/bin/activate\n\t$ pip install -r requirements.txt\n\t$ flask run\n\n## Dependencies\n\n`bento-sts` requires a Neo4j-based [MDB](https://github.com/CBIIT/bento-meta).\n\n\n\n',
    'author': 'Mark Benson',
    'author_email': 'mark.benson@nih.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
