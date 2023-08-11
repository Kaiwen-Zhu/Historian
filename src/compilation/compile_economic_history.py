from sys import stdout
from os.path import join as path_join
import pandas as pd
from jinja2 import Environment
from .utils import *
        

def plot_resources_reserves_income(env: Environment, data_dir: str, dir_path: str):
    df = pd.read_csv(path_join(data_dir, 'resources.csv'), index_col=0, sep=';')

    dates = df["date"].apply(lambda date: date[:-3]).tolist()
    resources = ['energy', 'minerals', 'food', 'consumer_goods', 'alloys',
            'volatile_motes', 'exotic_gases', 'rare_crystals', 'living_metal', 'zro',
            'dark_matter', 'nanites', 'minor_artifacts']
    colors = ['#f1e916', '#e95350', '#71bb50', '#d2754c', '#7e3e9e',
            '#973d2f', '#027a2e', '#cc8602', '#647676', '#567fce',
            '#1a212c', '#b1bfb3', '#8958a7']
    resources_label = ['能量币', '矿物', '食物', '消费品', '合金', '易爆微粒', '异星天然气',
        '稀有水晶', '活体金属', '泽珞', '暗物质', '纳米机器人', '稀有文物']
    
    resources_type_map = [
        ('基础资源', range(3)), ('工业资源', range(3,5)), ('稀有资源', range(5,13))
    ]
    
    # 绘制一类资源的储量和月收入折线图
    def plot_one_type_resources(resources_category):
        # resources_category: 0-基础资源，1-工业资源，2-稀有资源
        resources_category_name, resources_idx_range = resources_type_map[resources_category]
        color_list = [colors[i] for i in resources_idx_range]

        reserves_config = {
            'title': f"{resources_category_name}储量", 'x': dates, 'data': [], 
            'colors': color_list
        }
        income_config = {
            'title': f"{resources_category_name}月收入", 'x': dates, 'data': [], 
            'colors': color_list
        }

        for resource_idx in resources_idx_range:
            resource_name = resources[resource_idx]
            resource_name_in_label = resources_label[resource_idx]
            reserves_config['data'].append({
                'name': resource_name_in_label, 'data': df[f'{resource_name}_reserves'].tolist()
            })
            income_config['data'].append({
                'name': resource_name_in_label, 'data': df[f'{resource_name}_income'].tolist()
            })
        
        render_page(env, 'line_chart.html', dir_path, f'{resources_category_name}储量.html', 
                    config=reserves_config)
        render_page(env, 'line_chart.html', dir_path, f'{resources_category_name}月收入.html', 
                    config=income_config)


    # 绘制各资源储量/收入折线图
    for resources_category in range(3):
        plot_one_type_resources(resources_category)


def compile_economic_history(env: Environment, assets_path: str, data_path: str, output_path: str):
    print("编译经济史...", end=' ')
    stdout.flush()

    dir_path = prepare_output(output_path, "经济史")

    plot_resources_reserves_income(env, data_path, dir_path)

    print("完成")
    stdout.flush()
