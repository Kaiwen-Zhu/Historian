import re
from pathlib import Path
from sys import stdout
from json import load as json_load, dump as json_dump


def extract_basics(game_log: str, data_path: Path):
    print("提取基本信息...", end=' ')
    stdout.flush()

    file_path = data_path / 'basics.json'

    if not file_path.exists():
        basics_dict = {}
        basics_pat = re.compile('(?<=HIS_BASICS:).+')
        info = basics_pat.search(game_log)
        info = info.group().split(',')
        basics_dict['origin'] = info[0]
        basics_dict['home_world'] = info[1]
        basics_dict['home_world_class'] = info[2]
        basics_dict['home_system'] = info[3]
        basics_dict['species'] = info[4]

    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            basics_dict = json_load(f) 

    # extract the last day
    date_pat = re.compile('(?<=HIS_RESERVES_INCOME:)\d{4}.\d{2}.\d{2}(?=,)')
    dates = date_pat.findall(game_log)
    if dates:
        basics_dict['end_date'] = dates[-1]

    # extract name, government name, and personality
    ngp_pat = re.compile('(?<=HIS_ETHOS:).+')
    info = ngp_pat.findall(game_log)
    if info:
        info = info[0].split(',')
        last_date = info[0]
        basics_dict['name'] = info[1]
        basics_dict['government_name'] = info[2]
        basics_dict['personality'] = info[3]

    # extract ethics
    ethics_pat = re.compile('(?<=HIS_ETHIC:).+')
    ethics = ethics_pat.findall(game_log)
    if ethics:
        ethics = filter(lambda x: x.startswith(last_date), ethics)
        ethics = list(map(lambda x: x.split(',')[1], ethics))
        basics_dict['ethics'] = ethics

    with open(file_path, 'w', encoding='utf-8') as f:
        json_dump(basics_dict, f, ensure_ascii=False, indent=4)
        
    print("完成")
    stdout.flush()

    return basics_dict['name']
