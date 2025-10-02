"""
Terminal Multiplayer Game Client
Connects to the game server and allows players to interact with the game.
"""

import socket
import threading
import sys


class GameClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.client = None
        self.running = False
    
    def connect(self):
        """Connect to the game server."""
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, self.port))
            self.running = True
            
            print("="*60)
            print("Connected to game server!")
            print("="*60)
            
            # Start thread to receive messages from server
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Send messages to server
            self.send_messages()
            
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            print(f"Make sure the server is running on {self.host}:{self.port}")
            sys.exit(1)
    
    def receive_messages(self):
        """Receive and display messages from the server."""
        while self.running:
            try:
                print(">>> ", end='', flush=True)
                message = self.client.recv(4096).decode('utf-8')
                if message:
                    print(message, end='', flush=True)
                else:
                    print("\n[DISCONNECTED] Connection to server lost.")
                    self.running = False
                    break
            except Exception as e:
                if self.running:
                    print(f"\n[ERROR] Connection error: {e}")
                    self.running = False
                break
        
        self.client.close()
        sys.exit(0)
    
    def send_messages(self):
        """Send player commands to the server."""
        while self.running:
            try:
                message = input()
                if message.lower() == 'quit' or message.lower() == 'exit':
                    print("Disconnecting from server...")
                    self.running = False
                    break
                
                self.client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message: {e}")
                break
        
        self.client.close()
        sys.exit(0)


def main():
    """Main function to run the game client."""
    print("="*60)
    print("Terminal Multiplayer RPG - Client")
    print("="*60)
    
    # Get server connection details
    host = input("Enter server IP (press Enter for localhost): ").strip()
    if not host:
        host = 'localhost'
    
    port_input = input("Enter server port (press Enter for 5555): ").strip()
    if not port_input:
        port = 5555
    else:
        try:
            port = int(port_input)
        except ValueError:
            print("Invalid port. Using default 5555.")
            port = 5555
    
    print(f"\nConnecting to {host}:{port}...")
    
    # Create and connect client
    client = GameClient(host, port)
    client.connect()


if __name__ == "__main__":
    main()

