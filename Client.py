import socket
import pickle
import team_local_tactics as TLT

class TNTClient:

    def __init__(self, host, port):
        self._host = host 
        self._port = port 

    def start_up(self):
        # Create socket
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to server
        self._client.connect((self._host, self._port))
        # Start listening to incoming messages
        self.listen_for_messages() 

    def shut_down(self):
        self._client.close()
    
    def listen_for_messages(self):
        while True:

            # Try to recv data
            data = self._client.recv(2048)

            # Continue if no data
            if not data:
                continue

            # Load data with pickle
            data = pickle.loads(data)


            # Match commands
            match data["CMD"]:
                case "MSG":
                    print(data["Value"])
                case "PRINTWELCOME":
                    TLT.print_welcome_msg()
                case "RECVCHAMPS":
                    TLT.print_available_champs(data["Value"])
                case "CHOOSECHAMP":
                    args = data["Args"]
                    chosen_champion = TLT.input_champion(args["playername"], args["color"], args["champions"], args["player1list"], args["player2list"])
                    # Send choice back to server
                    self._client.send(chosen_champion.encode())
                case "PLAYERCHOSE":
                    # Print the other players champ choice
                    TLT.print_player_choice(data["Args"]["playernumber"], data["Args"]["champion"])
                case "PRINTMATCH":
                    TLT.print_match_summary(data["Value"])






if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 7017
    client = TNTClient(HOST, PORT)
    client.start_up()
    client.shut_down()
