from os import path
from json import load
from pylatex import Document
from prepare import prepare
from compile_basics import compile_basics
from compile_economic_history import compile_economic_history
from compile_demographic_history import compile_demographic_history
from compile_scientific_history import compile_scientific_history
from compile_diplomatic_history import compile_diplomatic_history
from sys import stdout


def main():
    # # data_dir = input("请输入存储数据的文件夹名称：")
    # data_dir = "data"
    # # output = input("请输入存储输出的文件夹名称：")
    # output = "output"
    
    # lang = input("选择语言\n输入“zh”以使用中文\nInput "en" if you prefer English\n")
    lang = "zh"

    root_path = path.dirname(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))  # Stellaris 目录路径
    data_dir = "洛克机械师工会data"  # 存储数据的目录名称
    data_path = path.join(root_path, "mod", "Historian", data_dir)
    output_dir = "洛克机械师工会output"  # 存储输出的目录名称
    output_path = path.join(root_path, "mod", "Historian", output_dir)
    
    geometry_options = {"top": "1.27cm", "bottom": "2cm", "left": "1.27cm", "right": "1.27cm"}  # 页边距
    doc = Document(geometry_options=geometry_options)
    

    prepare(doc, data_path, lang)
    compile_basics(doc, data_path, lang)
    compile_economic_history(doc, data_path, output_path, lang)
    compile_demographic_history(doc, data_path, output_path, lang)
    compile_scientific_history(doc, data_path, output_path, lang)
    compile_diplomatic_history(doc, data_path, output_path, lang)


    with open(path.join(data_path, 'basics.json'), encoding='utf-8') as f:
        basics = load(f)
        name = basics['name']
    if lang == 'en':
        file_path = path.join(output_path, f'The History of {name}')
    else:
        file_path = path.join(output_path, f'{name}史')

    print("Generating the document ...")
    stdout.flush()
    # doc.generate_tex(file_path)
    doc.generate_pdf(file_path, clean_tex=False, compiler='xelatex')
    print("Done!")
    stdout.flush()
    
    print("Successfully compiled the history!")
    # input("Press any key to close the window.")



if __name__ == '__main__':
    main()
