from sys import stdout
from os.path import join as path_join
import pandas as pd
from shutil import copyfile
from jinja2 import Environment
from .utils import *


def pad_vacant_year(df, species_name, all_dates):        
    """Makes the date complete by setting `num_pop` as 0 and fills `nan` by interpolation.""" 

    # 插入中间缺失的元组
    prev_year = int(df.iloc[0]['date'][:4])
    for idx, row in df.iterrows():
        this_year = int(row['date'][:4])
        if this_year > prev_year + 1:
            for vacant_year in range(prev_year+1, this_year):
                df = pd.concat([df, pd.DataFrame(
                    {"date": [f"{vacant_year}.01.15"], "species_name": species_name, "num_pop": 0})])
        prev_year = this_year
    
    # 插入头尾缺失的元组
    this_dates = df['date'].values
    new_dates = []
    for date in all_dates:
        if date not in this_dates:
            new_dates.append(date)
        else:
            break
    for date in all_dates[::-1]:
        if date not in this_dates:
            new_dates.append(date)
        else:
            break
    df = pd.concat([df, pd.DataFrame(
                {"date": new_dates, "species_name": species_name, "num_pop": 0})])

    df.sort_values(by="date", inplace=True)
    df.reset_index(inplace=True, drop=True) 
    df['num_pop'].interpolate(inplace=True)
    return df


def plot_pop_size(data_path, dir_path, lang):
    """Plots the line chart of population size of species."""    

    if lang == 'en':
        file_name = 'Population Size'
        others_label = "Other {} species"
    else:
        file_name = '人口数量'
        others_label = "其它{}个物种"


    df_species = pd.read_csv(path_join(data_path, 'species_pop_size.csv'), index_col=0, sep=';')  
    all_dates = df_species['date'].drop_duplicates(keep='first')
    all_dates.reset_index(inplace=True, drop=True)


    # 统计各物种最大数量，仅对前 `MAX_SPECIES_NUM` 个物种单独绘制
    MAX_SPECIES_NUM = 19
    max_sizes = []  # 各物种最大数量
    for species in set(df_species['species_name']):
        max_size = (species, df_species[df_species['species_name']==species]['num_pop'].max())
        if max_size[-1] == 0:
            df_species.drop(index=df_species[df_species['species_name']==species].index, inplace=True)
        else:
            max_sizes.append(max_size)
    max_sizes.sort(key = lambda t: t[-1])
    others = set(t[0] for t in max_sizes[:-MAX_SPECIES_NUM])  # `others` 中的物种不单独绘制
    num_in_others = len(others)

    # 按出现顺序统计物种名称
    species_names = df_species['species_name'].drop_duplicates(keep='first').values.tolist()
    
    pop_sizes = []
    other_num = pd.DataFrame(columns=["date", "species_name", "num_pop"])  # 记录其它物种的人口数量之和
    for species in species_names:
        df_one_species = df_species[df_species['species_name']==species].copy()
        df_one_species = pad_vacant_year(df_one_species, species, all_dates)  # 将中间缺失的值补上 0
        if species not in others:
            # 可能有多个物种同名，需要合并
            nums = []
            for date in all_dates:
                nums.append(df_one_species[df_one_species['date']==date]['num_pop'].sum())
            assert len(all_dates) == len(nums)
            pop_sizes.append(nums)
                    
    # plt.stackplot(all_dates, pop_sizes, colors=colors)


def plot_unity(env, data_path, dir_path):
    df = pd.read_csv(path_join(data_path, 'resources.csv'), index_col=0, sep=';')

    dates = df["date"].apply(lambda date: date[:-3]).tolist()

    unity_reserves_config = {
        'title': "凝聚力储量", 'x': dates, 
        'data': [{
            'name': '凝聚力', 'data': df['unity_reserves'].tolist()
        }], 
        'colors': ['#51aca6']
    }
    unity_income_config = {
        'title': "凝聚力月收入", 'x': dates, 
        'data': [{
            'name': '凝聚力', 'data': df['unity_income'].tolist()
        }],
        'colors': ['#51aca6']
    }

    render_page(env, 'line_chart.html', dir_path, '凝聚力储量.html', config=unity_reserves_config)
    render_page(env, 'line_chart.html', dir_path, '凝聚力月收入.html', config=unity_income_config)


def compile_demographic_history(env: Environment, data_path: str, output_path: str):
    print("编译人口史...", end=' ')
    stdout.flush()

    dir_path = prepare_output(output_path, "人口史")

    # plot_pop_size(env, data_path, dir_path)
    plot_unity(env, data_path, dir_path)

    print("完成")
    stdout.flush()
