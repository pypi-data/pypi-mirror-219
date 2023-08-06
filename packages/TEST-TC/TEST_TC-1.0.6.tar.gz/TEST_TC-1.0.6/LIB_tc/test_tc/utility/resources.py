from __future__ import annotations

import os
import sys
from typing import Any, Dict

import tomli

def get_configuration(name: str, config_path : str, config_file: str = "web_app.toml") -> Dict[str, Any]:
    """Read the configurations set in the properties.toml file in the config folder and returns them
    as a dictionary

    Parameters
    ----------
    name : str
        Section to be 
    config_path : str
        Specifies the config path where the .toml configurations resides
    config_file : str, optional
        Specifies the config file to read, by default 'properties.toml'

    Returns
    -------
    dict
        Dictionary containing the properties read

    Raises
    ------
    Exception
        Raise error if .conf file is not found
    """

    if config_file not in os.listdir(config_path):
        raise Exception(
            f"File {config_file} not found in {config_path} please double check that the filename is correct."
        )

    config = tomli.load(open(os.path.join(config_path, config_file), "rb"))
    # Read from the specified file, the specified section
    if name in config:
        return config[name]
    else:
        raise Exception("System " + name + " not found in .conf file")

def log_exception(logger=None):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    Parameters
    ----------
    logger : logging.Logger, default: None
        The logger to use, if None error and traceback will be printed anyway.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in "
                err += func.__name__
                print(err)
                if logger:
                    logger.exception(err)
                sys.exit()

        return wrapper

    return decorator