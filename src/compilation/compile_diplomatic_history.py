from sys import stdout
from os import path
import matplotlib.pyplot as plt
import pandas as pd
from pylatex import NoEscape, Section, Subsection, Figure
from typing import Tuple
from .utils import *
# from matplotlib.backends.backend_pdf import PdfPages

Color = Tuple[float]


def get_gradient_color(c1: Color, c2: Color, dis: float) -> Color:
    """Computes the color between `c1` and `c2` that is `dis` (in RGB) away from `c1`."""

    return tuple(min(1, c1[i] + round(dis * (c2[i]-c1[i]), 1)) for i in range(3))


def get_color(num: int, ls: str) -> Color:
    """Computes the color corresponding to the given number."""

    num *= 2 if ls != '-' else 1
    colors = [(1,0,0), (1, 0xd7/255, 0), (0,1,0)]
    thresholds = [-1000, 0, 1000]
    if num <= thresholds[0]:
        return colors[0]
    if num >= thresholds[-1]:
        return colors[-1]

    for ind in range(len(thresholds)-1):
        if num < thresholds[ind+1]:
            break
    dis = (num - thresholds[ind]) / (thresholds[ind+1] - thresholds[ind])
    return get_gradient_color(colors[ind], colors[ind+1], dis)


def plot_opinions(data_path, dir_path, lang) -> list[str]:
    """Plots the line chart of relationships and mutual opinions."""    

    pics = []  # 存储各图路径

    if lang == 'en':
        all_title = 'The Relationships with Other Countries'
        title = 'The Relationship with {}'

    else:
        all_title = '与各国关系'
        title = '与{}之间的关系'


    df = pd.read_csv(path.join(data_path, 'opinions.csv'), index_col=0, sep=';')

    # with PdfPages(path.join('..', output, filename)) as pdf:
    # 绘制与各国关系
    plt.figure(figsize=(9, 11))
    for ind in range((len(df.columns)-1) // 2):
        country = df.columns[2*ind+1][11:]  # 国家名称
        plt.plot(df["date"], df[df.columns[2*ind+1]] + df[df.columns[2*ind+2]], label=country, alpha=0.8)
    # plt.title(all_title, fontsize=15)
    date_step = max(len(df) // 9, 1)  # 横轴相邻标签间隔的月数
    omitted = 6 if date_step > 60 else 3  # 为6则日期省略月、日，为3则省略日
    plt.xticks(ticks = range(0, len(df), date_step), 
            labels = df["date"][::date_step].apply(lambda date: date[:-omitted]), rotation = 30)
    num_legend_col = min(len(df.columns)//2, 4)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5,1), borderaxespad=1, ncol=num_legend_col)

    # pdf.savefig()
    pic_path = path.join(dir_path, all_title + '.png')
    pics.append(pic_path)
    plt.savefig(pic_path, dpi=500, bbox_inches='tight', pad_inches=0.02)
    plt.close()


    # 分别绘制关系和相互的评价
    for ind in range((len(df.columns)-1) // 2):
        country = df.columns[2*ind+1][11:]
        plt.figure(figsize=(8,4))
        plt.title(title.format(country), fontsize=15)
        df_tmp = df.dropna(subset=[f'opinion_on_{country}'])

        # 绘制颜色随数值变化的关系变化图
        def plot_colored_relationship(vals, ls):
            vals = list(vals)
            i = 0
            while i < len(vals):
                start = i-1 if i != 0 else i
                color = get_color(vals[i], ls)
                i += 1
                while i < len(vals) and get_color(vals[i], ls) == color:
                    i += 1
                plt.plot(df_tmp["date"][start:i], vals[start:i], ls=ls, color=color, alpha=0.8)

        plot_colored_relationship(df_tmp[df_tmp.columns[2*ind+1]], ls='--')
        plot_colored_relationship(df_tmp[df_tmp.columns[2*ind+2]], ls=':')
        plot_colored_relationship(df_tmp[df_tmp.columns[2*ind+1]] + df_tmp[df_tmp.columns[2*ind+2]], ls='-')

        date_step = max(len(df_tmp) // 9, 1)  # 横轴相邻标签间隔的月数
        omitted = 6 if date_step > 60 else 3  # 为6则日期省略月、日，为3则省略日
        plt.xticks(ticks = range(0, len(df_tmp), date_step), 
                labels = df_tmp["date"][::date_step].apply(lambda date: date[:-omitted]), rotation = 30)

        # pdf.savefig()
        pic_path = path.join(dir_path, title.format(country)) + '.png'
        pics.append(pic_path)
        plt.savefig(pic_path, dpi=500, bbox_inches='tight', pad_inches=0.02)
        plt.close()
    
    return pics


def add_pics_to_doc(doc, pics, lang):
    doc.append(NoEscape(R'\newpage'))
    
    if lang == 'en':
        section_name = 'Diplomacy'
        subsection1_name = 'The Relationships with All Other Countries'
        subsection2_name = 'The Relationships with Specific Countries'
        annotation = 'Solid lines represent the relationships between us and them, dashed lines represent our opinions of them and dotted lines represent their opinions of us.'
    else:
        section_name = '外交'
        subsection1_name = '与各国关系总览'
        subsection2_name = '与各国关系'
        annotation = '实线代表我方与对方之间的关系，破折线代表我方对对方的评价，点虚线代表对方对我方的评价。'

    with doc.create(Section(section_name)):
        # 加入与各国关系图
        with doc.create(Subsection(subsection1_name)):
            with doc.create(Figure(position='H')) as pic_in_doc:
                pic_in_doc.add_image(pics[0], width='17cm')
        # 加入与单独国家关系图
        doc.append(NoEscape(R'\newpage'))
        with doc.create(Subsection(subsection2_name)):
            doc.append(annotation)
            for pic in pics[1:]:
                with doc.create(Figure(position='H')) as pic_in_doc:
                    pic_in_doc.add_image(pic, width='17cm')
                

def compile_diplomatic_history(doc, data_path, output_path, lang):
    if path.exists(path.join(data_path, 'opinions.csv')):
        print("Compiling the diplomatic history ...")
        stdout.flush()
        
        dir_path = prepare_compile_section(lang, output_path, "Diplomatic", "外交")

        pics = plot_opinions(data_path, dir_path, lang)
        add_pics_to_doc(doc, pics, lang)

        print("Done!")
        stdout.flush()
