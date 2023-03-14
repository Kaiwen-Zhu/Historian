from os import path, mkdir
from pylatex import Document
from sys import stdout
from compilation import *


def main():
    # HIS_dir = input("请输入存储数据与输出的文件夹名称：")
    HIS_dir = "旋桌骑士高阶领主国"  # 存储数据目录与输出目录的目录名称
    
    # lang = input("选择语言\n输入“zh”以使用中文\nInput "en" if you prefer English\n")
    lang = "zh"

    Historian_path = path.dirname(path.dirname(path.abspath(__file__)))  # Historian 目录路径
    data_path = path.join(Historian_path, HIS_dir, "data")
    output_path = path.join(Historian_path, HIS_dir, "output")

    assert path.exists(data_path)
    if not path.exists(output_path):
        mkdir(output_path)
    
    geometry_options = {"top": "0.89cm", "bottom": "1.43cm", "left": "0.89cm", "right": "0.89cm"}
    doc = Document(geometry_options=geometry_options)

    name = prepare(doc, data_path, lang)
    compile_basics(doc, data_path, lang)
    compile_economic_history(doc, data_path, output_path, lang)
    compile_demographic_history(doc, data_path, output_path, lang)
    compile_scientific_history(doc, data_path, output_path, lang)
    compile_diplomatic_history(doc, data_path, output_path, lang)

    if lang == 'en':
        file_path = path.join(output_path, f'The History of {name}')
    else:
        file_path = path.join(output_path, f'{name}史')

    print("Generating the document ...")
    stdout.flush()
    # doc.generate_tex(file_path)
    doc.generate_pdf(file_path, clean_tex=False, compiler='latexmk', compiler_args=[
        '-xelatex', '-file-line-error', '-halt-on-error'])
    print("Done!")
    stdout.flush()
    
    print("Successfully compiled the history!")
    # input("Press any key to close the window.")



if __name__ == '__main__':
    main()
