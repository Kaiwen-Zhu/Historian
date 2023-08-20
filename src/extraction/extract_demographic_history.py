from sys import stdout
import pandas as pd
from .utils import *


def extract_pop_size_by_species(game_log, data_path):
    """Extracts population size of various species respectively."""

    # data中的每项为 [date, species_name, pop_num]
    data = extract_info(game_log, "(?<=HIS_NUM_POP_OF_ONE_SPECIES:).*")

    if data:
        new_df = pd.DataFrame(columns = ["date", "species_name", "num_pop"])
        for row in data:
            new_df.loc[len(new_df.index)] = row

        merge_and_save_df(data_path, 'species_pop_size.csv', new_df)
            

def extract_demographic_history(game_log, data_path):  
    print("提取人口史...", end=' ')
    stdout.flush()
    
    extract_pop_size_by_species(game_log, data_path)  # 提取各物种人口数
        
    print("完成")
    stdout.flush()
