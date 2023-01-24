from sys import stdout
import pandas as pd
from utils import extract


def extract_economic_history(game_log, data_path):
    """ Extracts the reserves and monthly income of all kinds of resources.
    """    

    print("Extracting the economic history ...")
    stdout.flush()
    
    data = extract.extract_info(game_log, "(?<=HIS_RESERVES_INCOME:).*")

    if data:
        new_df = pd.DataFrame(columns = ["energy_reserves", "minerals_reserves", "food_reserves",
                "consumer_goods_reserves", "alloys_reserves", "volatile_motes_reserves",
                "exotic_gases_reserves", "rare_crystals_reserves", "living_metal_reserves",
                "zro_reserves", "dark_matter_reserves", "nanites_reserves", "unity_reserves", 
                "energy_income", "minerals_income", "food_income", "consumer_goods_income",
                "alloys_income", "volatile_motes_income", "exotic_gases_income",
                "rare_crystals_income", "living_metal_income", "zro_income",
                "dark_matter_income", "nanites_income", "unity_income",
                "physics_research_income", "society_research_income", "engineering_research_income"])
        for row in data:
            new_df.loc[row[0]] = row[1:]

        extract.merge_and_save_df(data_path, 'resources.csv', new_df)
        
    print("Done!")
    stdout.flush()