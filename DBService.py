from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = config["DB_URL"]

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['LNT']


def add_champion(champ):
    collection = get_database()["Champions"]
    collection.insert_one(champ)



for line in open("some_champs.txt"):
    words = line.split(",")
    champ = {
        "Name": words[0],
        "rockProbability": words[1],
        "scissorsProbability": words[2],
        "paperProbability": words[3][:-1]

    }
    add_champion(champ)


