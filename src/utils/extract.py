import re
from os import path
import pandas as pd


def extract_info(game_log: str, pat: str) -> list[list[str]]:
    """ Extracts information of some pattern from log.

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


def merge_and_save_df(data_path: str, file_name: str, new_df) -> None:
    """ Merges the new dataframe with the old one (if exists) and saves it.

    Args:
        data_path (str): Path of directory of data.
        file_name (str): Filename of the dataframe.
        new_df (Dataframe): The new dataframe.
    """    

    file_path = path.join(data_path, file_name)
    if path.exists(file_path):
        old_df = pd.read_csv(file_path, sep=';', index_col=0)
        dup_index = old_df.index.intersection(new_df.index)
        old_df.drop(index = dup_index, inplace = True)
        new_df = pd.concat([old_df, new_df])
    new_df.to_csv(file_path, sep=';')