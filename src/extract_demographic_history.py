from sys import stdout
import pandas as pd
from utils import extract_utils


def extract_total_pop_num(game_log, data_path):
    """ Extracts the total number of population.
    """    

    # data中的每项为 [date, pop_num]
    data = extract_utils.extract_info(game_log, "(?<=HIS_NUM_POP:).*")
    
    if data:
        new_df = pd.DataFrame(columns = ["date", "num_pop"])
        for row in data:
            new_df.loc[len(new_df.index)] = row

        extract_utils.merge_and_save_df(data_path, 'num_pop.csv', new_df)


def extract_pop_num_by_species(game_log, data_path):
    """ Extracts population size of various species respectively.
    """

    # data中的每项为 [date, species_name, pop_num]
    data = extract_utils.extract_info(game_log, "(?<=HIS_NUM_POP_OF_ONE_SPECIES:).*")

    if data:
        new_df = pd.DataFrame(columns = ["date", "species_name", "num_pop"])
        for row in data:
            new_df.loc[len(new_df.index)] = row

        extract_utils.merge_and_save_df(data_path, 'species_pop_num.csv', new_df, keys=["date","species_name"])
            

def extract_demographic_history(game_log, data_path):  
    print("Extracting the demographic history ...")
    stdout.flush()
    
    extract_total_pop_num(game_log, data_path)  # 提取人口总数
    extract_pop_num_by_species(game_log, data_path)  # 提取各物种人口数
        
    print("Done!")
    stdout.flush()