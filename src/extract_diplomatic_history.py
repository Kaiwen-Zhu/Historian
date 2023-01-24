from sys import stdout
import pandas as pd
from utils import extract


# 提取我国与其它国家之间相互的评价
def extract_opinion(game_log, data_path):
    """ Extracts mutual opinions of all countries.
    """    

    # data中的每项为 [date, name, my_opinion, its_opinion]
    data = extract.extract_info(game_log, "(?<=HIS_OPINION:).*")
    
    if data:
        new_df = pd.DataFrame()
        for ele in data:
            date = ele[0]
            country_name = ele[1]
            if f"opinion_on_{country_name}" not in new_df.columns:
                new_df[f"opinion_on_{country_name}"] = pd.NA
                new_df[f"{country_name}'s_opinion"] = pd.NA
            if date not in new_df.index:
                new_df.loc[date] = pd.NA
            new_df.loc[date, f"opinion_on_{country_name}"] = ele[2]
            new_df.loc[date, f"{country_name}'s_opinion"] = ele[3]

        extract.merge_and_save_df(data_path, 'opinions.csv', new_df)
            

def extract_diplomatic_history(game_log, data_path):
    print("Extracting the diplomatic history ...")
    stdout.flush()
    
    extract_opinion(game_log, data_path)  # 提取我国与其它国家之间相互的评价
        
    print("Done!")
    stdout.flush()