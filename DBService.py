from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")


def getCollection(collection):
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = config["DB_URL"]

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['LNT'][collection]


# CHAMPIONS

def add_champion(champ):
    collection = getCollection("Champions")
    collection.insert_one(champ)


def get_champion(name):
    collection = getCollection("Champions")
    champList = collection.find({"Name": name})
    # TODO: error handle this
    champ = champList[0]
    return {
        "Name": champ["Name"],
        "rockProbability": champ["rockProbability"],
        "paperProbability": champ["paperProbability"],
        "scissorsProbability": champ["scissorsProbability"]
    }

def get_all_champs():
    collection = getCollection("Champions")
    return collection.find()




# MATCH STATISTICS

def uploadMatchStatistic(match):
    collection = getCollection("MatchHistory")
    collection.insert_one(match)


def getMatchHistory(nMatches):
    collection = getCollection("MatchHistory")
    matchList = collection.find({}).limit(nMatches)
    return matchList









