import socket
import pickle
import team_local_tactics

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
        receiving_champs = False
        while True:
            # Check if rceiving champions data
            if (receiving_champs):
                data = self._client.recv(2048)
                dedcoded = pickle.loads(data)
                receiving_champs = False
                # Print rubric
                team_local_tactics.print_available_champs(dedcoded)
                


            # Receive any message
            data = self._client.recv(4096).decode()
            # If there was no data, try again
            if not data:
                continue

            
            
            command = data.split()[0]
            if (command == "MSG"):
                print(" ".join(data.split()[1:]))
            elif (command == "CMD"):
                print("Command received to print rubric")
                # Print champ rubric
            elif (command == "RECVCHAMPS"):
                # Next message is champ dictionary
                print("Received recvchamps")
                receiving_champs = True



if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 7008
    client = TNTClient(HOST, PORT)
    client.start_up()
    client.shut_down()
