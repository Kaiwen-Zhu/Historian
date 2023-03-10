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

  - Total population size
  - Population size of all species
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
+ The diplomatic history identifies countries by their names, but names are changeable.
+ When you resume the game, it is possible that the date is earlier than that when you exited game last time, so info of the same date may be recorded twice. Duplicate entries will be removed, which are determined by a subset of attributes (keys) (typically date). However, for population size of species, as there may be multiple species sharing the same name, I have to set keys as `["date","species_name", "num_pop"]`, which is all-key. This poses some problems. For example, if two species of the same name has exactly the same pop size, then one of them will be incorrectly removed; also, if on the same date of your two play, the pop sizes of one species differ, then both entries will be incorrectly kept (this seldom happens unless you read save games too often).

## Requirements
+ Python 3
+ LaTex
+ PyLaTex
  
## Usage
Create a new folder for one game in the same folder as this file and specify its name in `extract.py` and `compile.py`. After exiting game, run `extract.py` to extract info from game log, which will be stored in `{your_folder_name}/data`. Run `compile.py` when you want to generate the history, which will be stored in `{your_folder_name}/output`.

**IMPORTANT: If you forget to run `extract.py` after one play, then its info will be _LOST_ once you enter the game again, because the game log is overwritten each time you play the game.**

## Contributing
I am not so familiar with the modding API provided by PDX, so I will be very happy if you are interested and could contact me. Feel free to send emails to `zhukaiwensq@outlook.com` or just talk to me in QQ (3387572450). Any ideas about content of the history, layout of the document or any other things are highly welcome!
