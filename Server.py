import socket 
import DBService
import pickle
from core import Match, Team


class TNTServer:
    def __init__(self, host, port):
        self._host = host
        self._port = port 
        self._connections = []
        self._player1 = []
        self._player2 = []

    def start_up(self):
        # Create the socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind it to address and port
        self._sock.bind((self._host, self._port))
        # Start listening
        self._sock.listen()
        # Start accepting incoming connections
        self.welcome_message()
        

    def shut_down(self):
        self._sock.close()

    def welcome_message(self):
        while True:
            try:
                conn, _ = self._sock.accept()
            except:
                pass 
            else:
                # Add connection to list
                self._connections.append(conn)
                # If only connection, send msg waiting for other player
                if (len(self._connections) == 1):
                    data = {
                        "CMD": "MSG",
                        "Value": "Waiting for other player."
                    }
                    self.send_message_to_client(conn, data)
                # If two connections start game
                else:
                    self.game_loop()


    def send_message_to_client(self, conn, data):
        conn.send(pickle.dumps(data))

    def send_to_all(self, data):
        for conn in self._connections:
            conn.send(pickle.dumps(data))


    def display_welcome_and_champs(self):
        # Ask client to print welcome message
        data = {
            "CMD": "PRINTWELCOME"
        }
        self.send_to_all(data)

        # Need to send all champions to both clients
        self._champions = DBService.get_all_champs()

        data = {
            "CMD": "RECVCHAMPS",
            "Value": self._champions
        }
        self.send_to_all(data)


    def ask_for_team(self, playernr):
        if playernr == 1:
            choosingIndex = 0
            sendIndex = 1
            color = "red"

        else:
            choosingIndex = 1
            sendIndex = 0
            color = "blue"

        data = {
            "CMD": "CHOOSECHAMP",
            "Args": {
                "playername": "Player " + str(playernr),
                "color": color,
                "champions": self._champions,
                "player1list": self._player1,
                "player2list": self._player2,
            }
        }

        # Send to first player/connection
        self.send_message_to_client(self._connections[choosingIndex], data)

        # Recv champ here
        while True:
            chosen_champ = self._connections[choosingIndex].recv(1024).decode()
            if not chosen_champ:
                continue
            # Check which list to add to
            if playernr == 1:
                self._player1.append(chosen_champ)
            else:
                self._player2.append(chosen_champ)
            break
        
        # Send result to other player
        data = {
            "CMD": "PLAYERCHOSE",
            "Args": {
                "playernumber": playernr,
                "champion": chosen_champ
            }
        }
        self.send_message_to_client(self._connections[sendIndex], data)



    def game_loop(self):
        # Ask client to display welcome msg and avilable champs
        self.display_welcome_and_champs()
        
        # Ask each player twice
        for _ in range(2):
            self.ask_for_team(1)
            self.ask_for_team(2)

        # Create match object from teams
        match = Match(
            Team([self._champions[name] for name in self._player1]),
            Team([self._champions[name] for name in self._player2])
        )

        # Play match
        match.play()

        # Tell client to print match summary
        data = {
            "CMD": "PRINTMATCH",
            "Value": match
        }

        self.send_to_all(data)

        # Finally, upload match staistics
        DBService.uploadMatchStatistic(match.to_dict())

        
            



if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 7017
    serv = TNTServer(HOST, PORT)
    serv.start_up()
    serv.shut_down()








