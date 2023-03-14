from os import path, mkdir
from extraction import *


def main():
    root_path = path.dirname(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))  # Stellaris 目录路径
    # HIS_dir = input("请输入存储数据与输出的文件夹名称：")
    HIS_dir = "旋桌骑士高阶领主国"  # 存储数据目录与输出目录的目录名称
    # HIS_dir += "HIS"
    HIS_path = path.join(root_path, "mod", "Historian", HIS_dir)
    data_path = path.join(HIS_path, "data")

    if not path.exists(HIS_path):
        mkdir(HIS_path)
        mkdir(data_path)
    
    with open(path.join(root_path, "logs", "game.log"), 'r', encoding='utf-8') as f:
        game_log = f.read()
    
    extract_basics(game_log, data_path)
    extract_economic_history(game_log, data_path)
    extract_demographic_history(game_log, data_path)
    extract_diplomatic_history(game_log, data_path)
    extract_military_history(game_log, data_path)

    print("Successfully extracted the history!")
    # input("Press any key to close the window.")


if __name__ == '__main__':
    main()