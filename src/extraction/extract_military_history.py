from sys import stdout
import pandas as pd
from os.path import join as path_join, exists as path_exists
from json import load as json_load, dump as json_dump
from .utils import *


def extract_fleet(game_log, data_path):
    """Extracts organization of navy."""   
     
    # data中的每项为 [date, fleet_name, *ship_sizes]
    data = extract_info(game_log, "(?<=HIS_FLEET:).*")
    warning = extract_info(game_log, "(?<=HIS_MILITARY_SHIP_WARNING:UNKNOWN_MILITARY_SHIP_SIZE,).*")
    if warning:
        unknown_ship_sizes = set(ship[0] for ship in warning)
        unknown_ship_sizes = ','.join(list(unknown_ship_sizes))
        print()
        print(f"\033[93m警告: 未知军舰类型: {unknown_ship_sizes}\033[0m")
    
    if data:
        ship_sizes = ['corvette', 'frigate', 'destroyer', 'cruiser', 'battleship', 'titan', 'colossus', 'juggernaut', 'small_ship_fallen_empire', 'large_ship_fallen_empire', 'pirate_corvette', 'pirate_destroyer', 'galleon', 'psionic_avatar', 'space_amoeba', 'crisis_corvette', 'crisis_destroyer', 'crisis_cruiser', 'star_eater', 'caravaneer_destroyer_01', 'caravaneer_cruiser_01', 'graygoo_interdictor', 'graygoo_mothership', 'npc_warship_01', 'toxic_god', 'payback_warship']
        new_df = pd.DataFrame(columns = ["date", "fleet_name"] + ship_sizes)
        for row in data:
            new_df.loc[len(new_df.index)] = row

        merge_and_save_df(data_path, 'fleets.csv', new_df)


def extract_naval_size_capacity(game_log, data_path):
    # data中的每项为 [date, naval_size, naval_capacity]
    data = extract_info(game_log, "(?<=HIS_NAVAL_SIZE_CAPACITY:).*")
    
    if data:
        new_df = pd.DataFrame(columns = ["date", "naval_size", "naval_capacity"])
        for row in data:
            new_df.loc[len(new_df.index)] = row

        merge_and_save_df(data_path, 'naval_size_capacity.csv', new_df)


def extract_war(game_log, data_path):
    """Extracts war history."""

    wars = {}
    if path_exists(path_join(data_path, 'wars.json')):
        with open(path_join(data_path, 'wars.json'), encoding='utf-8') as f:
            wars = json_load(f)
    
    # data_start 中的每项为 [date, war_id, war_name, main attacker, main defender]
    data_start = extract_info(game_log, "(?<=HIS_WAR_START:).*")

    # 更新战争开始时记录的信息 (ID，名称，开始日期，进攻方领导者与成员与战争目标，防守方领导者与成员)
    for start_date, war_id, war_name, main_attacker, main_defender in data_start:
        attackers = extract_info(game_log, f"(?<=HIS_WAR_START_ATTACKER:{war_id},).*")
        defenders = extract_info(game_log, f"(?<=HIS_WAR_START_DEFENDER:{war_id},).*")
        attacker_wg = extract_info(game_log, f"(?<=HIS_WAR_GOAL:{war_id},{main_attacker},).*")
        war_info = {
            'name': war_name, 'start_date': start_date,
            'main_attacker': main_attacker, 
            'attackers': [id[0] for id in attackers if id[0]],  # TO FIX: 可能会有空项
            'attacker_wg': attacker_wg[0][0],
            'main_defender': main_defender,
            'defenders':  [id[0] for id in defenders if id[0]],  # TO FIX: 可能会有空项
            'defender_wg': '',
            'end_date': '',
            'result': ''
        }
        if war_id not in wars:
            wars[war_id] = war_info
        else:
            wars[war_id].update(war_info)

    # 更新其它战争信息：防守方战争目标，结束日期，结果（决出胜负/维持现状/被迫维持现状）
    for war_id, war_info in wars.items():
        main_attacker, main_defender = war_info['main_attacker'], war_info['main_defender']
        # 提取防守方战争目标
        defender_wg = extract_info(game_log, f"(?<=HIS_WAR_GOAL:{war_id},{main_defender},).*")
        # 提取结束日期（决出胜负），胜方领导者
        won_info = extract_info(game_log, f"(?<=HIS_WAR_WON:{war_id},).*")
        # 提取结束日期（维持现状）
        status_quo_info = extract_info(game_log, f"(?<=HIS_WAR_STATUS_QUO:{war_id},).*")
        # 提取结束日期（被迫维持现状）
        status_quo_forced_info = extract_info(game_log, f"(?<=HIS_WAR_STATUS_QUO_FORCED:{war_id},).*")

        if defender_wg:
            war_info['defender_wg'] = defender_wg[0][0]
        if won_info:
            war_info['end_date'] = won_info[0][0]
            war_info['result'] = ('won', won_info[0][1])
        elif status_quo_info:
            war_info['end_date'] = status_quo_info[0][0]
            war_info['result'] = 'status_quo'
        elif status_quo_forced_info:
            war_info['end_date'] = status_quo_forced_info[0][0]
            war_info['result'] = 'status_quo_forced'

        if not war_info['end_date']:
            # 检查是否为全面战争且已结束
            opinions = pd.read_csv(path_join(data_path, 'opinions.csv'), sep=';', index_col=0)
            if '0' in war_info['attackers']:
                enemies = war_info['defenders']
                our_leader = war_info['main_attacker']
            else:
                enemies = war_info['attackers']
                our_leader = war_info['main_defender']
            enemies_cols = opinions[[f'our_opinion_{enemy}' for enemy in enemies]]
            if len(enemies_cols.columns):  # TO FIX: 可能为空
                null_rows = enemies_cols.isnull().all(axis=1)
                if null_rows.iloc[-1]:
                    # 敌人已全部灭亡，战争结束
                    for i in range(len(null_rows)-1, -1, -1):
                        if not null_rows.iloc[i]:
                            first_nan = i + 1
                            break
                    war_info['end_date'] = opinions.loc[first_nan]['date']
                    war_info['result'] = ('won', our_leader)

        wars[war_id] = war_info

    with open(path_join(data_path, 'wars.json'), 'w', encoding='utf-8') as f:
        json_dump(wars, f, ensure_ascii=False, indent=4)
            

def extract_military_history(game_log, data_path):
    print("提取军事史...", end=' ')
    stdout.flush()
    
    extract_fleet(game_log, data_path)  # 提取海军组织
    extract_naval_size_capacity(game_log, data_path)  # 提取海军规模与舰队容量
    extract_war(game_log, data_path)  # 提取战争信息
        
    print("完成")
    stdout.flush()
    