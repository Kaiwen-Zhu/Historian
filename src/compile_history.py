from os import path, mkdir
from pylatex import Document
from sys import stdout
import argparse
from compilation import *


def main():
    parser = argparse.ArgumentParser(description='Compile the history in PDF.')
    parser.add_argument('--output', '-o', help='the output directory', type=str, default='MemoryGrain')
    parser.add_argument('--lang', '-l', help='the language of the history', type=str, 
                        choices=['en', 'zh'], default='zh')
    args = parser.parse_args()
    
    Historian_path = path.dirname(path.dirname(path.abspath(__file__)))  # Historian 目录路径
    data_path = path.join(Historian_path, args.output, "data")
    output_path = path.join(Historian_path, args.output, "output")

    assert path.exists(data_path)
    if not path.exists(output_path):
        mkdir(output_path)
    
    geometry_options = {"top": "0.89cm", "bottom": "1.43cm", "left": "0.89cm", "right": "0.89cm"}
    doc = Document(geometry_options=geometry_options)

    name = prepare(doc, data_path, args.lang)
    compile_basics(doc, data_path, args.lang)
    compile_economic_history(doc, data_path, output_path, args.lang)
    compile_demographic_history(doc, data_path, output_path, args.lang)
    compile_scientific_history(doc, data_path, output_path, args.lang)
    compile_diplomatic_history(doc, data_path, output_path, args.lang)

    if args.lang == 'en':
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
