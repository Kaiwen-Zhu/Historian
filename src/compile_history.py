from os import mkdir
from os.path import join as path_join, dirname, abspath, exists as path_exists
import argparse
from jinja2 import Environment, FileSystemLoader
from compilation import *


def main():
    parser = argparse.ArgumentParser(description='编译史书')
    parser.add_argument('--output', '-o', help='输出文件夹名称', type=str, default='MemoryGrain')
    args = parser.parse_args()
    
    Historian_path = dirname(dirname(abspath(__file__)))  # Historian 目录路径
    data_path = path_join(Historian_path, args.output, "data")
    output_path = path_join(Historian_path, args.output, "output")
    assets_path = path_join(Historian_path, "src", "assets")

    assert path_exists(data_path)
    if not path_exists(output_path):
        mkdir(output_path)

    env = Environment(loader=FileSystemLoader(path_join(Historian_path, 'src', 'templates')))

    compile_overview(env, assets_path, data_path, output_path)
    compile_economic_history(env, assets_path, data_path, output_path)
    compile_demographic_history(env, data_path, output_path)
    compile_scientific_history(env, assets_path, data_path, output_path)
    # compile_diplomatic_history(env, data_path, output_path)

    compile_index(env, assets_path, output_path)

    print(f"史书已被保存到 {path_join(output_path, env.globals['name']+'史.html')}。")


if __name__ == '__main__':
    main()
