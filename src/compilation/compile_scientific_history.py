from sys import stdout
from os import path
import matplotlib.pyplot as plt
import pandas as pd
from pylatex import NoEscape, Section, Subsection, Figure
from .utils import *


def plot_points_income(data_dir, dir_path, lang, name) -> str:
    """ Plots the line charts of monthly income of scientific points.
    """ 

    research = ['physics_research', 'society_research', 'engineering_research']
    colors = ['#359db6', '#53b977', '#df8c4c']

    if lang == 'en':
        file_name = f'The Monthly Income of Scientific Points of {name}.png'
        # title = 'The Monthly Income of Research Points'

    else:
        file_name = f'{name}研究点数月收入.png'
        research_zh = ['物理学研究', '社会学研究', '工程学研究']
        # title = '研究点数月收入'
    

    df = pd.read_csv(path.join(data_dir, 'resources.csv'), index_col=0, sep=';')

    # plt.title(title, fontsize=15)
    plt.figure(figsize=(8,4))
    for research_idx in range(3):
        research_name = research[research_idx]
        if lang == 'en':
            research_name_in_label = research[research_idx].replace('_', ' ').title()
        else:
            research_name_in_label = research_zh[research_idx]
        plt.plot(df["date"], df[f'{research_name}_income'], alpha = 0.8,
                            label = research_name_in_label, color = colors[research_idx])

    date_step = max(len(df) // 9, 1)  # 横轴相邻标签间隔的月数
    omitted = 6 if date_step > 60 else 3  # 为6则日期省略月、日，为3则省略日
    plt.xticks(ticks = range(0, len(df), date_step), 
            labels = df["date"][::date_step].apply(lambda date: date[:-omitted]), rotation = 30)
    plt.legend()

    pic_path = path.join(dir_path, file_name)
    plt.savefig(pic_path, dpi=500, bbox_inches='tight', pad_inches=0.02)
    plt.close()

    return pic_path


def add_pics_to_doc(doc, pic, lang):
    doc.append(NoEscape(R'\newpage'))

    if lang == 'en':
        section_name = 'Science'
        subsection1_name = 'The Monthly Income of Scientific Points'
    else:
        section_name = '科技'
        subsection1_name = '研究点数月收入'
        
    with doc.create(Section(section_name)):
        with doc.create(Subsection(subsection1_name)):
            with doc.create(Figure(position='H')) as pic_in_doc:
                pic_in_doc.add_image(pic, width='17cm')


def compile_scientific_history(doc, data_dir, output_path, lang, name):
    print("Compiling the scientific history ...")
    stdout.flush()

    dir_path = prepare_compile_section(name, lang, output_path, "Scientific", "科技")

    pic = plot_points_income(data_dir, dir_path, lang, name)
    add_pics_to_doc(doc, pic, lang)

    print("Done!")
    stdout.flush()