#!/usr/bin/env python3
"""Script to run a Pod that acts as a compute and data provider."""
import logging
import os
from os import PathLike
from typing import Union

import fire

from bitfount import config
from bitfount.runners.pod_runner import setup_pod_from_config_file
from bitfount.runners.utils import setup_loggers

log_level = os.getenv("BITFOUNT_LOG_LEVEL", logging.INFO)

loggers = setup_loggers([logging.getLogger("bitfount")], log_level=log_level)

config._BITFOUNT_CLI_MODE = True


def run(path_to_config_yaml: Union[str, PathLike]) -> None:
    """Runs a pod from a config file."""
    pod = setup_pod_from_config_file(path_to_config_yaml)
    pod.start()


if __name__ == "__main__":
    fire.Fire(run)
