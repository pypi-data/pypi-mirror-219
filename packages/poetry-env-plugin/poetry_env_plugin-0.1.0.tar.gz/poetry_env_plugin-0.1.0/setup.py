# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_env_plugin']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.5.1,<2.0.0']

entry_points = \
{'poetry.plugin': ['env = poetry_env_plugin:EnvPlugin']}

setup_kwargs = {
    'name': 'poetry-env-plugin',
    'version': '0.1.0',
    'description': 'A Poetry plugin to load environment variables from .env file',
    'long_description': '# Poetry Env Plugin\n',
    'author': 'Brian Jinwright',
    'author_email': 'bjinwright@qwigo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
