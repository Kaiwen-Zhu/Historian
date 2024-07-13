from sys import stdout
from pathlib import Path
import pandas as pd
from .utils import *


def extract_scientific_history(game_log: str, data_path: Path):
    """Extracts the complete date and descriptions of technologies."""

    print("提取科技史...", end=' ')
    stdout.flush()
    
    data = extract_info(game_log, "(?<=HIS_SCIENCE:).*")

    if data:
        new_df = pd.DataFrame(columns = ["date", "id"])
        for row in data:
            new_df.loc[len(new_df.index)] = row

        merge_and_save_df(data_path, 'technologies.csv', new_df, keys=['id'])
        
    print("完成")
    stdout.flush()
