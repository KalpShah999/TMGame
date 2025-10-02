"""
Menu-Driven Game Client
Persistent menu interface that updates based on game state.
Server sends structured data, client renders context-aware menus.
"""

import socket
import threading
import sys
import json
import time
from menu_utils import interactive_menu, clear_screen


class MenuGameClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.client = None
        self.running = False
        self.game_state = {}
        self.menu_options = []
        self.menu_descriptions = []
        self.state_lock = threading.Lock()
        self.awaiting_response = False
        
    def connect(self):
        """Connect to the game server."""
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, self.port))
            self.running = True
            
            clear_screen()
            print("="*60)
            print("Connected to game server!")
            print("="*60)
            
            # Start thread to receive messages from server
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Wait for initial game state
            time.sleep(1)
            
            # Main menu loop
            self.menu_loop()
            
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            print(f"Make sure the server is running on {self.host}:{self.port}")
            sys.exit(1)
    
    def receive_messages(self):
        """Receive messages from server."""
        buffer = ""
        while self.running:
            try:
                data = self.client.recv(4096).decode('utf-8')
                if data:
                    buffer += data
                    
                    # Try to parse game state updates
                    if "###STATE_UPDATE###" in buffer:
                        parts = buffer.split("###STATE_UPDATE###")
                        for part in parts[:-1]:
                            self.parse_state_update(part)
                        buffer = parts[-1]
                    else:
                        # Regular text message - display it
                        print(data, end='', flush=True)
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
    
    def parse_state_update(self, data):
        """Parse game state update from server."""
        try:
            # For now, we'll work with text responses
            # In production, this would parse JSON
            with self.state_lock:
                self.game_state['last_update'] = data
                self.awaiting_response = False
        except:
            pass
    
    def send_command(self, command):
        """Send command to server."""
        try:
            self.client.send(command.encode('utf-8'))
            self.awaiting_response = True
        except Exception as e:
            print(f"Error sending command: {e}")
            self.running = False
    
    def build_menu_from_state(self):
        """Build menu options based on current game state."""
        options = []
        descriptions = []
        
        # Parse last server message to determine context
        last_msg = self.game_state.get('last_update', '')
        
        # Check for available exits in last message
        available_exits = []
        if 'Exits:' in last_msg:
            # Extract exits from message
            try:
                exits_line = [line for line in last_msg.split('\n') if 'Exits:' in line][0]
                exits_str = exits_line.split('Exits:')[1].strip()
                available_exits = [e.strip() for e in exits_str.split(',')]
            except:
                # Default to all directions if can't parse
                available_exits = ['north', 'south', 'east', 'west']
        
        # Check for enemies
        has_enemies = 'Enemies:' in last_msg or '[!] Enemies' in last_msg
        
        # MOVEMENT OPTIONS (based on available exits or all directions)
        movement_dirs = ['north', 'south', 'east', 'west']
        if available_exits:
            for direction in movement_dirs:
                if direction in available_exits:
                    options.append(f"Move {direction.capitalize()}")
                    descriptions.append(f"Travel {direction}")
        else:
            # Show all directions if we haven't looked yet
            for direction in movement_dirs:
                options.append(f"Move {direction.capitalize()}")
                descriptions.append(f"Travel {direction}")
        
        # LOOK AROUND (always available)
        options.append("Look Around")
        descriptions.append("Examine your current location")
        
        # COMBAT OPTIONS (only if enemies present)
        if has_enemies:
            options.append("Attack Enemy")
            descriptions.append("Fight an enemy in this location")
            
            options.append("Cast Spell")
            descriptions.append("Use magic against enemies")
        
        # CHARACTER INFO
        options.append("View Status")
        descriptions.append("Check your health, level, and stats")
        
        options.append("View Inventory")
        descriptions.append("See your equipment and spells")
        
        # SHOP (always available - can be used anywhere)
        options.append("Shop")
        descriptions.append("Browse and buy items")
        
        # SOCIAL
        options.append("See Players")
        descriptions.append("View who's online")
        
        options.append("Send Message")
        descriptions.append("Chat with other players")
        
        # HELP & SYSTEM
        options.append("Help")
        descriptions.append("View game commands")
        
        options.append("Quit Game")
        descriptions.append("Disconnect from server")
        
        return options, descriptions
    
    def menu_loop(self):
        """Main menu loop - persistent menu that updates based on context."""
        while self.running:
            try:
                # Build menu based on current state
                options, descriptions = self.build_menu_from_state()
                
                # Show menu
                choice = interactive_menu(
                    "GAME ACTIONS - What would you like to do?",
                    options,
                    descriptions,
                    show_indices=True
                )
                
                if choice == -1 or choice == len(options) - 1:  # Quit
                    print("\nDisconnecting...")
                    self.running = False
                    break
                
                # Map choice to command
                command = self.map_choice_to_command(choice, options)
                
                if command:
                    # Send command to server
                    self.send_command(command)
                    
                    # Wait a moment for response
                    time.sleep(0.5)
                    
                    # Menu will refresh with new context
            
            except KeyboardInterrupt:
                print("\nDisconnecting...")
                self.running = False
                break
            except Exception as e:
                print(f"Error in menu loop: {e}")
                time.sleep(1)
        
        self.client.close()
        sys.exit(0)
    
    def map_choice_to_command(self, choice, options):
        """Map menu choice to server command."""
        option = options[choice].lower()
        
        # Movement - extract direction
        if option.startswith('move '):
            direction = option.split('move ')[1]
            return direction
        
        # Information
        elif 'look around' in option:
            return 'look'
        elif 'view status' in option:
            return 'status'
        elif 'view inventory' in option:
            return 'inventory'
        elif 'see players' in option:
            return 'players'
        
        # Combat
        elif 'attack enemy' in option:
            clear_screen()
            print("\n" + "="*60)
            print("Enter enemy name to attack (or press Enter to cancel):")
            print("Examples: goblin, wolf, skeleton")
            print("="*60)
            enemy = input("> ").strip()
            if enemy:
                return f'attack {enemy}'
            return None
        
        # Magic
        elif 'cast spell' in option:
            clear_screen()
            print("\n" + "="*60)
            print("Enter spell name to cast (or press Enter to cancel):")
            print("Examples: fireball, heal, lightning")
            print("="*60)
            spell = input("> ").strip()
            if spell:
                return f'cast {spell}'
            return None
        
        # Shop
        elif 'shop' in option:
            return 'shop'
        
        # Social
        elif 'send message' in option:
            clear_screen()
            print("\n" + "="*60)
            print("Enter message to send to all players:")
            print("="*60)
            message = input("> ").strip()
            if message:
                return f'say {message}'
            return None
        
        # Help
        elif 'help' in option:
            return 'help'
        
        return None


def main():
    """Main function to run the menu-driven client."""
    clear_screen()
    print("="*60)
    print("Terminal Multiplayer RPG - Menu Client")
    print("="*60)
    print()
    
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
    print("\n[INFO] This client uses a persistent menu interface!")
    print("[INFO] Select actions with arrow keys - menu updates automatically!\n")
    
    input("Press Enter to continue...")
    
    # Create and connect client
    client = MenuGameClient(host, port)
    client.connect()


if __name__ == "__main__":
    main()

