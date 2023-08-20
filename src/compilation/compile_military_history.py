from sys import stdout
from os.path import join as path_join
import pandas as pd
from pandas.core.frame import DataFrame
from json import load as json_load
from jinja2 import Environment
from .utils import *


def list_fleets(env: Environment, assets_path: str, data_path: str):
    df = pd.read_csv(path_join(data_path, 'fleets.csv'), index_col=0, sep=';')
    last_date = df['date'].iloc[-1]
    df_last: DataFrame = df[df['date'] == last_date]
    df_last = df_last.reset_index(drop=True)
    
    with open(path_join(assets_path, 'entities', 'ship_size_localisation.json'), encoding='utf-8') as f:
        ship_size_loc = json_load(f)
    
    fleets = []
    for i in range(len(df_last)):
        fleet = { 'name': df_last.loc[i, 'fleet_name'], 'ships': {} }
        for ship_size in df_last.columns[2:]:
            if (num:=int(df_last.loc[i, ship_size])) > 0:
                fleet['ships'][ship_size_loc[ship_size]] = num
        fleets.append(fleet)

    env.globals['fleets'] = fleets


def compile_military_history(env: Environment, assets_path: str, data_path: str, output_path: str):
    print("编译军事史...", end=' ')
    stdout.flush()

    dir_path = prepare_output(output_path, "军事史")
    list_fleets(env, assets_path, data_path)

    print("完成")
    stdout.flush()
