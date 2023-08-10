from sys import stdout
from os.path import join as path_join
import pandas as pd
from shutil import copyfile
from jinja2 import Environment
from .utils import *


def plot_points_income(env: Environment, data_dir: str, dir_path: str):
    df = pd.read_csv(path_join(data_dir, 'resources.csv'), index_col=0, sep=';')

    dates = df["date"].apply(lambda date: date[:-3]).tolist()
    env.globals['resource_income_dates'] = dates
    
    for name in ('physics_research', 'society_research', 'engineering_research'):
        val = df[f'{name}_income'].tolist()
        env.globals[name] = list(zip(dates, val))

    render_page(env, 'research_points_income.html', dir_path, '研究点数月收入.html')


def compile_scientific_history(env: Environment, assets_path: str, data_path: str, output_path: str):
    print("编译科技史...", end=' ')
    stdout.flush()

    dir_path = prepare_output(output_path, "科技史")
    plot_points_income(env, data_path, dir_path)

    # render_page(env, 'scientific_history.html', dir_path, '科技史.html')

    print("完成")
    stdout.flush()
