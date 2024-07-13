from sys import stdout
import pandas as pd
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
    df = pd.concat([df, pd.DataFrame({"date": new_dates, "species_name": species_name, "num_pop": 0})])

    df.sort_values(by="date", inplace=True)
    df.reset_index(inplace=True, drop=True) 
    df['num_pop'].interpolate(inplace=True)
    return df


def plot_pop_size(env, data_path, dir_path):
    df_species = pd.read_csv(data_path / 'species_pop_size.csv', index_col=0, sep=';')  

    dates = df_species['date'].drop_duplicates(keep='first')
    dates.reset_index(inplace=True, drop=True)
    species_names = df_species['species_name'].drop_duplicates(keep='first').values.tolist()  # 按出现顺序排列

    # # 统计各物种最大数量
    # max_sizes = []  # 各物种最大数量
    # for species in set(df_species['species_name']):
    #     max_size = (species, df_species[df_species['species_name']==species]['num_pop'].max())
    #     if max_size[-1] == 0:
    #         df_species.drop(index=df_species[df_species['species_name']==species].index, inplace=True)
    #     else:
    #         max_sizes.append(max_size)
    # max_sizes.sort(key = lambda t: t[-1])

    pop_size_config = {
        'title': "人口规模", 'x': dates.apply(lambda date: date[:-3]).tolist(), 'data': []
    }
    
    for species in species_names:
        df_one_species = df_species[df_species['species_name']==species].copy()
        df_one_species = pad_vacant_year(df_one_species, species, dates)  # 将缺失的值补上 0
        
        # 可能有多个物种同名，需要合并
        nums = []
        for date in dates:
            nums.append(df_one_species[df_one_species['date']==date]['num_pop'].sum())
        assert len(dates) == len(nums)
        pop_size_config['data'].append({
            'name': species, 'data': nums
        })
    
    render_page(env, 'charts/pop_size.html', dir_path, '人口规模.html', config=pop_size_config)
                    

def plot_unity(env, data_path, dir_path):
    df = pd.read_csv(data_path / 'resources.csv', index_col=0, sep=';')

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

    render_page(env, 'charts/line_chart.html', dir_path, '凝聚力储量.html', config=unity_reserves_config)
    render_page(env, 'charts/line_chart.html', dir_path, '凝聚力月收入.html', config=unity_income_config)


def compile_demographic_history(env: Environment, data_path: Path, output_path: Path):
    print("编译人口史...", end=' ')
    stdout.flush()

    dir_path = prepare_output(output_path, "人口史")

    plot_pop_size(env, data_path, dir_path)
    plot_unity(env, data_path, dir_path)

    print("完成")
    stdout.flush()
