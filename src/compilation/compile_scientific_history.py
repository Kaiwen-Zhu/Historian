from sys import stdout
from os.path import join as path_join
import pandas as pd
from shutil import copyfile
from jinja2 import Environment
import pyecharts.options as opts
from pyecharts.charts import Line
from .utils import *


def plot_points_income(data_dir, dir_path, assets_path):
    df = pd.read_csv(path_join(data_dir, 'resources.csv'), index_col=0, sep=';')
    dates = df["date"].apply(lambda date: date[:-3]).tolist()
    c = (
        Line()
        .add_xaxis(dates)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=15)),
            yaxis_opts=opts.AxisOpts(is_scale=True),
            title_opts=opts.TitleOpts(title="研究点数月收入"),
            legend_opts=opts.LegendOpts(),
            # datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
            toolbox_opts=opts.ToolboxOpts(
                is_show=True,
                orient="horizontal",
                feature=opts.ToolBoxFeatureOpts(
                    save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                        type_="png", pixel_ratio=2, background_color='white'),
                    restore=opts.ToolBoxFeatureRestoreOpts(),
                    data_zoom=opts.ToolBoxFeatureDataZoomOpts(back_title="区域缩放回退"),
                    data_view=opts.ToolBoxFeatureDataViewOpts(is_show=False),
                    magic_type=opts.ToolBoxFeatureDataViewOpts(is_show=False),
                    brush=opts.ToolBoxFeatureDataZoomOpts(is_show=False)
                )
            )
        )
    )

    names = ('physics_research', 'society_research', 'engineering_research')
    labels = ('物理学研究', '社会学研究', '工程学研究')
    colors = ('#359db6', '#53b977', '#df8c4c')

    research_src_path = path_join(assets_path, 'resources', '{}.webp')
    research_dst_path = path_join(dir_path, '{}.webp')
    
    for name, label, color in zip(names, labels, colors):
        copyfile(research_src_path.format(name), research_dst_path.format(name))
        val = df[f'{name}_income'].tolist()
        c.add_yaxis(label, val, color=color, is_smooth=True, is_symbol_show=False)
    
    c.render(path_join(dir_path, f'研究点数月收入.html'))


def compile_scientific_history(env: Environment, assets_path: str, data_path: str, output_path: str):
    print("编译科技史...", end=' ')
    stdout.flush()

    dir_path = prepare_output(output_path, "科技史")
    plot_points_income(data_path, dir_path, assets_path)
    # render_page(env, 'scientific_history.html', dir_path, '科技史.html')

    print("完成")
    stdout.flush()
