from functools import wraps
from os import environ

from dotenv import load_dotenv

__ENV_LOADED: bool = False


def depends_on_env(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        load_env()
        return func(*args, **kwargs)

    return wrapper


def load_env():
    global __ENV_LOADED
    if __ENV_LOADED:
        return

    default_dotenv = ".env"
    if environ.get("APP_ENV", "dev") == "test":
        default_dotenv = ".env.test"

    load_dotenv(
        environ.get(
            "APP_ENV_FILE",
            default_dotenv,
        ),
        interpolate=True,
        override=False,
        verbose=True,
    )

    __ENV_LOADED = True


@depends_on_env
def env_str(key: str, default: str = "") -> str:
    return environ.get(key, default)


@depends_on_env
def env_csv(key: str, default: list[str] | None = None) -> list[str]:
    if default is None:
        default = []

    var = environ.get(key, None)
    if var is None:
        return default

    return [x.strip() for x in var.split(",")]


@depends_on_env
def env_int(key: str, default: int = 0) -> int:
    return int(env_str(key, str(default)))


@depends_on_env
def env_bool(key: str, default: bool = False) -> bool:
    return env_str(key, str(default)).lower() in ["true", "1", "yes", "on"]


@depends_on_env
def env_list(key: str, default: list[str] | None = None) -> list[str]:
    if default is None:
        default = []

    var = env_str(key, None)
    if var is None:
        return default

    return [x.strip() for x in var.split(",")]


@depends_on_env
def env_dict(key: str, default: dict | None = None) -> dict:
    if default is None:
        default = {}

    var = env_str(key, None)
    if var is None:
        return default

    return {x.strip().split(":")[0]: x.strip().split(":")[1] for x in var.split(",")}
