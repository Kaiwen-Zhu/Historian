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
    
    with open(path_join(assets_path, 'entities', 'ship_size_localisation.json'), 
              encoding='utf-8') as f:
        ship_size_loc = json_load(f)
    
    fleets = []
    for i in range(len(df_last)):
        fleet = { 'name': df_last.loc[i, 'fleet_name'], 'ships': {} }
        for ship_size in df_last.columns[2:]:
            if (num:=int(df_last.loc[i, ship_size])) > 0:
                fleet['ships'][ship_size_loc[ship_size]] = num
        fleets.append(fleet)

    env.globals['fleets'] = fleets


def plot_naval_size_capacity(env: Environment, data_path: str, dir_path: str):
    df = pd.read_csv(path_join(data_path, 'naval_size_capacity.csv'), index_col=0, sep=';')

    dates = df["date"].apply(lambda date: date[:-3]).tolist()

    naval_size_capacity_config = {
        'title': "海军规模与容量", 'x': dates, 
        'data': [{
            'name': '海军规模', 'data': df['naval_size'].tolist()
        }, {
            'name': '海军容量', 'data': df['naval_capacity'].tolist()
        }], 
        'colors': ['#000080', '#408000']
    }

    render_page(env, 'charts/line_chart.html', dir_path, '海军规模与容量.html', 
                config=naval_size_capacity_config)
    

def plot_war(env: Environment, assets_path: str, data_path: str, dir_path: str):
    with open(path_join(data_path, 'wars.json'), encoding='utf-8') as f:
        wars: dict = json_load(f)
    with open(path_join(assets_path, 'entities', 'war_goal_localisation.json'), 
              encoding='utf-8') as f:
        war_goal_loc: dict = json_load(f)
    with open(path_join(data_path, 'country_name_dict.json'), encoding='utf-8') as f:
        country_name_dict: dict = json_load(f)

    # 键为国家 ID，值为我国与该国参与的战争列表
    war_participants = {}
    for war_info in wars.values():
        attackers_set = set(war_info['attackers'])

        # 本地化 (暂不本地化国家)
        if war_info['defender_wg']:
            war_info['defender_wg'] = war_goal_loc["war_goal_"+war_info['defender_wg']]
        if war_info['result']:
            if isinstance(war_info['result'], list):
                winner = war_info['result'][1]
                if winner == war_info['main_attacker'] and '0' in attackers_set or \
                   winner == war_info['main_defender'] and '0' not in attackers_set:
                    war_info['result'] = "我方胜利"
                else:
                    war_info['result'] = "我方战败"
            elif war_info['result'] == 'status_quo':
                war_info['result'] = "维持现状"
            elif war_info['result'] == 'forced_status_quo':
                war_info['result'] = "被迫维持现状"

        war_info['attacker_wg'] = war_goal_loc["war_goal_"+war_info['attacker_wg']]
        # war_info['main_attacker'] = country_name_dict[war_info['main_attacker']]
        # war_info['main_defender'] = country_name_dict[war_info['main_defender']]
        # war_info['attackers'] = [country_name_dict[attacker] for attacker in war_info['attackers']]
        # war_info['defenders'] = [country_name_dict[defender] for defender in war_info['defenders']]

        # 向 war_participants 中添加战争
        if '0' in attackers_set:
            this_enemies = war_info['defenders']
            this_allies = war_info['attackers']
        else:
            this_enemies = war_info['attackers']
            this_allies = war_info['defenders']
        for enemy in this_enemies:
            war_info_copy = war_info.copy()
            war_info_copy['side'] = '敌方'
            war_participants[enemy] = war_participants.get(enemy, []) + [war_info_copy]
        for ally in this_allies:
            if ally == '0':
                continue
            war_info_copy = war_info.copy()
            war_info_copy['side'] = '友方'
            war_participants[ally] = war_participants.get(ally, []) + [war_info_copy]

    # 计算在柱状图中的长度
    for country_wars in war_participants.values():
        prev_timestamp = 0
        for i, war in enumerate(country_wars):
            country_wars[i]['placeholder_length'] = time2stamp(war['start_date']) - prev_timestamp
            end_date = war['end_date'] if war['end_date'] else env.globals['end_date']
            country_wars[i]['war_length'] = time2stamp(end_date) - time2stamp(war['start_date'])
            prev_timestamp = time2stamp(end_date)
            if country_wars[i]['end_date'] is None:
                country_wars[i]['end_date'] = "-"
                country_wars[i]['result'] = "-"
    
    # 将 war_participants 转为键值对的列表，根据进入战争的时间排序
    war_participants = sorted(war_participants.items(), 
                              key=lambda t: t[1][0]['placeholder_length'])
    countries = [country_name_dict[country] for country, _ in war_participants]

    # 从 war_participants 中整理出数据
    num_war_participants = len(war_participants)
    war_data = []
    for i, (country, country_wars) in enumerate(war_participants):
        for war in country_wars:
            # 填入占位块
            this_data = [0] * num_war_participants
            this_data[i] = war['placeholder_length']
            war_data.append({'data': this_data})
            del war['placeholder_length']
            
            # 填入该战争
            this_data = [0] * num_war_participants
            this_data[i] = war['war_length']
            war['data'] = this_data
            del war['war_length']
            # 本地化，并从双方成员中删除领导者
            war['other_attackers'] = [country_name_dict[attacker] 
                for attacker in war['attackers'] if attacker != war['main_attacker']]
            war['other_defenders'] = [country_name_dict[defender] 
                for defender in war['defenders'] if defender != war['main_defender']]
            war['main_attacker'] = country_name_dict[war['main_attacker']]
            war['main_defender'] = country_name_dict[war['main_defender']]
            del war['attackers'], war['defenders']
            war_data.append(war)
    
    render_page(env, 'charts/wars.html', dir_path, '战争.html', 
                config={"war_data": war_data, "countries": countries})


def compile_military_history(env: Environment, assets_path: str, data_path: str, output_path: str):
    print("编译军事史...", end=' ')
    stdout.flush()

    dir_path = prepare_output(output_path, "军事史")
    list_fleets(env, assets_path, data_path)
    plot_naval_size_capacity(env, data_path, dir_path)
    plot_war(env, assets_path, data_path, dir_path)

    print("完成")
    stdout.flush()
