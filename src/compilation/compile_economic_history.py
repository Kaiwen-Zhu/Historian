from sys import stdout
from os import path
import matplotlib.pyplot as plt
import pandas as pd
from pylatex import Section, Figure, NoEscape
from .utils import *
# from matplotlib.backends.backend_pdf import PdfPages
        

def plot_resources_reserves_income(data_path, dir_path, lang) -> list[str]:
    """ Plots the line charts of reserves and monthly income of various resources and returns the paths of them.
    """   

    pics = []  # 存储各图路径

    resources = ['energy', 'minerals', 'food', 'consumer_goods', 'alloys',
            'volatile_motes', 'exotic_gases', 'rare_crystals', 'living_metal', 'zro',
            'dark_matter', 'nanites']
    colors = ['#f1e916', '#e95350', '#71bb50', '#d2754c', '#7e3e9e',
            '#973d2f', '#027a2e', '#cc8602', '#647676', '#567fce',
            '#1a212c', '#b1bfb3']

    if lang == 'en':
        time = 'Time'
        reserves = 'Reserves'
        income = 'Monthly Income'

    else:
        time = '时间'
        income = '月收入'
        reserves = '储量'
        resources_zh = ['能量币', '矿物', '食物', '消费品', '合金', '易爆微粒', '异星天然气',
            '稀有水晶', '活体金属', '泽珞', '暗物质', '纳米机器人']
        

    df = pd.read_csv(path.join(data_path, 'resources.csv'), index_col=0, sep=';')
    
    resources_type_map = [(('Fundamental Resources', '基础资源'), range(3)),
                        (('Industrial Resources', '工业资源'), range(3,5)), 
                        (('Rare Resources', '稀有资源'), range(5,12))]
    # 绘制一类资源的储量和月收入折线图
    def plot_one_type_resources(resources_category):
        # resources_category: 0-基础资源，1-工业资源，2-稀有资源
        resources_category_name, resources_idx_range = resources_type_map[resources_category]
        num_legend_col = min(len(resources_idx_range), 3)

        fig, (axes_reserves, axes_income) = plt.subplots(2, 1, figsize=(9,13))
        if lang == 'en':
            suptitle = 'The Reserves and Monthly Income of {}'.format(resources_category_name[0])
        else:
            suptitle = '{}储量及月收入'.format(resources_category_name[1])
        fig.suptitle(suptitle, fontsize=15)

        for resource_idx in resources_idx_range:
            resource_name = resources[resource_idx]
            if lang == 'en':
                resource_name_in_label = resources[resource_idx].replace('_', ' ').title()
            else:
                resource_name_in_label = resources_zh[resource_idx]

            date_step = max(len(df) // 9, 1)  # 横轴相邻标签间隔的月数
            omitted = 6 if date_step > 60 else 3  # 为6则日期省略月、日，为3则省略日
            xticks_labels = df["date"][::date_step]
            axes_reserves.plot(df["date"], df[f'{resource_name}_reserves'], alpha = 0.8,
                                label = resource_name_in_label, color = colors[resource_idx])
            axes_reserves.set_xlabel(time, fontsize = 17)
            axes_reserves.set_xticks(xticks_labels)
            axes_reserves.set_xticklabels(labels = xticks_labels.apply(lambda date: date[:-omitted]), rotation = 30)
            axes_reserves.set_ylabel(reserves, fontsize = 17)
            
            axes_income.plot(df["date"], df[f'{resource_name}_income'], alpha = 0.8,
                                label = resource_name_in_label, color = colors[resource_idx])
            axes_income.set_xlabel(time, fontsize = 17)
            axes_income.set_xticks(xticks_labels)
            axes_income.set_xticklabels(labels = xticks_labels.apply(lambda date: date[:-omitted]), rotation = 30)
            axes_income.set_ylabel(income, fontsize = 17)

        plt.subplots_adjust(hspace = 0.5)
        axes_reserves.legend(loc='lower center', bbox_to_anchor=(0.5,1), borderaxespad=1, ncol=num_legend_col)

        # pdf.savefig()
        pic_path = path.join(dir_path, suptitle + '.png')
        pics.append(pic_path)
        plt.savefig(pic_path, dpi=500, bbox_inches='tight', pad_inches=0.02)
        plt.close()


    # 绘制各资源储量/收入折线图
    # with PdfPages(path.join('..', output, filename)) as pdf:
    for resources_category in range(3):
        plot_one_type_resources(resources_category)
    
    return pics


def add_pics_to_doc(doc, pics, lang):
    doc.append(NoEscape(R'\newpage'))

    if lang == 'en':
        section_name = 'Economy'
    else:
        section_name = '经济'
        
    with doc.create(Section(section_name)):
        for pic in pics:
            with doc.create(Figure(position='H')) as pic_in_doc:
                pic_in_doc.add_image(pic, width='15cm')


def compile_economic_history(doc, data_path, output_path, lang):
    print("Compiling the economic history ...")
    stdout.flush()

    dir_path = prepare_compile_section(lang, output_path, "Economic", "经济")

    pics = plot_resources_reserves_income(data_path, dir_path, lang)
    add_pics_to_doc(doc, pics, lang)

    print("Done!")
    stdout.flush()