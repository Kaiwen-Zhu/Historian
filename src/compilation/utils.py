from os import mkdir
from os.path import exists as path_exists, join as path_join
from shutil import rmtree
from jinja2 import Environment


def prepare_output(output_path: str, title: str) -> str:
    """Prepares the output directory and returns its path."""
    
    dir_path = path_join(output_path, title)
    if path_exists(dir_path):
        rmtree(dir_path)
    mkdir(dir_path)

    return dir_path


def render_page(env: Environment, template_name: str, output_path: str, page_name: str, config: dict = None):
    """Renders the page from the template and writes it to the output directory."""    
    
    index = env.get_template(template_name)
    page = index.render(config=config)
    file_path = path_join(output_path, page_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(page)
