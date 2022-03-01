from matplotlib import collections
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


# CHAMPIONS

def add_champion(champ):
    collection = get_database()["Champions"]
    collection.insert_one(champ)


def get_champion(name):
    collection = get_database()["Champions"]
    champList = collection.find({"Name": name})
    # TODO: error handle this
    champ = champList[0]
    return {
        "Name": champ["Name"],
        "rockProbability": champ["rockProbability"],
        "paperProbability": champ["paperProbability"],
        "scissorsProbability": champ["scissorsProbability"]
    }


# MATCH STATISTICS

def uploadMatchStatistic(match):
    collection = get_database()["MatchHistory"]
    collection.insert_one(match)

def getMatchHistory(nMatches):
    collection = get_database()["MatchHistory"]
    matchList = collection.find().skip(collection.count() - nMatches)
    return matchList[0:11]




