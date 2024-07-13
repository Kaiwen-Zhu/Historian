from sys import stdout
from pathlib import Path
import pandas as pd
from .utils import *


def extract_economic_history(game_log: str, data_path: Path):
    """Extracts the reserves and monthly income of all kinds of resources."""    

    print("提取经济史...", end=' ')
    stdout.flush()
    
    data = extract_info(game_log, "(?<=HIS_RESERVES_INCOME:).*")

    if data:
        new_df = pd.DataFrame(columns = ["date", "energy_reserves", "minerals_reserves", 
                "food_reserves", "consumer_goods_reserves", "alloys_reserves", 
                "volatile_motes_reserves", "exotic_gases_reserves", "rare_crystals_reserves", 
                "living_metal_reserves", "zro_reserves", "dark_matter_reserves", 
                "nanites_reserves", "minor_artifacts_reserves", "unity_reserves", 
                "energy_income", "minerals_income", "food_income", "consumer_goods_income",
                "alloys_income", "volatile_motes_income", "exotic_gases_income",
                "rare_crystals_income", "living_metal_income", "zro_income",
                "dark_matter_income", "nanites_income", "minor_artifacts_income", "unity_income",
                "physics_research_income", "society_research_income", "engineering_research_income"])
        for row in data:
            new_df.loc[len(new_df.index)] = row

        merge_and_save_df(data_path, 'resources.csv', new_df, keys=["date"])
        
    print("完成")
    stdout.flush()
