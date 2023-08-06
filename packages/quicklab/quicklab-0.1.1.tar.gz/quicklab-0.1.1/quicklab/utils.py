import asyncio
import datetime
import math
import os
import re
import time
import unicodedata
from datetime import timedelta
from importlib import import_module
from os.path import expanduser
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

import requests
import tomli
import tomli_w
from nanoid import generate
from rich.table import Table

from quicklab.defaults import NANO_ID_ALPHABET, QUICKLAB_CONF
from quicklab.types import ProjectSettings, UserSettings

user_settings_path = (
    Path(expanduser("~")) / Path(".config/quicklab") / Path(QUICKLAB_CONF)
)


def generate_random(
    size: int = 10, strategy: str = "nanoid", alphabet: str = NANO_ID_ALPHABET
) -> str:
    """Default URLSafe id"""
    if strategy == "nanoid":
        return generate(alphabet=alphabet, size=size)
    raise NotImplementedError("Strategy %s not implemented", strategy)


async def run_async(func: Callable, *args, **kwargs):
    """Run sync functions from async code"""
    loop = asyncio.get_running_loop()
    rsp = await loop.run_in_executor(None, func, *args, **kwargs)
    return rsp


def mkdir_p(fp: str) -> None:
    """Make the fullpath
    similar to mkdir -p in unix systems.
    """
    Path(fp).mkdir(parents=True, exist_ok=True)


def get_class(fullclass_path: str) -> Any:
    """get a class or object from a module. The fullclass_path should be passed as:
    package.my_module.MyClass
    """
    module, class_ = fullclass_path.rsplit(".", maxsplit=1)
    mod = import_module(module)
    cls = getattr(mod, class_)
    return cls


def write_toml(fpath: str, data: Dict[Any, Any]) -> None:
    """Write a dictionary to a file in TOML format"""
    with open(fpath, "wb") as f:
        tomli_w.dump(data, f)


def read_toml(fpath: str) -> Dict[Any, Any]:
    """Read a TOML file into a dictionary"""
    with open(fpath, "r") as f:
        data = tomli.loads(f.read())
        return data


def convert_size(size_bytes: int) -> str:
    """Humanize a size in bytes"""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def from_path_to_module_str(fp: str) -> str:
    """experimental:
    from "examples/model.py" it should return
    "example.model"
    """
    return fp.rsplit(".", maxsplit=1)[0].replace("/", ".")


def load_user_settings() -> Optional[UserSettings]:
    """Load user settings from a Toml file"""
    if user_settings_path.is_file():
        return UserSettings.parse_obj(read_toml(user_settings_path))


def save_user_settings(settings: UserSettings) -> None:
    """Save user settings to a Toml file"""
    mkdir_p(os.path.dirname(user_settings_path))
    write_toml(user_settings_path, settings.dict())


def get_user_setting(key: str, default: Optional[Any] = None) -> Optional[Any]:
    """
    Fetch a user setting by key

    If key is not present, fallback to a default value argument.
    """
    settings = load_user_settings()
    if settings:
        return settings.dict().get(key, default)
    return default


def get_project_settings_path() -> Path:
    """Get path to project settings config file"""
    return get_project_root_path() / Path(QUICKLAB_CONF)


def get_project_root_path() -> Path:
    """Get path to project root directory, based on current working directory"""
    cwd = os.getcwd()
    return find_vcs_root(cwd, default=cwd)


def load_project_settings() -> Optional[ProjectSettings]:
    """Load project settings from a Toml file at the project root directory"""
    settings_path = get_project_settings_path()
    if settings_path.is_file():
        return ProjectSettings.parse_obj(read_toml(settings_path))


def save_project_settings(settings: ProjectSettings) -> None:
    """Save project settings to a Toml file at the project root directory"""
    settings_path = get_project_settings_path()
    write_toml(settings_path, settings.dict())


def build_table_from_dict(
    d: Dict, key_title="key", value_title="value", **params
) -> Table:
    """Build a Rich Table instance from a dictionary"""
    table = Table(**params)
    table.add_column(key_title)
    table.add_column(value_title)
    for k, v in d.items():
        table.add_row(k, v)
    return table


def slugify(value: Any, allow_unicode: bool = False) -> str:
    """
    Convert to ASCII if 'allow_unicode' is False.

    Convert spaces or repeated dashes to single dashes. Remove characters that
    aren't alphanumerics, underscores, or hyphens. Convert to lowercase. Also
    strip leading and trailing whitespace, dashes, and underscores.

    Taken from https://github.com/django/django/blob/master/django/utils/text.py

    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def find_vcs_root(test: str, dirs: Tuple[str] = (".git",), default: str = None) -> Path:
    """Find VCS root path from a test directory path"""
    prev, test = None, os.path.abspath(test)
    while prev != test:
        if any(os.path.isdir(os.path.join(test, d)) for d in dirs):
            return Path(test)
        prev, test = test, os.path.abspath(os.path.join(test, os.pardir))
    return Path(default)


def check_readiness(url: str, timeout: int = 10 * 60) -> int:
    start_time = datetime.datetime.now()
    end_time = start_time + timedelta(seconds=timeout)
    code = -1
    _url = url if url.startswith("https://") else f"https://{url}"
    while code != 200 and datetime.datetime.now() < end_time:
        try:
            res = requests.get(_url, timeout=20)
            code = res.status_code
        except requests.exceptions.RequestException:
            code = -1
        if code != 200:
            time.sleep(10)
    return code
