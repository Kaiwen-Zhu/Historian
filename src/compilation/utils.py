from pathlib import Path
from shutil import rmtree
from jinja2 import Environment


def prepare_output(output_path: Path, title: str) -> Path:
    """Prepares the output directory and returns its path."""
    
    dir_path = output_path / title
    if dir_path.exists():
        rmtree(dir_path)
    dir_path.mkdir()

    return dir_path


def render_page(env: Environment, template_name: str, output_path: Path, page_name: str, config: dict = None):
    """Renders the page from the template and writes it to the output directory."""    
    
    index = env.get_template(template_name)
    page = index.render(config=config)
    file_path = output_path / page_name
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(page)


def time2stamp(time: str) -> int:
    """Converts a time string to a timestamp (days passed since 2200)."""

    year, month, day = time.split(".")
    return (int(year) - 2200) * 360 + (int(month) - 1) * 30 + int(day)
