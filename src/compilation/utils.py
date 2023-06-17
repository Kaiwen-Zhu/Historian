import matplotlib.pyplot as plt
from os import path, mkdir
from shutil import rmtree


def prepare_compile_section(lang: str, output_path: str, en_title: str, zh_title: str) -> str:
    """Prepares the output directory and returns its path."""
    
    if lang == 'en':
        dir_name = f'The {en_title} History'
    else:
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        dir_name = f'{zh_title}史'

    dir_path = path.join(output_path, dir_name)
    if path.exists(dir_path):
        rmtree(dir_path)
    mkdir(dir_path)

    return dir_path
