from os import environ
from dotenv import dotenv_values
from pymongo import MongoClient
from Core import Champion
from socket import *
import pickle

config = dotenv_values(".env")

class DBServer:
    def __init__(self, host: str, port: int, buffer_size: int = 2048) -> None:
        self._host = host
        self._port = port
        self._buffer_size = buffer_size
        self._connections = []
    
    def start(self):
        self._serv_sock = create_server(
            (self._host, self._port),
            reuse_port=True
        )
        CONNECTION_STRING = config["DB_URL"]
        self._client = MongoClient(CONNECTION_STRING)
        self.add_connection()
    
    def add_connection(self):
        while True:
            try:
                conn, _ = self._serv_sock.accept()
            except:
                pass 
            else:
                # Add connection to list
                self._connections.append(conn)
                # Start listening
                self.listen_for_messages()
    
    def listen_for_messages(self):
        while True:
            for conn in self._connections:
                # Try to recv data
                data = conn.recv(self._buffer_size)

                # Continue if no data
                if not data:
                    continue

                # Load data with pickle
                data = pickle.loads(data)

                # Match commands
                match data["CMD"]:
                    case "ADDCHAMP":
                        self.add_champion(data["Value"])
                    case "GETCHAMP":
                        champ = self.get_champion(data["Value"])
                        conn.send(pickle.dumps(champ))
                    case "GETALLCHAMPS":
                        champs = self.get_all_champs()
                        conn.send(pickle.dumps(champs))
                    case "UPLOADMATCH":
                        self.uploadMatchStatistic(data["Value"])
                    case "GETMATCHES":
                        matches = self.getMatchHistory(data["Value"])
                        conn.send(pickle.dumps(matches))
    
    def getCollection(self, collection):
        return self._client['LNT'][collection]
    
    # CHAMPIONS
    
    def add_champion(self, champ):
        collection = self.getCollection("Champions")
        collection.insert_one(champ)


    def get_champion(self, name):
        collection = self.getCollection("Champions")
        champList = collection.find({"Name": name})
        # TODO: error handle this
        champ = champList[0]
        return {
            "Name": champ["Name"],
            "rockProbability": champ["rockProbability"],
            "paperProbability": champ["paperProbability"],
            "scissorsProbability": champ["scissorsProbability"]
        }

    def get_all_champs(self):
        champions = {}
        collection = self.getCollection("Champions").find()
        for doc in collection:
            champ = Champion(doc["Name"], float(doc["rockProbability"]), float(doc["paperProbability"]))
            champions[doc["Name"]] = champ
        return champions


    # MATCH STATISTICS

    def uploadMatchStatistic(self, match):
        collection = self.getCollection("MatchHistory")
        collection.insert_one(match)


    def getMatchHistory(self, nMatches):
        collection = self.getCollection("MatchHistory")
        matchList = collection.find({}).limit(nMatches)
        return matchList



if __name__ == "__main__":
    server = environ.get("SERVER", "localhost")
    port = 7020
    serv = DBServer(server, port)
    serv.start()