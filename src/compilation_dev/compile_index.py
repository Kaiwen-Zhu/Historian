from sys import stdout
from os.path import join as path_join
from json import load as json_load
from shutil import copyfile
from jinja2 import Environment
from .utils import *
        

def compile_index(env: Environment, assets_path: str, data_path: str, output_path: str):
    print("编译基础信息...", end=' ')
    stdout.flush()

    dir_path = prepare_output(output_path, "基本信息")

    loc = {
            "FanaticEgalitarian": "极端平等主义",
            "FanaticAuthoritarian": "极端威权主义",
            "Egalitarian": "平等主义",
            "Authoritarian": "威权主义",

            "FanaticPacifist": "极端和平主义",
            "FanaticMilitarist": "极端军国主义",
            "Pacifist": "和平主义",
            "Militarist": "军国主义",

            "FanaticXenophile": "极端亲外主义",
            "FanaticXenophobe": "极端排外主义",
            "Xenophile": "亲外主义",
            "Xenophobe": "排外主义",

            "FanaticMaterialist": "极端唯物主义",
            "FanaticSpiritualist": "极端唯心主义",
            "Materialist": "唯物主义",
            "Spiritualist": "唯心主义",

            "GestaltConsciousness": "格式塔意识"
        }

    with open(path_join(data_path, 'basics.json'), encoding='utf-8') as f:
        basics = json_load(f)

    ethic_icon_src_path = path_join(assets_path, 'ethics', '{}.webp')
    origin_icon_src_path = path_join(assets_path, 'origins', '{}.webp')
    assets_dst_path = path_join(dir_path, '{}.webp')
    page_src_path = path_join('.', '基本信息', '{}.webp')

    for ethic in basics['ethics']:
        copyfile(ethic_icon_src_path.format(ethic), assets_dst_path.format(ethic))
    copyfile(origin_icon_src_path.format(basics['origin']), assets_dst_path.format(basics['origin']))

    basics['ethics'] = list(map(lambda e: (loc[e], page_src_path.format(e)), basics['ethics']))
    basics['origin'] = (basics['origin'], page_src_path.format(basics['origin']))
    env.globals.update(basics)

    render_page(env, 'index.html', output_path, '{}史.html'.format(env.globals['name']))
    
    print("完成")
    stdout.flush()
