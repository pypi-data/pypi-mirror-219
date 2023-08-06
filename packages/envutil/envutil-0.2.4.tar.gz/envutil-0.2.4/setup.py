# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['envutil']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'envutil',
    'version': '0.2.4',
    'description': '',
    'long_description': "# Python Environment Variable Helper\n\nThis Python package provides an easy way to interact with environment variables in your Python applications. It is designed to simplify the process of loading and parsing various data types from environment variables.\n\n## Features\n\n- Auto load environment variables from .env files based on application environment (`dev` or `test`).\n- Provide easy-to-use functions to access environment variables with type hinting.\n- Support different data types including strings, lists, dictionaries, integers and booleans.\n- Allow defaults for environment variables.\n- Provide decorator `@depends_on_env` for user-defined functions to ensure environment variables are loaded.\n\n## Installation\n\nInstall the package from PyPi using pip:\n\n```shell\npip install envutil\n```\n\n## Usage\n\nImport the package in your Python code as follows:\n\n```python\nfrom envutil import env_str, env_csv, env_int, env_bool, env_list, env_dict\n```\n\nAccess your environment variables:\n\n```python\n# Access string variable\nmy_var = env_str('MY_VAR', default='default-value')\n\n# Access comma separated value as a list\nmy_csv = env_csv('MY_CSV', default=[])\n\n# Access integer variable\nmy_int = env_int('MY_INT', default=0)\n\n# Access boolean variable\nmy_bool = env_bool('MY_BOOL', default=False)\n\n# Access list variable\nmy_list = env_list('MY_LIST', default=[])\n\n# Access dictionary variable\nmy_dict = env_dict('MY_DICT', default={})\n```\n\n## Environment Configuration\n\nBy default, this package loads `.env` file. If the `APP_ENV` is set to `test`, it will load `.env.test` file. You can also specify a custom environment file by setting the `APP_ENV_FILE` environment variable.\n\n## Contributing\n\nYour contributions are always welcome! Please have a look at the [contribution guidelines](CONTRIBUTING.md) first. 🎉\n\n## License\n\nThis package is released under the [MIT License](LICENSE).",
    'author': 'Berke Arslan',
    'author_email': 'berke@kwilabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
