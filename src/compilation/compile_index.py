from sys import stdout
from shutil import copyfile
from jinja2 import Environment
from .utils import *
        

def compile_index(env: Environment, assets_path: str, output_path: str):
    print("编译索引...", end=' ')
    stdout.flush()

    # 添加 CSS 样式
    css_src_path = path_join(assets_path, 'css', 'general.css')
    css_dst_path = path_join(output_path, 'css', 'general.css')
    if not path_exists(path_join(output_path, 'css')):
        mkdir(path_join(output_path, 'css'))
    copyfile(css_src_path, css_dst_path)

    render_page(env, 'index.html', output_path, '{}史.html'.format(env.globals['name']))
    
    print("完成")
    stdout.flush()
