import socket 
import DBService
import pickle

welcome_msg = 'MSG \n' 'Welcome to [bold yellow]Team Local Tactics[/bold yellow]!' '\n' 'Each player choose a champion each time.' '\n'

class TNTServer:
    def __init__(self, host, port, connections):
        self._host = host
        self._port = port 
        self._connections = connections
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
                    self.send_message_to_client(conn, pickle.dumps(data))
                # If two connections start game
                else:
                    self.game_loop()


    def send_message_to_client(self, conn, data):
        conn.send(data)

    def send_to_all(self, data):
        for conn in self._connections:
            conn.send(data)

    def display_welcome_and_champs(self):
        # Ask client to print welcome message
        data = {
            "CMD": "PRINTWELCOME"
        }
        self.send_to_all(pickle.dumps(data))

        # Need to send all champions to both clients
        champions = DBService.get_all_champs()

        data = {
            "CMD": "RECVCHAMPS",
            "Value": champions
        }
        self.send_to_all(pickle.dumps(data))

    def game_loop(self):
        self.display_welcome_and_champs()
        

        # # Ask first connection for champion
        # data = {
        #     "CMD": "CHOOSECHAMP",
        #     "Args": {
        #         "Color": "red",
        #         "Champions": champions,
        #         "player1": self._player1,
        #         "player2": self._player2
        #     }
        # }
        # self.send_message_to_client(self._connections[0], pickle.dumps(data))


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 7010
    serv = TNTServer(HOST, PORT, [])
    serv.start_up()
    serv.shut_down()








