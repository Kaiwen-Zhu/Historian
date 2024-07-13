import re
from pathlib import Path
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


def merge_and_save_df(data_path: Path, file_name: str, new_df: DataFrame, keys: list[str] = ['date']) -> None:
    """Merges the new dataframe with the old one (if exists) and saves it.

    Args:
        data_path (Path): Path of directory of data.
        file_name (str): Filename of the dataframe.
        new_df (DataFrame): The new dataframe.
        keys (list[str]): Keys of dataframe (used to remove duplicate rows).
    """    

    file_path = data_path / file_name
    if file_path.exists():
        old_df: DataFrame = pd.read_csv(file_path, sep=';', index_col=0)
        new_first_date = new_df.iloc[0]['date']
        old_df = old_df[old_df['date'] < new_first_date]
        new_df = pd.concat([old_df, new_df], ignore_index=True)

    # 去重（因为回档）
    # 1. 确保时间记录不会倒序
    next_date = new_df.iloc[-1]['date']
    for i in range(len(new_df.index)-2, -1, -1):
        if new_df.iloc[i]['date'] > next_date:
            new_df.drop(i, inplace=True)
        else:
            next_date = new_df.iloc[i]['date']
    # 2. 去除 `keys` 重复的记录
    for col in keys:
        new_df[col] = new_df[col].apply(str)
    new_df.drop_duplicates(subset=keys, inplace=True, keep='last')
    new_df.reset_index(inplace=True, drop=True)

    new_df.to_csv(file_path, sep=';')
