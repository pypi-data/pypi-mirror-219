# Python Environment Variable Helper

This Python package provides an easy way to interact with environment variables in your Python applications. It is designed to simplify the process of loading and parsing various data types from environment variables.

## Features

- Auto load environment variables from .env files based on application environment (`dev` or `test`).
- Provide easy-to-use functions to access environment variables with type hinting.
- Support different data types including strings, lists, dictionaries, integers and booleans.
- Allow defaults for environment variables.
- Provide decorator `@depends_on_env` for user-defined functions to ensure environment variables are loaded.

## Installation

Install the package from PyPi using pip:

```shell
pip install envutil
```

## Usage

Import the package in your Python code as follows:

```python
from envutil import env_str, env_csv, env_int, env_bool, env_list, env_dict
```

Access your environment variables:

```python
# Access string variable
my_var = env_str('MY_VAR', default='default-value')

# Access comma separated value as a list
my_csv = env_csv('MY_CSV', default=[])

# Access integer variable
my_int = env_int('MY_INT', default=0)

# Access boolean variable
my_bool = env_bool('MY_BOOL', default=False)

# Access list variable
my_list = env_list('MY_LIST', default=[])

# Access dictionary variable
my_dict = env_dict('MY_DICT', default={})
```

## Environment Configuration

By default, this package loads `.env` file. If the `APP_ENV` is set to `test`, it will load `.env.test` file. You can also specify a custom environment file by setting the `APP_ENV_FILE` environment variable.

## Contributing

Your contributions are always welcome! Please have a look at the [contribution guidelines](CONTRIBUTING.md) first. 🎉

## License

This package is released under the [MIT License](LICENSE).