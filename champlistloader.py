from core import Champion
import DBService


def from_DB() -> dict[str, Champion]:
    champions = {}

    champList = DBService.get_all_champs()
    for champ in champList:
        champion = Champion(champ["Name"], 
        float(champ["rockProbability"]), 
        float(champ["scissorsProbability"]),
        float(champ["paperProbability"]))
        
        champions[champ["Name"]] = champion

    return champions


def load_some_champs():
<<<<<<< HEAD
    return from_csv('some_champs.txt')
=======
    return from_DB()
    
>>>>>>> 9be5ec4e90566b25e3f91f611817d880614592d1

