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
        ethics = "Ethics"
    else:
        section_name = "基本信息"
        government_name = "政府名称"
        personality = "个性"
        origin = "起源"
        home_world = "母星"
        species = "创始物种"
        ethics = "主流思潮"

    with open(path.join(data_path, 'basics.json'), encoding='utf-8') as f:
        basics = json.load(f)

    loc = {
            "FanaticEgalitarian": ("极端平等主义", "Fanatic Egalitarian"),
            "FanaticAuthoritarian": ("极端威权主义", "Fanatic Authoritarian"),
            "Egalitarian": ("平等主义", "Egalitarian"),
            "Authoritarian": ("威权主义", "Authoritarian"),

            "FanaticPacifist": ("极端和平主义", "Fanatic Pacifist"),
            "FanaticMilitarist": ("极端军国主义", "Fanatic Militarist"),
            "Pacifist": ("和平主义", "Pacifist"),
            "Militarist": ("军国主义", "Militarist"),

            "FanaticXenophile": ("极端亲外主义", "Fanatic Xenophile"),
            "FanaticXenophobe": ("极端排外主义", "Fanatic Xenophobe"),
            "Xenophile": ("亲外主义", "Xenophile"),
            "Xenophobe": ("排外主义", "Xenophobe"),

            "FanaticMaterialist": ("极端唯物主义", "Fanatic Materialist"),
            "FanaticSpiritualist": ("极端唯心主义", "Fanatic Spiritualist"),
            "Materialist": ("唯物主义", "Materialist"),
            "Spiritualist": ("唯心主义", "Spiritualist"),

            "GestaltConsciousness": ("格式塔意识", "Gestalt Consciousness")
        }
    
    with doc.create(Section(section_name)):
        doc.append(NoEscape(R'''\begin{itemize}
\item ''' + R"{}: {}".format(government_name, basics['government_name']).replace(' ', R'\ ') +
"\item " + R"{}: {}".format(personality, basics['personality']).replace(' ', R'\ ') + 
"\item " + R"{}: {}".format(origin, basics['origin']).replace(' ', R'\ ') + 
"\item " + R"{}: {} {} {}".format(home_world, basics['home_system'], basics['home_world_class'], basics['home_world']).replace(' ', R'\ ') +
"\item " + R"{}: {}".format(species, basics['species']).replace(' ', R'\ ') +
"\item " + R"{}: {}".format(ethics, ', '.join(list(map(lambda k: loc[k][lang=='en'], basics['ethics']))).replace(' ', R'\ ') + 
R"\end{itemize}")))

    print("Done!")
    stdout.flush()
