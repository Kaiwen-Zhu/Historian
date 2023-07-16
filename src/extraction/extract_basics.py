import re
from os import path
from sys import stdout
from json import load as json_load, dump as json_dump


def extract_basics(game_log, data_path):
    print("Extracting basics ...")
    stdout.flush()

    file_path = path.join(data_path, 'basics.json')

    if not path.exists(file_path):
        basics_dict = {}
        basics_pat = re.compile('(?<=HIS_BASICS:).+')
        info = basics_pat.search(game_log)
        info = info.group().split(',')
        basics_dict['name'] = info[0]
        basics_dict['government_name'] = info[1]
        basics_dict['personality'] = info[2]
        basics_dict['origin'] = info[3]
        basics_dict['home_world'] = info[4]
        basics_dict['home_world_class'] = info[5]
        basics_dict['home_system'] = info[6]
        basics_dict['species'] = info[7]

    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            basics_dict = json_load(f) 

    # extract the last day
    date_pat = re.compile('(?<=HIS_RESERVES_INCOME:)\d{4}.\d{2}.\d{2}(?=,)')
    dates = date_pat.findall(game_log)
    if dates:
        basics_dict['end_date'] = dates[-1]

    with open(path.join(data_path, 'basics.json'), 'w', encoding='utf-8') as f:
        json_dump(basics_dict, f, ensure_ascii=False)
        
    print("Done!")
    stdout.flush()
