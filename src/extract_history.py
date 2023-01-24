from os import path
from extract_basics import extract_basics
from extract_economic_history import extract_economic_history
from extract_demographic_history import extract_demographic_history
from extract_diplomatic_history import extract_diplomatic_history
from extract_military_history import extract_military_history


def main():
    # data_dir = input("请输入存储数据的文件夹名称：")
    root_path = path.dirname(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))  # Stellaris 目录路径
    data_dir = "data"  # 存储数据的目录名称
    data_path = path.join(root_path, "mod", "Historian", data_dir)
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