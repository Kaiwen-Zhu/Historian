[中文](介绍.md)
# Historian
Stellaris mod which records information of player's country automatically during the game and then compiles its history in PDF format.

Record, Retain, Remember.

## Current features
The compiled history includes
+ Basic info

   country name, government name, personality, origin, homeworld name, homeworld class, home system name, species name
+ Economic history

  Reserves and monthly income of all kinds of resources
+ Demographic history
  
  Population size of all species
+ Scientific history

  Monthly income of scientific points
+ Diplomatic history
  
  Relationships and mutual opinions between us and each of other countries

## Future plans
In my modest dream, the history may include
+ Diplomatic history
  
  Diplomatic actions between us and other countries
+ Scientific history
  
  Name, descriptions and complete date of technologies
+ Military history
  - Details of wars and battles of them
  - Organizations of armies
+ Map
  
  Map of the galaxy
+ Others
  - Local chronicles of each colony
  - Biographies of leaders
  - Description of all events

## Known issues
+ The basic info is only recorded at the start of one game, so changes could not be recorded.
+ When you resume the game, it is possible that the date is earlier than that when you exited game last time, so info of the same date may be recorded twice. Duplicate entries will be removed, which are determined by a subset of attributes (keys) (typically date). For population size of species, as there may be multiple species sharing the same name, I have to set keys as `(date,species_name, num_pop)`, which is all-key. This poses some problems. For example, if two species of the same name has exactly the same pop size, then one of them will be incorrectly removed; also, if on the same date of your two play, the pop sizes of one species differ, then both entries will be incorrectly kept (this seldom happens unless you read save games too often).

## Requirements
+ Python 3
  - PyLatex
  - Pandas
  - Matplotlib
+ LaTex
  
## Usage
Two Python scripts should be run:
+ **Each time you exit game, run `./src/extract_history.py`.** This will extract data from game log and write it to structured data files.
+ **When you want to generate the history, run `./src/compile_history.py`.** This will read data from data files and compile PDF document.

Generated data files and PDF document will be stored in a unique folder in this folder, whose name should be specified as a parameter when running scripts (defaults to `MemoryGrain`). Therefore, **each of your countries should correspond to a unique folder**. This folder will be automatically created the first time you run `extract.py`.

Here is how to run the two scripts.
#### Run `extract_history.py`
Run
```sh
python ./src/extract_history.py -o 'your_folder_name'
```
Generated data files will be stored in `./your_folder_name/data`.
#### Run `compile_history.py`
Run
```sh
python ./src/compile_history.py -o 'your_folder_name'
```
Generated history will be stored in `./your_folder_name/output`.

**IMPORTANT: If you forget to run `extract_history.py` after one play, then its info will be _LOST_ once you enter the game again, because the game log is overwritten each time you play the game.**

## Contributing
Welcome any contribution to modding, including coding (Stellaris modding API or Python) and design of content or layout of the history. If you are interested, feel free to create issues or send emails to `zhukaiwensq@outlook.com`.
