import socket 

class TNTServer:
    def __init__(self, host, port, connections):
        self._host = host
        self._port = port 
        self._connections = connections

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
                    self.send_message_to_client(conn, "MSG Waiting for other player.")
                # If two connections start game
                else:
                    self.game_loop()


    def send_message_to_client(self, conn, msg):
        conn.send(msg.encode())

    def send_to_all(self, msg):
        for conn in self._connections:
            conn.send(msg)

    def game_loop(self):
        # Start by telling client to print champion rubric
        self.send_to_all("CMD PRINT CHAMP_RUBRIC".encode())


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 7002
    serv = TNTServer(HOST, PORT, [])
    serv.start_up()
    serv.shut_down()



