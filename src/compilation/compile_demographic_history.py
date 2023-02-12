from sys import stdout
from os import path
import matplotlib.pyplot as plt
import pandas as pd
from pylatex import Section, Subsection, Figure, NoEscape
from .utils import *


def plot_pop_size(data_path, dir_path, lang):
    """ Plots the line chart of population size.
    """    

    if lang == 'en':
        file_name = 'Population Size'
        total_label = "Total Size"
    else:
        file_name = '人口数量'
        total_label = "总数"

    plt.figure(figsize=(9, 11))

    # 绘制人口总数
    df = pd.read_csv(path.join(data_path, 'num_pop.csv'), index_col=0, sep=';')
    plt.plot(df["date"], df['num_pop'], label=total_label, alpha=0.8)

    date_step = max(len(df) // 9, 1)  # 横轴相邻标签间隔的月数
    omitted = 6
    plt.xticks(ticks = range(0, len(df), date_step), 
            labels = df["date"][::date_step].apply(lambda date: date[:-omitted]), rotation = 30)

    # 绘制各物种人口数量
    df_species = pd.read_csv(path.join(data_path, 'species_pop_size.csv'), index_col=0, sep=';')   
    species_names = set(df_species['species_name']) 
    for species in species_names:
        df_one_species = df_species[df_species['species_name']==species]
        plt.plot(df_one_species['date'], df_one_species['num_pop'], label=species, alpha=0.8)

    # plt.xticks(ticks = range(0, len(df_species), date_step), 
            # labels = df_species["date"][::date_step].apply(lambda date: date[:-omitted]), rotation = 30)
    num_legend_col = min(len(species_names)//2, 5)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5,1), borderaxespad=1, ncol=num_legend_col)


    pic_path = path.join(dir_path, file_name) + '.png'
    plt.savefig(pic_path, dpi=500, bbox_inches='tight', pad_inches=0.02)
    plt.close()

    return pic_path


def plot_unity(data_path, dir_path, lang):
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

    pic_path = path.join(dir_path, title + '.png')
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


def compile_demographic_history(doc, data_path, output_path, lang, name):
    print("Compiling the demographic history ...")
    stdout.flush()

    dir_path = prepare_compile_section(name, lang, output_path, "Demographic", "人口")

    pics = []
    pics.append(plot_pop_size(data_path, dir_path, lang))
    pics.append(plot_unity(data_path, dir_path, lang))
    add_pics_to_doc(doc, pics, lang)

    print("Done!")
    stdout.flush()