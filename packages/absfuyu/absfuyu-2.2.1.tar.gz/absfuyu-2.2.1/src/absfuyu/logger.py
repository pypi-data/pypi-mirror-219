"""
Absfuyu: Logger
---
Logger Module

Version: 1.1.0
Last update: 09/06/2023 (mm/dd/yyyy)

Usage:
>>> from absfuyu.logger import logger, log_debug, LogLevel
"""


# Module level
###########################################################################
__all__ = [
    "logger", "log_debug",
    "LogLevel"
]


# Library
###########################################################################
from itertools import chain
import logging
import math


# Setup
###########################################################################
logger = logging.getLogger(__name__)
class _LogFormat:
    FULL = "[%(asctime)s] [%(process)-d] [%(module)s] [%(name)s] [%(funcName)s] [%(levelname)-s] %(message)s"
    SHORT = "[%(module)s] [%(name)s] [%(funcName)s] [%(levelname)-s] %(message)s"
_handler = logging.StreamHandler()
_handler.setLevel(logging.DEBUG)
_handler.setFormatter(logging.Formatter(_LogFormat.SHORT, "%Y-%m-%d %H:%M:%S"))
logger.addHandler(_handler)
logger.setLevel(logging.WARNING)


# Functions
###########################################################################
def _compress_list_for_print(iterable: list, max_visible: int = 3) -> str:
    """
    Compress the list to be more log-readable
    
    iterable : list
    max_visible : int
        maximum items can be printed on screen
        minimum is 3
    """

    if max_visible is None:
        max_visible = 3

    if max_visible <= 2:
        max_visible = 3
    
    if len(iterable) <= max_visible:
        return str(iterable)
    else:        
        # logger.debug(f"Max vis: {max_visible}")
        if max_visible % 2 == 0:
            cut_idx_1 = math.floor(max_visible/2) - 1
            cut_idx_2 = math.floor(max_visible/2)
        else:
            cut_idx_1 = cut_idx_2 = math.floor(max_visible/2)
        
        # logger.debug(f"Cut pos: {(cut_idx_1, cut_idx_2)}")
        temp = [iterable[:cut_idx_1], ["..."], iterable[len(iterable)-cut_idx_2:]]
        out = list(chain.from_iterable(temp))
        # logger.debug(out)
        return f"{out} Len: {len(iterable)}"

def _compress_string_for_print(text: str, max_visible: int = 25) -> str:
    """
    Compress the string to be more log-readable
    """
    
    if max_visible is None:
        max_visible = 25
    
    text = text.replace("\n", " ")
    # logger.debug(text)
    
    if len(text) <= max_visible:
        return str(text)
    else:
        cut_idx = math.floor((max_visible - 3) / 2)
        temp = f"{text[:cut_idx]}...{text[len(text)-cut_idx:]}"
        return f"{temp} Len: {len(text)}"


def log_debug(object_, max_visible: int = None) -> None:
    if isinstance(object_, list):
        logger.debug(_compress_list_for_print(object_, max_visible))
    elif isinstance(object_, set):
        logger.debug(_compress_list_for_print(list(object_), max_visible))
    elif isinstance(object_, dict):
        temp = [{k: v} for k, v in object_.items()]
        logger.debug(_compress_list_for_print(temp, max_visible))
    elif isinstance(object_, str):
        logger.debug(_compress_string_for_print(object_, max_visible))
    else:
        logger.debug(object_)


# Functions
###########################################################################
class LogLevel:
    """`logging`'s log level wrapper"""
    __TRACE: int = logging.DEBUG - 5 # Soon
    DEBUG: int = logging.DEBUG
    INFO: int = logging.INFO
    WARNING: int = logging.WARNING
    ERROR: int = logging.ERROR
    CRITICAL: int = logging.CRITICAL


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
