"""
Absfuyu: Data Analysis [W.I.P]
---
Extension for `pd.DataFrame`

Version: 2.0.0
Date updated: 28/06/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
from collections import namedtuple
import random
import itertools
from typing import List, Optional, Union

# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from absfuyu.logger import logger


# Function
###########################################################################
def summary(data: Union[list, np.ndarray]):
    """
    Quick summary of data
    
    data : np.ndarray | list
    """
        
    if not isinstance(data, np.ndarray):
        data = np.array(data)

    output = {
        "Observations": len(data),
        "Mean": np.mean(data),
        "Median": np.median(data),
        "Mode": stats.mode(data)[0][0],
        "Standard deviation": np.std(data),
        "Variance": np.var(data),
        "Max": max(data),
        "Min": min(data),
        "Percentiles": {
            "1st Quartile": np.quantile(data, 0.25),
            "2nd Quartile": np.quantile(data, 0.50),
            "3rd Quartile": np.quantile(data, 0.75),
            "IQR": stats.iqr(data),
        },
    }
    return output


def divide_dataframe(df: pd.DataFrame, by: str) -> list:
    """
    Divide df into a list of df
    """
    divided = [y for _, y in df.groupby(by)]
    # divided[0] # this is the first separated df
    # divided[len(divided)-1] # this is the last separated df
    return divided


def delta_date(df: pd.DataFrame, date_field: str, col_name: str="delta_date"):
    """
    Calculate date interval between row
    """
    dated = df[date_field].to_list()
    cal = []
    for i in range(len(dated)):
        if i==0:
            cal.append(dated[i]-dated[i])
        else:
            cal.append(dated[i]-dated[i-1])
    df[col_name] = [x.days for x in cal]
    return df


def modify_date(df: pd.DataFrame, date_col: str):
    """
    Add date, week, and year column for date_col
    """
    df["Date"] = pd.to_datetime(df[date_col])
    df["Week"] = df["Date"].dt.isocalendar().week
    df["Year"] = df["Date"].dt.isocalendar().year
    return df


def equalize_df(data: dict, fillna = np.nan):
    """
    Make all list in dict have equal length to make pd.DataFrame
    """
    max_len = 0
    for _, v in data.items():
        if len(v) >= max_len:
            max_len = len(v)
    for _, v in data.items():
        if len(v) < max_len:
            missings = max_len-len(v)
            for _ in range(missings):
                v.append(fillna)
    return data



# Class
###########################################################################
PLTFormatString = namedtuple("PLTFormatString", ["marker", "line_style", "color"])

class _DictToAtrr:
    """Convert `keys` or `values` of `dict` into attribute"""
    def __init__(
            self, 
            dict_data: dict,
            *,
            key_as_atrribute: bool = True,
            remove_char: str = r"( ) [ ] { }"
        ) -> None:
        """
        dict_data: Dictionary to convert
        key_as_atrribute: Use `dict.keys()` as atrribute when True, else use `dict.values()`
        remove_char: Characters that excluded from attribute name
        """
        self._data = dict_data

        if key_as_atrribute:
            # temp = list(map(self._remove_space, self._data.keys()))
            temp = [self._remove_space(x, remove_char) for x in self._data.keys()]
            [self.__setattr__(k, v) for k, v in zip(temp, self._data.values())]
        else:
            temp = [self._remove_space(x, remove_char) for x in self._data.values()]
            [self.__setattr__(k, v) for k, v in zip(temp, self._data.keys())]
        self._keys = temp

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self._keys})"
    def __repr__(self) -> str:
        return self.__str__()
    
    @staticmethod
    def _remove_space(value: str, remove_char: str) -> str:
        """
        Remove special characters and replace space with underscore
        """
        remove_char = remove_char.split(" ")
        logger.debug(remove_char)
        for x in remove_char:
            value = value.replace(x, "")
        value = value.replace(" ", "_")
        return value


class MatplotlibFormatString:
    """
    Format string format: `[marker][line][color]` or `[color][marker][line]`
    """
    MARKER_LIST = {
        ".": "point marker",
        ",": "pixel marker",
        "o": "circle marker",
        "v": "triangle_down marker",
        "^": "triangle_up marker",
        "<": "triangle_left marker",
        ">": "triangle_right marker",
        "1": "tri_down marker",
        "2": "tri_up marker",
        "3": "tri_left marker",
        "4": "tri_right marker",
        "8": "octagon marker",
        "s": "square marker",
        "p": "pentagon marker",
        "P": "plus (filled) marker",
        "*": "star marker",
        "h": "hexagon1 marker",
        "H": "hexagon2 marker",
        "+": "plus marker",
        "x": "x marker",
        "X": "x (filled) marker",
        "D": "diamond marker",
        "d": "thin_diamond marker",
        "|": "vline marker",
        "_": "hline marker"
    }
    LINE_STYLE_LIST = {
        "-": "solid line style",
        "--": "dashed line style",
        "-.": "dash-dot line style",
        ":": "dotted line style"
    }
    COLOR_LIST = {
        "b": "blue",
        "g": "green",
        "r": "red",
        "c": "cyan",
        "m": "magenta",
        "y": "yellow",
        "k": "black",
        "w": "white"
    }
    Marker = _DictToAtrr(MARKER_LIST, key_as_atrribute=False)
    LineStyle = _DictToAtrr(LINE_STYLE_LIST, key_as_atrribute=False)
    Color = _DictToAtrr(COLOR_LIST, key_as_atrribute=False)

    @staticmethod
    def all_format_string() -> List[PLTFormatString]:
        fmt_str = [__class__.MARKER_LIST, __class__.LINE_STYLE_LIST, __class__.COLOR_LIST]
        return [PLTFormatString._make(x) for x in list(itertools.product(*fmt_str))]

    @staticmethod
    def get_random(alt: bool = False) -> str:
        temp = random.choice(__class__.all_format_string())
        if alt:
            return f"{temp.marker}{temp.line_style}{temp.color}"
        else:
            return f"{temp.color}{temp.marker}{temp.line_style}"
    


class DataFrameKai(pd.DataFrame):
    def get_unique(self, col: str):
        """
        Return a list of unique values in a column
        """
        return list(self[col].unique())
    
    def convert_to_SeriesKai(self):
        pass

    def summary(self, col: str):
        """
        Quick summary of data
        """
        data = self[col]
            
        if not isinstance(data, np.ndarray):
            data = np.array(data)

        output = {
            "Observations": len(data),
            "Mean": np.mean(data),
            "Median": np.median(data),
            "Mode": stats.mode(data)[0][0],
            "Standard deviation": np.std(data),
            "Variance": np.var(data),
            "Max": max(data),
            "Min": min(data),
            "Percentiles": {
                "1st Quartile": np.quantile(data, 0.25),
                "2nd Quartile": np.quantile(data, 0.50),
                "3rd Quartile": np.quantile(data, 0.75),
                "IQR": stats.iqr(data),
            },
        }
        return output


class SeriesKai(pd.Series):
    pass

# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)
