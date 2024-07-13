from sys import stdout
from jinja2 import Environment
from .utils import *
        

def compile_index(env: Environment, output_path: Path):
    print("编译索引...", end=' ')
    stdout.flush()

    render_page(env, 'index.html', output_path, '{}史.html'.format(env.globals['name']))
    
    print("完成")
    stdout.flush()
