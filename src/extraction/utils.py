import re
from os import path
import pandas as pd
from pandas.core.frame import DataFrame


def extract_info(game_log: str, pat: str) -> list[list[str]]:
    """Extracts information of some pattern from log.

    Args:
        game_log (str): Log of game.
        pat (str): Pattern of target info.
        
    Returns:
        Target info organized into list of lists. Each element
        in it represents an entry.
    """
    
    pat = re.compile(pat)
    data = pat.findall(game_log)
    return [row.split(',') for row in data]


def merge_and_save_df(data_path: str, file_name: str, new_df: DataFrame, keys: list[str] = ['date']) -> None:
    """Merges the new dataframe with the old one (if exists) and saves it.

    Args:
        data_path (str): Path of directory of data.
        file_name (str): Filename of the dataframe.
        new_df (DataFrame): The new dataframe.
        keys (list[str]): Keys of dataframe (used to remove duplicate rows).
    """    

    file_path = path.join(data_path, file_name)
    if path.exists(file_path):
        old_df = pd.read_csv(file_path, sep=';', index_col=0)
        new_df = pd.concat([old_df, new_df], ignore_index=True)
        # `old_df` 中的数据类型均为 `str`，而去重时需要比较，
        # 因此需要将 `new_df` 中作为 `keys` 的列中的数据都转为 `str`
        for col in keys:
            new_df[col] = new_df[col].apply(str)
        new_df.drop_duplicates(subset=keys, inplace=True, keep='last')
        new_df.reset_index(inplace=True, drop=True)
    new_df.to_csv(file_path, sep=';')
