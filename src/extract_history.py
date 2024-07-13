from pathlib import Path
from sys import stdout
import argparse
from extraction import *


def main():
    parser = argparse.ArgumentParser(description='Extract the history from the game log.')
    parser.add_argument('--output', '-o', help='the output directory', type=str, default='MemoryGrain')
    args = parser.parse_args()

    root_path = Path().resolve().parents[3]  # Stellaris 目录路径
    data_path: Path = root_path / "mod" / "Historian" / args.output / "data"
    data_path.mkdir(parents=True, exist_ok=True)
    
    print("读取日志...", end=' ')
    stdout.flush()
    with open(root_path / "logs" / "game.log", 'r', encoding='utf-8') as f:
        game_log = f.read()
    print("完成")
    stdout.flush()
    
    our_name = extract_basics(game_log, data_path)
    extract_economic_history(game_log, data_path)
    extract_demographic_history(game_log, data_path)
    extract_scientific_history(game_log, data_path)
    extract_diplomatic_history(game_log, data_path, our_name)
    extract_military_history(game_log, data_path)

    print(f"数据已被提取到 {data_path}。")


if __name__ == '__main__':
    main()
