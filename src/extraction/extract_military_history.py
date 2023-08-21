from sys import stdout
import pandas as pd
from .utils import *


def extract_fleet(game_log, data_path):
    """Extracts organization of navy."""   
     
    # data中的每项为 [date, fleet_name, *ship_sizes]
    data = extract_info(game_log, "(?<=HIS_FLEET:).*")
    
    if data:
        ship_sizes = ['corvette', 'frigate', 'destroyer', 'cruiser', 'battleship', 'titan', 'colossus', 'juggernaut', 'small_ship_fallen_empire', 'large_ship_fallen_empire', 'pirate_corvette', 'pirate_destroyer', 'galleon', 'psionic_avatar', 'space_amoeba', 'crisis_corvette', 'crisis_destroyer', 'crisis_cruiser', 'star_eater', 'caravaneer_destroyer_01', 'caravaneer_cruiser_01', 'graygoo_interdictor', 'graygoo_mothership', 'npc_warship_01', 'toxic_god']
        new_df = pd.DataFrame(columns = ["date", "fleet_name"] + ship_sizes)
        for row in data:
            new_df.loc[len(new_df.index)] = row

        merge_and_save_df(data_path, 'fleets.csv', new_df)


def extract_naval_size_capacity(game_log, data_path):
    # data中的每项为 [date, naval_size, naval_capacity]
    data = extract_info(game_log, "(?<=HIS_NAVAL_SIZE_CAPACITY:).*")
    
    if data:
        new_df = pd.DataFrame(columns = ["date", "naval_size", "naval_capacity"])
        for row in data:
            new_df.loc[len(new_df.index)] = row

        merge_and_save_df(data_path, 'naval_size_capacity.csv', new_df)
            

def extract_military_history(game_log, data_path):
    print("提取军事史...", end=' ')
    stdout.flush()
    
    extract_fleet(game_log, data_path)  # 提取海军组织
    extract_naval_size_capacity(game_log, data_path)  # 提取海军规模与舰队容量
        
    print("完成")
    stdout.flush()
    