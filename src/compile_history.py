from pathlib import Path
import argparse
from jinja2 import Environment, FileSystemLoader
from compilation import *


def main():
    parser = argparse.ArgumentParser(description='编译史书')
    parser.add_argument('--output', '-o', help='输出文件夹名称', type=str, default='MemoryGrain')
    args = parser.parse_args()
    
    Historian_path = Path(__file__).resolve().parents[1]  # Historian 目录路径
    data_path: Path = Historian_path / args.output / "data"
    output_path: Path = Historian_path / args.output / "output"
    assets_path: Path = Historian_path / "src" / "assets"

    assert data_path.exists()
    output_path.mkdir(exist_ok=True)

    env = Environment(loader=FileSystemLoader(Historian_path / 'src' /'templates'))

    compile_overview(env, assets_path, data_path, output_path)
    compile_economic_history(env, data_path, output_path)
    compile_demographic_history(env, data_path, output_path)
    compile_scientific_history(env, assets_path, data_path, output_path)
    compile_diplomatic_history(env, data_path, output_path)
    compile_military_history(env, assets_path, data_path, output_path)

    compile_index(env, output_path)

    print(f"史书已被保存为 {output_path / (env.globals['name']+'史.html')}。")


if __name__ == '__main__':
    main()
