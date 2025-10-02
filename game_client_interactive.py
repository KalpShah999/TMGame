"""
Enhanced Interactive Game Client
Provides arrow key navigation for in-game menus and actions.
"""

import socket
import threading
import sys
import re
from menu_utils import interactive_menu, clear_screen


class InteractiveGameClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.client = None
        self.running = False
        self.pending_response = []
        self.response_complete = threading.Event()
        self.in_menu_mode = False
        
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
            
            # Enhanced command loop
            self.command_loop()
            
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            print(f"Make sure the server is running on {self.host}:{self.port}")
            sys.exit(1)
    
    def receive_messages(self):
        """Receive and display messages from the server."""
        while self.running:
            try:
                message = self.client.recv(4096).decode('utf-8')
                if message:
                    if self.in_menu_mode:
                        # Buffer the response
                        self.pending_response.append(message)
                    else:
                        # Display immediately
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
    
    def send_command(self, command):
        """Send command to server."""
        try:
            self.client.send(command.encode('utf-8'))
        except Exception as e:
            print(f"Error sending command: {e}")
            self.running = False
    
    def command_loop(self):
        """Enhanced command loop with menu interception."""
        import time
        
        print("\n[TIP] Press 'm' or 'menu' to open the action menu anytime!\n")
        
        while self.running:
            try:
                # Get user input
                user_input = input().strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    print("Disconnecting from server...")
                    self.running = False
                    break
                
                # Main action menu
                if user_input.lower() in ['m', 'menu', 'actions']:
                    self.show_action_menu()
                    continue
                
                # Check if this should trigger an interactive menu
                if self.should_show_menu(user_input):
                    self.handle_interactive_command(user_input)
                else:
                    # Send command directly to server
                    self.send_command(user_input)
            
            except KeyboardInterrupt:
                print("\nDisconnecting...")
                self.running = False
                break
            except Exception as e:
                print(f"Error: {e}")
        
        self.client.close()
        sys.exit(0)
    
    def should_show_menu(self, command):
        """Check if command should trigger interactive menu."""
        cmd = command.lower().strip()
        
        # Commands that benefit from menus
        menu_triggers = [
            'help',
            'h',
            '?',
        ]
        
        # Check for movement commands that could use menu
        if cmd in ['move', 'go', 'travel']:
            return True
        
        return cmd in menu_triggers
    
    def handle_interactive_command(self, command):
        """Handle commands with interactive menus."""
        cmd = command.lower().strip()
        
        if cmd in ['help', 'h', '?']:
            self.show_help_menu()
        elif cmd in ['move', 'go', 'travel']:
            self.show_movement_menu()
    
    def show_help_menu(self):
        """Show interactive help menu."""
        options = [
            "Movement",
            "Combat",
            "Information",
            "Shopping",
            "Social",
            "All Commands",
            "Back"
        ]
        
        descriptions = [
            "How to navigate the world",
            "Fighting enemies and using spells",
            "Checking stats and surroundings",
            "Buying weapons and spells",
            "Interacting with other players",
            "Show all available commands",
            "Return to game"
        ]
        
        choice = interactive_menu(
            "HELP MENU - What do you need help with?",
            options,
            descriptions,
            show_indices=True
        )
        
        if choice == -1 or choice == 6:  # Back
            return
        
        # Map choice to help command
        help_categories = ['movement', 'combat', 'information', 'shopping', 'social', 'all']
        if 0 <= choice < len(help_categories):
            # Send help command to server
            self.send_command(f"help {help_categories[choice]}")
    
    def show_action_menu(self):
        """Show main action menu with all game actions."""
        options = [
            "Movement",
            "Combat",
            "Magic",
            "Character Info",
            "Shop",
            "Social",
            "Help",
            "Back to Game"
        ]
        
        descriptions = [
            "Move to a different location",
            "Attack enemies",
            "Cast spells",
            "View status, inventory, and other players",
            "Buy weapons and spells",
            "Chat with other players",
            "View help and commands",
            "Return to typing commands"
        ]
        
        choice = interactive_menu(
            "ACTION MENU - What would you like to do?",
            options,
            descriptions,
            show_indices=True
        )
        
        if choice == -1 or choice == 7:  # Back
            return
        elif choice == 0:  # Movement
            self.show_movement_menu()
        elif choice == 1:  # Combat
            self.show_combat_menu()
        elif choice == 2:  # Magic
            self.show_magic_menu()
        elif choice == 3:  # Character Info
            self.show_info_menu()
        elif choice == 4:  # Shop
            self.send_command("shop")
        elif choice == 5:  # Social
            self.show_social_menu()
        elif choice == 6:  # Help
            self.show_help_menu()
    
    def show_movement_menu(self):
        """Show interactive movement menu."""
        options = [
            "North",
            "South", 
            "East",
            "West",
            "Look Around",
            "Back"
        ]
        
        descriptions = [
            "Move north",
            "Move south",
            "Move east",
            "Move west",
            "Examine your current location",
            "Return to action menu"
        ]
        
        choice = interactive_menu(
            "MOVEMENT - Where do you want to go?",
            options,
            descriptions,
            show_indices=True
        )
        
        if choice == -1 or choice == 5:  # Back
            return
        elif choice == 4:  # Look
            self.send_command("look")
        else:
            # Send movement command
            directions = ['north', 'south', 'east', 'west']
            if 0 <= choice < len(directions):
                self.send_command(directions[choice])
    
    def show_combat_menu(self):
        """Show combat menu."""
        print("\nEnter enemy name to attack (or press Enter to cancel): ")
        enemy = input("> ").strip()
        
        if enemy:
            self.send_command(f"attack {enemy}")
    
    def show_magic_menu(self):
        """Show magic/spells menu."""
        options = [
            "View Inventory (see known spells)",
            "Cast Spell (enter spell name)",
            "Back"
        ]
        
        descriptions = [
            "See what spells you know",
            "Cast a specific spell",
            "Return to action menu"
        ]
        
        choice = interactive_menu(
            "MAGIC - What would you like to do?",
            options,
            descriptions,
            show_indices=True
        )
        
        if choice == 0:
            self.send_command("inventory")
        elif choice == 1:
            print("\nEnter spell name to cast: ")
            spell = input("> ").strip()
            if spell:
                self.send_command(f"cast {spell}")
    
    def show_info_menu(self):
        """Show character information menu."""
        options = [
            "Status",
            "Inventory",
            "Online Players",
            "Look Around",
            "Back"
        ]
        
        descriptions = [
            "View your character stats",
            "View your equipment and spells",
            "See who else is online",
            "Examine your current location",
            "Return to action menu"
        ]
        
        choice = interactive_menu(
            "CHARACTER INFO - What do you want to see?",
            options,
            descriptions,
            show_indices=True
        )
        
        commands = ['status', 'inventory', 'players', 'look']
        if choice >= 0 and choice < len(commands):
            self.send_command(commands[choice])
    
    def show_social_menu(self):
        """Show social/chat menu."""
        print("\nEnter message to send to all players (or press Enter to cancel): ")
        message = input("> ").strip()
        
        if message:
            self.send_command(f"say {message}")


def main():
    """Main function to run the interactive game client."""
    print("="*60)
    print("Terminal Multiplayer RPG - Interactive Client")
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
    print("\n[TIP] This client has enhanced menus - try typing 'help'!")
    print()
    
    # Create and connect client
    client = InteractiveGameClient(host, port)
    client.connect()


if __name__ == "__main__":
    main()

