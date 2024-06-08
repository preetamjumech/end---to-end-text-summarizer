import os
import yaml
from box.exceptions import BoxValueError
from box import ConfigBox
from ensure import ensure_annotations
from pathlib import Path
from typing import Any
from textSummarizer.logging import logger


@ensure_annotations
def read_yaml(path: Path) -> ConfigBox:
    try:
        with open(path) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok= True)
        if verbose:
            logger.info(f"creating directory at: {path}")


@ensure_annotations
def get_size(path: Path) -> str:
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"


