from sys import stdout
import pandas as pd
from .utils import *


def extract_opinion(game_log, data_path):
    """ Extracts mutual opinions of all countries.
    """    

    # data中的每项为 [date, name, my_opinion, its_opinion]
    data = extract_info(game_log, "(?<=HIS_OPINION:).*")
    
    if data:
        new_df = pd.DataFrame(columns=["date"])
        for ele in data:
            date = ele[0]
            if date not in list(new_df["date"]):
                new_df.loc[len(new_df.index), "date"] = date

            country_name = ele[1]
            if f"opinion_on_{country_name}" not in new_df.columns:
                new_df[f"opinion_on_{country_name}"] = pd.NA
                new_df[f"{country_name}'s_opinion"] = pd.NA

            new_df.loc[new_df[new_df["date"]==date].index, f"opinion_on_{country_name}"] = ele[2]
            new_df.loc[new_df[new_df["date"]==date].index, f"{country_name}'s_opinion"] = ele[3]

        merge_and_save_df(data_path, 'opinions.csv', new_df)
            

def extract_diplomatic_history(game_log, data_path):
    print("Extracting the diplomatic history ...")
    stdout.flush()
    
    extract_opinion(game_log, data_path)  # 提取我国与其它国家之间相互的评价
        
    print("Done!")
    stdout.flush()