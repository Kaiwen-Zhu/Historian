from pylatex import Package, Command, NoEscape
from os import path
from json import load


def prepare(doc, data_path, lang):
    # 引入宏包
    doc.packages.add(Package('float'))
    doc.packages.add(Package('hyperref', options=['breaklinks=true','colorlinks=true','linkcolor=black','citecolor=black','urlcolor=black']))
    if lang == 'zh':
        doc.packages.add(Package('ctex'))

    # 创建标题页
    with open(path.join(data_path, 'basics.json'), encoding='utf-8') as f:
        basics = load(f)
        name = basics['name'].replace(' ', '\ ')
        end_date = basics['end_date'][:4]

    if lang == 'en':
        title = f'The History of {name}'
    else:
        title = f'{name}史'

    doc.append(NoEscape(R'''\begin{titlepage}
\begin{center}
\vspace*{10cm}
{\Huge\bfseries ''' + title + R'''} \\ 
\vspace{1cm}
{\huge\bfseries 2200 - ''' + end_date + R'''}
\end{center}
\end{titlepage}'''))

    # 创建目录页
    doc.append(NoEscape(R'''\begin{center}
\tableofcontents
\end{center}'''))
    doc.append(NoEscape(R'\thispagestyle{empty}'))
    doc.append(NoEscape(R'\newpage'))
    doc.append(NoEscape(R'\setcounter{page}{1}'))