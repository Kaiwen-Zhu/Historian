import re
from os.path import join as path_join, exists as path_exists
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


def merge_and_save_df(data_path: str, file_name: str, new_df: DataFrame):
    """Merges the new dataframe with the old one (if exists) and saves it.

    Args:
        data_path (str): Path of directory of data.
        file_name (str): Filename of the dataframe.
        new_df (DataFrame): The new dataframe.
    """    

    file_path = path_join(data_path, file_name)
    if path_exists(file_path):
        old_df: DataFrame = pd.read_csv(file_path, sep=';', index_col=0)
        new_first_date = new_df.iloc[0]['date']
        old_df = old_df[old_df['date'] < new_first_date]
        new_df = pd.concat([old_df, new_df], ignore_index=True)
        new_df.reset_index(inplace=True, drop=True)
    new_df.to_csv(file_path, sep=';')
