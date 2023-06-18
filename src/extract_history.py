from os import path, mkdir
from sys import stdout
import argparse
from extraction import *


def main():
    parser = argparse.ArgumentParser(description='Extract the history from the game log.')
    parser.add_argument('--output', '-o', help='the output directory', type=str, default='MemoryGrain')
    args = parser.parse_args()

    root_path = path.dirname(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))  # Stellaris 目录路径
    HIS_path = path.join(root_path, "mod", "Historian", args.output)
    data_path = path.join(HIS_path, "data")

    if not path.exists(HIS_path):
        mkdir(HIS_path)
        mkdir(data_path)
    
    print("Reading the log ...")
    stdout.flush()
    with open(path.join(root_path, "logs", "game.log"), 'r', encoding='utf-8') as f:
        game_log = f.read()
    print("Done!")
    stdout.flush()
    
    extract_basics(game_log, data_path)
    extract_economic_history(game_log, data_path)
    extract_demographic_history(game_log, data_path)
    extract_diplomatic_history(game_log, data_path)
    # extract_military_history(game_log, data_path)

    print("Successfully extracted the history!")


if __name__ == '__main__':
    main()
