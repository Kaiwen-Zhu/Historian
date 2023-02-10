from sys import stdout
from os import path, mkdir
from shutil import rmtree
import json
import matplotlib.pyplot as plt
import pandas as pd
from pylatex import Section, Subsection, Figure, NoEscape
        

def plot_num_pop(data_path, output_path, dir_name, lang):
    """ Plots the line chart of population size.
    """    

    if lang == 'en':
        file_name = 'Population Size'
    else:
        file_name = '人口数量'
        
    df = pd.read_csv(path.join(data_path, 'num_pop.csv'), index_col=0, sep=';')
    
    plt.figure(figsize=(9, 13))
    plt.plot(df["date"], df[f'num_pop'])

    date_step = max(len(df) // 9, 1)  # 横轴相邻标签间隔的月数
    omitted = 6
    plt.xticks(ticks = range(0, len(df), date_step), 
            labels = df["date"][::date_step].apply(lambda date: date[:-omitted]), rotation = 30)

    dir_path = path.join(output_path, dir_name)
    if path.exists(dir_path):
        rmtree(dir_path)
    mkdir(dir_path)
    pic_path = path.join(dir_path, file_name) + '.png'
    plt.savefig(pic_path, dpi=500, bbox_inches='tight', pad_inches=0.02)
    plt.close()

    return pic_path


def plot_unity(data_path, output_path, dir_name, lang):
    """ Plots the line chart of reserves and monthly income of unity.
    """    

    if lang == 'en':
        title = 'The Reserves and Monthly Income of Unity'
        time = 'Time'
        reserves = 'Reserves'
        income = 'Income'
    else:
        title = '凝聚力储量及月收入'
        time = '时间'
        reserves = '储量'
        income = '月收入'

    df = pd.read_csv(path.join(data_path, 'resources.csv'), index_col=0, sep=';')
    
    fig, (axes_reserves, axes_income) = plt.subplots(2, 1, figsize=(9,13))
    
    date_step = max(len(df) // 9, 1)  # 横轴相邻标签间隔的月数
    omitted = 6 if date_step > 60 else 3  # 为6则日期省略月、日，为3则省略日
    xticks_labels = df["date"][::date_step]

    axes_reserves.plot(df["date"], df['unity_reserves'], color = '#51aca6')
    axes_reserves.set_xlabel(time, fontsize = 17)
    axes_reserves.set_xticks(xticks_labels)
    axes_reserves.set_xticklabels(labels = xticks_labels.apply(lambda date: date[:-omitted]), rotation = 30)
    axes_reserves.set_ylabel(reserves, fontsize = 17)

    axes_income.set_xlabel(time, fontsize = 17)
    axes_income.plot(df["date"], df['unity_income'], color = '#51aca6')
    axes_income.set_xticks(xticks_labels)
    axes_income.set_xticklabels(labels = xticks_labels.apply(lambda date: date[:-omitted]), rotation = 30)
    axes_income.set_ylabel(income, fontsize = 17)

    plt.subplots_adjust(hspace = 0.5)
    plt.suptitle(title, fontsize=15)

    pic_path = path.join(output_path, dir_name, title + '.png')
    plt.savefig(pic_path, dpi=500, bbox_inches='tight', pad_inches=0.02)
    plt.close()

    return pic_path


def add_pics_to_doc(doc, pics, lang):
    doc.append(NoEscape(R'\newpage'))

    if lang == 'en':
        section_name = 'Demography'
        subsection1_name = 'Population Size'
        subsection2_name = 'Unity'
    else:
        section_name = '人口'
        subsection1_name = '人口数量'
        subsection2_name = '凝聚力'

    with doc.create(Section(section_name)):
        with doc.create(Subsection(subsection1_name)):
            with doc.create(Figure(position='H')) as pic_in_doc:
                pic_in_doc.add_image(pics[0], width='15cm')
        with doc.create(Subsection(subsection2_name)):
            with doc.create(Figure(position='H')) as pic_in_doc:
                pic_in_doc.add_image(pics[1], width='15cm')


def compile_demographic_history(doc, data_path, output_path, lang):
    print("Compiling the demographic history ...")
    stdout.flush()

    with open(path.join(data_path, 'basics.json'), encoding='utf-8') as f:
        basics = json.load(f)
        name = basics['name']
    if lang == 'en':
        dir_name = f'The Demographic History of {name}'
    else:
        plt.rcParams['font.sans-serif'] = ['SimHei']
        dir_name = f'{name}人口史'

    pics = []
    pics.append(plot_num_pop(data_path, output_path, dir_name, lang))
    pics.append(plot_unity(data_path, output_path, dir_name, lang))
    add_pics_to_doc(doc, pics, lang)

    print("Done!")
    stdout.flush()