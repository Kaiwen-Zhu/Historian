from sys import stdout
import pandas as pd
from .utils import *


def extract_ship_building(game_log, data_path):
    """Extracts records of building ships."""   
     
    # data中的每项为 [date, ship_size, ship_design_name, ship_name]
    data = extract_info(game_log, "(?<=HIS_BUILT_SHIP:).*")
    
    if data:
        new_df = pd.DataFrame(columns = ["date", "ship_size", "ship_design_name", "ship_name"])
        for row in data:
            new_df.loc[len(new_df.index)] = row

        merge_and_save_df(data_path, 'ship_building.csv', new_df, keys=["date","ship_name"])
            

def extract_military_history(game_log, data_path):
    print("提取军事史...", end=' ')
    stdout.flush()
    
    extract_ship_building(game_log, data_path)  # 提取舰船建造记录
        
    print("完成")
    stdout.flush()
    