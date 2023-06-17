from sys import stdout
from os import path
import json
from pylatex import Section, NoEscape
        

def compile_basics(doc, data_path, lang):
    print("Compiling the basics ...")
    stdout.flush()

    if lang == 'en':
        section_name = "Basics"
        government_name = "Government Name"
        personality = "Personality"
        origin = "Origin"
        home_world = "Home World"
        species = "Founder Species"
    else:
        section_name = "基本信息"
        government_name = "政府名称"
        personality = "个性"
        origin = "起源"
        home_world = "母星"
        species = "创始物种"

    with open(path.join(data_path, 'basics.json'), encoding='utf-8') as f:
        basics = json.load(f)

    with doc.create(Section(section_name)):
        doc.append(NoEscape(R'''\begin{itemize}
\item ''' + R"{}: {}".format(government_name, basics['government_name']).replace(' ', R'\ ') +
"\item " + R"{}: {}".format(personality, basics['personality']).replace(' ', R'\ ') + 
"\item " + R"{}: {}".format(origin, basics['origin']).replace(' ', R'\ ') + 
"\item " + R"{}: {} {} {}".format(home_world, basics['home_system'], basics['home_world_class'], basics['home_world']).replace(' ', R'\ ') +
"\item " + R"{}: {}".format(species, basics['species']).replace(' ', R'\ ') +
R"\end{itemize}"))

    print("Done!")
    stdout.flush()
