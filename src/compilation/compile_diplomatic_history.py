from sys import stdout
from os.path import join as path_join, exists as path_exists
from json import load as json_load
import pandas as pd
from jinja2 import Environment
from .utils import *


def plot_opinions(env: Environment, data_path: str, dir_path: str, mapping: dict[str, str]):
    df = pd.read_csv(path_join(data_path, 'opinions.csv'), index_col=0, sep=';')

    df["date"] = df["date"].apply(lambda date: date[:-3])

    rel_config = {
        'title': "外交关系", 'x': df["date"].tolist(), 'data': []
    }

    for ind in range((len(df.columns)-1) // 2):
        country = mapping[df.columns[2*ind+1][12:]]  # 国家名称
        df_tmp = df[df[df.columns[2*ind+1]].notnull()]
        rel_config['data'].append({
            'name': country,
            'date': df_tmp["date"].tolist(),
            'our_opinion': df_tmp[df.columns[2*ind+1]].tolist(),
            'their_opinion': df_tmp[df.columns[2*ind+2]].tolist()
        })
    
    render_page(env, 'diplomatic_relationship.html', dir_path, '外交关系.html', config=rel_config)


def compile_diplomatic_history(env: Environment, data_path: str, output_path: str):
    if path_exists(path_join(data_path, 'opinions.csv')):
        print("编译外交史...", end=' ')
        stdout.flush()
        
        dir_path = prepare_output(output_path, "外交史")

        with open(path_join(data_path, 'mapping.json'), encoding='utf-8') as f:
            mapping = json_load(f)
    
        plot_opinions(env, data_path, dir_path, mapping)

        print("完成")
        stdout.flush()
