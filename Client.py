import socket
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
        while True:
            # Receive any message
            data = self._client.recv(4096).decode()
            # If there was no data, try again
            if not data:
                continue

            print(f"Data Received: {data}")
            command = data.split()[0]
            if (command == "MSG"):
                print(" ".join(data.split()[1:]))
            elif (command == "CMD"):
                print("Command received to print rubric")
                # Print champ rubric



if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 7002
    client = TNTClient(HOST, PORT)
    client.start_up()
    client.shut_down()
