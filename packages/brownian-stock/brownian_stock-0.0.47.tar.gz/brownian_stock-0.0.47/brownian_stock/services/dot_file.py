import pathlib
from dataclasses import dataclass
from typing import Optional, Union

import dacite
import yaml


@dataclass
class DotfileConfig:
    username: Optional[str] = None
    password: Optional[str] = None


def load_config(
    path: Union[None, str, pathlib.Path] = None,
    args_username: Optional[str] = None,
    args_password: Optional[str] = None,
) -> Optional[DotfileConfig]:
    dot_path = pathlib.Path("~/.brownianrc")
    if isinstance(path, str):
        dot_path = pathlib.Path(path)
    if isinstance(path, pathlib.Path):
        dot_path = path
    dot_path = dot_path.expanduser()

    if not dot_path.exists():
        return None

    with open(dot_path, "r") as fp:
        data_dict = yaml.safe_load(fp)

    conf = dacite.from_dict(DotfileConfig, data_dict)
    if args_username is not None:
        conf.username = args_username
    if args_password is not None:
        conf.password = args_password
    return conf
