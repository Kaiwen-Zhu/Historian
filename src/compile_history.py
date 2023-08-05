from os import path, mkdir
import argparse
from jinja2 import Environment, FileSystemLoader
from compilation import *


def main():
    parser = argparse.ArgumentParser(description='编译史书')
    parser.add_argument('--output', '-o', help='输出文件夹名称', type=str, default='MemoryGrain')
    args = parser.parse_args()
    
    Historian_path = path.dirname(path.dirname(path.abspath(__file__)))  # Historian 目录路径
    data_path = path.join(Historian_path, args.output, "data")
    output_path = path.join(Historian_path, args.output, "output")
    assets_path = path.join(Historian_path, "src", "assets")

    assert path.exists(data_path)
    if not path.exists(output_path):
        mkdir(output_path)

    env = Environment(loader=FileSystemLoader(path.join(Historian_path, 'src', 'templates')))

    compile_index(env, assets_path, data_path, output_path)
    # compile_economic_history(env, data_path, output_path)
    # compile_demographic_history(env, data_path, output_path)
    compile_scientific_history(env, assets_path, data_path, output_path)
    # compile_diplomatic_history(env, data_path, output_path)

    print("编译完成")


if __name__ == '__main__':
    main()
