from pathlib import Path
from typing import Optional

import yaml


def get_config(key: Optional[str] = None):
    cfg = yaml.safe_load(open('config.yaml'))

    if key is None:
        return cfg

    if key not in cfg:
        raise KeyError(f'Key not found in config: {key}')
    else:
        return cfg.get(key)


def create_folder(folder_name: str, path: Optional[str] = None):
    _path = path or Path.cwd()
    folder_path = _path / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)

    if not folder_path.exists():
        raise FileNotFoundError(f'Failed to create folder: {folder_path}')
    else:
        print(f'Folder created: {folder_path}')

