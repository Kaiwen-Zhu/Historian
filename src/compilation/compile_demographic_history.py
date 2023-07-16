from sys import stdout
from os import path
import matplotlib.pyplot as plt
import pandas as pd
from pylatex import Section, Subsection, Figure, NoEscape
from .utils import *


def pad_vacant_year(df, species_name, all_dates):        
    """Makes the date complete by setting `num_pop` as 0 and fills `nan` by interpolation.""" 

    # 插入中间缺失的元组
    prev_year = int(df.iloc[0]['date'][:4])
    for idx, row in df.iterrows():
        this_year = int(row['date'][:4])
        if this_year > prev_year + 1:
            for vacant_year in range(prev_year+1, this_year):
                df = pd.concat([df, pd.DataFrame(
                    {"date": [f"{vacant_year}.01.15"], "species_name": species_name, "num_pop": 0})])
        prev_year = this_year
    
    # 插入头尾缺失的元组
    this_dates = df['date'].values
    new_dates = []
    for date in all_dates:
        if date not in this_dates:
            new_dates.append(date)
        else:
            break
    for date in all_dates[::-1]:
        if date not in this_dates:
            new_dates.append(date)
        else:
            break
    df = pd.concat([df, pd.DataFrame(
                {"date": new_dates, "species_name": species_name, "num_pop": 0})])

    df.sort_values(by="date", inplace=True)
    df.reset_index(inplace=True, drop=True) 
    df['num_pop'].interpolate(inplace=True)
    return df


def plot_pop_size(data_path, dir_path, lang):
    """Plots the line chart of population size of species."""    

    if lang == 'en':
        file_name = 'Population Size'
        others_label = "Other {} species"
    else:
        file_name = '人口数量'
        others_label = "其它{}个物种"

    plt.figure(figsize=(9, 13))
    colors = plt.get_cmap('tab20').colors
    plt.gca().set_prop_cycle('color', colors)  # 设置颜色
    num_legend = 0  # 图例个数

    df_species = pd.read_csv(path.join(data_path, 'species_pop_size.csv'), index_col=0, sep=';')  
    all_dates = df_species['date'].drop_duplicates(keep='first')
    all_dates.reset_index(inplace=True, drop=True)

    date_step = max(len(all_dates) // 9, 1)  # 横轴相邻标签间隔的月数
    omitted = 6
    plt.xticks(ticks = range(0, len(all_dates), date_step), 
            labels = all_dates[::date_step].apply(lambda date: date[:-omitted]), rotation = 30)

    # 统计各物种最大数量，仅对前 `MAX_SPECIES_NUM` 个物种单独绘制
    MAX_SPECIES_NUM = 19
    max_sizes = []  # 各物种最大数量
    for species in set(df_species['species_name']):
        max_size = (species, df_species[df_species['species_name']==species]['num_pop'].max())
        if max_size[-1] == 0:
            df_species.drop(index=df_species[df_species['species_name']==species].index, inplace=True)
        else:
            max_sizes.append(max_size)
    max_sizes.sort(key = lambda t: t[-1])
    others = set(t[0] for t in max_sizes[:-MAX_SPECIES_NUM])  # `others` 中的物种不单独绘制
    num_in_others = len(others)

    # 按出现顺序统计物种名称
    species_names = df_species['species_name'].drop_duplicates(keep='first').values.tolist()
    
    pop_sizes = []
    other_num = pd.DataFrame(columns=["date", "species_name", "num_pop"])  # 记录其它物种的人口数量之和
    color_iter = iter(colors)
    for species in species_names:
        df_one_species = df_species[df_species['species_name']==species].copy()
        df_one_species = pad_vacant_year(df_one_species, species, all_dates)  # 将中间缺失的值补上 0
        if species not in others:
            # 可能有多个物种同名，需要合并
            nums = []
            for date in all_dates:
                nums.append(df_one_species[df_one_species['date']==date]['num_pop'].sum())
            assert len(all_dates) == len(nums)
            pop_sizes.append(nums)
            plt.plot([], [], label=species, color=next(color_iter))
            num_legend += 1

        else:
            for date in all_dates:
                num = df_one_species[df_one_species['date']==date]['num_pop'].sum()
                if date not in other_num['date'].values:
                    other_num.loc[len(other_num)] = [date, "others", num]
                else:
                    other_num.loc[other_num['date']==date, 'num_pop'] += num
                    
    # 绘制其它物种人口数量之和
    if len(other_num) > 0:
        other_num.sort_values(by='date', inplace=True)
        other_num.reset_index(inplace=True, drop=True)
        pop_sizes.append(other_num['num_pop'])
        plt.plot([], [], label=others_label.format(num_in_others), color=next(color_iter))
        num_legend += 1
    plt.stackplot(all_dates, pop_sizes, colors=colors)

    num_legend_col = min(num_legend, 5)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5,1), borderaxespad=1, ncol=num_legend_col)

    pic_path = path.join(dir_path, file_name) + '.png'
    plt.savefig(pic_path, dpi=500, bbox_inches='tight', pad_inches=0.02)
    plt.close()

    return pic_path


def plot_unity(data_path, dir_path, lang):
    """Plots the line chart of reserves and monthly income of unity."""    

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


def compile_demographic_history(doc, data_path, output_path, lang):
    print("Compiling the demographic history ...")
    stdout.flush()

    dir_path = prepare_compile_section(lang, output_path, "Demographic", "人口")

    pics = []
    pics.append(plot_pop_size(data_path, dir_path, lang))
    pics.append(plot_unity(data_path, dir_path, lang))
    add_pics_to_doc(doc, pics, lang)

    print("Done!")
    stdout.flush()
