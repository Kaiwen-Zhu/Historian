from sys import stdout
import pandas as pd
from json import load as json_load, dump as json_dump
from .utils import *


def extract_opinion(game_log, data_path):
    """Extracts mutual opinions of all countries and updates mapping from id to name if necessary."""    

    # data中的每项为 [date, id, name, our_opinion, their_opinion]
    data = extract_info(game_log, "(?<=HIS_OPINION:).*")
    
    if data:
        if path.exists(path.join(data_path, 'mapping.json')):
            with open(path.join(data_path, 'mapping.json'), encoding='utf-8') as f:
                mapping = json_load(f)
        else:
            mapping = {}

        new_df = pd.DataFrame(columns=["date"])
        for ele in data:
            date = ele[0]
            if date not in set(new_df["date"]):
                new_df.loc[len(new_df.index), "date"] = date

            country_id, country_name = ele[1], ele[2]
            mapping[country_id] = country_name
            if f"our_opinion_{country_id}" not in new_df.columns:
                new_df[f"our_opinion_{country_id}"] = pd.NA
                new_df[f"their_opinion_{country_id}"] = pd.NA

            new_df.loc[new_df[new_df["date"]==date].index, f"our_opinion_{country_id}"] = ele[3]
            new_df.loc[new_df[new_df["date"]==date].index, f"their_opinion_{country_id}"] = ele[4]

        merge_and_save_df(data_path, 'opinions.csv', new_df)
        with open(path.join(data_path, 'mapping.json'), 'w', encoding='utf-8') as f:
            json_dump(mapping, f, ensure_ascii=False)
    
        return mapping
    
    return {}
            

def extract_diplomatic_history(game_log, data_path):
    print("提取外交史...", end=' ')
    stdout.flush()
    
    mapping = extract_opinion(game_log, data_path)  # 提取我国与其它国家之间相互的评价
        
    print("完成")
    stdout.flush()
