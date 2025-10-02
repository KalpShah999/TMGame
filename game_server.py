"""
Terminal Multiplayer Game Server
Handles multiple client connections and manages the game world.
"""

import socket
import threading
import json
import random
import copy
import os
import signal
import sys
from datetime import datetime
from game_data import LOCATIONS, ENEMIES, WEAPONS, SPELLS, STARTING_STATS


class GameServer:
    def __init__(self, host='0.0.0.0', port=5555, save_file=None):
        self.host = host
        self.port = port
        self.server = None
        self.players = {}  # {username: player_data}
        self.client_sockets = {}  # {username: socket}
        self.lock = threading.Lock()
        self.save_file = save_file
        self.running = True
        self.saves_dir = "saves"
        
        # Create saves directory if it doesn't exist
        if not os.path.exists(self.saves_dir):
            os.makedirs(self.saves_dir)
        
        # Load game state if save file provided
        if save_file:
            self.load_game(save_file)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown_handler)
        signal.signal(signal.SIGTERM, self.shutdown_handler)
    
    def save_game(self, save_file=None):
        """Save the current game state to a .tms file."""
        if save_file is None:
            save_file = self.save_file
        
        if save_file is None:
            # Generate a default save file name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_file = f"world_{timestamp}.tms"
        
        save_path = os.path.join(self.saves_dir, save_file)
        
        # Prepare game state
        game_state = {
            "saved_at": datetime.now().isoformat(),
            "players": self.players,
            "server_info": {
                "host": self.host,
                "port": self.port
            }
        }
        
        try:
            with open(save_path, 'w') as f:
                json.dump(game_state, f, indent=2)
            print(f"[SAVE] Game state saved to {save_path}")
            return save_path
        except Exception as e:
            print(f"[ERROR] Failed to save game: {e}")
            return None
    
    def load_game(self, save_file):
        """Load game state from a .tms file."""
        save_path = os.path.join(self.saves_dir, save_file)
        
        if not os.path.exists(save_path):
            print(f"[ERROR] Save file not found: {save_path}")
            return False
        
        try:
            with open(save_path, 'r') as f:
                game_state = json.load(f)
            
            self.players = game_state.get("players", {})
            saved_at = game_state.get("saved_at", "unknown")
            
            print(f"[LOAD] Game state loaded from {save_path}")
            print(f"[LOAD] Save date: {saved_at}")
            print(f"[LOAD] Players loaded: {len(self.players)}")
            
            return True
        except Exception as e:
            print(f"[ERROR] Failed to load game: {e}")
            return False
    
    def shutdown_handler(self, signum, frame):
        """Handle graceful shutdown."""
        print("\n[SERVER] Shutting down gracefully...")
        
        # Save game state
        if self.players:
            if self.save_file:
                self.save_game(self.save_file)
            else:
                # Auto-generate save file name
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_file = f"autosave_{timestamp}.tms"
                self.save_game(save_file)
        
        # Notify all connected players
        self.broadcast("[SERVER] Server is shutting down. Your progress has been saved.")
        
        # Close all client connections
        with self.lock:
            for username, client_socket in list(self.client_sockets.items()):
                try:
                    client_socket.close()
                except:
                    pass
        
        # Close server socket
        if self.server:
            self.server.close()
        
        print("[SERVER] Shutdown complete.")
        sys.exit(0)
        
    def auto_save_loop(self):
        """Periodically save game state."""
        import time
        while self.running:
            time.sleep(300)  # Auto-save every 5 minutes
            if self.players and self.save_file:
                print("[AUTO-SAVE] Saving game state...")
                self.save_game()
    
    def start(self):
        """Start the game server."""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"[SERVER] Game server started on {self.host}:{self.port}")
        print(f"[SERVER] Waiting for players to connect...")
        
        # Start auto-save thread
        if self.save_file:
            auto_save_thread = threading.Thread(target=self.auto_save_loop)
            auto_save_thread.daemon = True
            auto_save_thread.start()
            print(f"[SERVER] Auto-save enabled (every 5 minutes)")
        
        while True:
            try:
                client_socket, address = self.server.accept()
                print(f"[SERVER] New connection from {address}")
                thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                thread.daemon = True
                thread.start()
            except Exception as e:
                print(f"[SERVER ERROR] {e}")
                break
    
    def handle_client(self, client_socket, address):
        """Handle individual client connection."""
        username = None
        try:
            # Request username
            self.send_message(client_socket, "Welcome to the Realm of Adventures!\nEnter your username: \n")
            username = self.receive_message(client_socket).strip()
            
            if not username:
                self.send_message(client_socket, "Invalid username. Disconnecting.\n")
                client_socket.close()
                return
            
            with self.lock:
                # Create new player or load existing
                if username not in self.players:
                    self.players[username] = copy.deepcopy(STARTING_STATS)
                    self.client_sockets[username] = client_socket
                    welcome_msg = f"\n[NEW PLAYER] Welcome, {username}! Your adventure begins...\n"
                else:
                    self.client_sockets[username] = client_socket
                    welcome_msg = f"\n[RETURNING PLAYER] Welcome back, {username}!\n"
            
            # Send messages outside the lock to avoid deadlock
            self.send_message(client_socket, welcome_msg)
            self.broadcast(f"[SERVER] {username} has joined the realm!", exclude=username)
            
            # Send initial status
            self.show_status(username)
            self.show_location(username)
            self.send_message(client_socket, "\n[TIP] Type 'help' to see the help menu with command categories.\n\n")
            
            # Main game loop for this client
            while True:
                command = self.receive_message(client_socket)
                if not command:
                    break
                
                self.process_command(username, command.strip().lower())
                
        except Exception as e:
            print(f"[ERROR] Client {address}: {e}")
        finally:
            if username:
                with self.lock:
                    if username in self.client_sockets:
                        del self.client_sockets[username]
                self.broadcast(f"[SERVER] {username} has left the realm.")
            client_socket.close()
            print(f"[SERVER] Connection closed: {address}")
    
    def send_message(self, client_socket, message):
        """Send message to a client."""
        try:
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"[ERROR] Failed to send message: {e}")
            raise
    
    def receive_message(self, client_socket):
        """Receive message from a client."""
        try:
            return client_socket.recv(4096).decode('utf-8')
        except:
            return None
    
    def send_to_player(self, username, message):
        """Send message to specific player."""
        if username in self.client_sockets:
            self.send_message(self.client_sockets[username], message)
    
    def broadcast(self, message, exclude=None):
        """Broadcast message to all connected players."""
        with self.lock:
            for username, client_socket in self.client_sockets.items():
                if username != exclude:
                    self.send_message(client_socket, message + "\n")
    
    def process_command(self, username, command):
        """Process player commands."""
        player = self.players[username]
        parts = command.split()
        
        if not parts:
            return
        
        cmd = parts[0]
        
        # Movement commands
        if cmd in ['north', 'south', 'east', 'west', 'n', 's', 'e', 'w']:
            direction_map = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west'}
            direction = direction_map.get(cmd, cmd)
            self.move_player(username, direction)
        
        # Combat commands
        elif cmd == 'attack':
            self.attack(username, parts)
        elif cmd == 'cast':
            self.cast_spell(username, parts)
        
        # Information commands
        elif cmd == 'status':
            self.show_status(username)
        elif cmd == 'look':
            self.show_location(username)
        elif cmd == 'inventory' or cmd == 'inv':
            self.show_inventory(username)
        elif cmd == 'players':
            self.show_players(username)
        
        # Shop commands
        elif cmd == 'shop':
            self.show_shop(username)
        elif cmd == 'buy':
            self.buy_item(username, parts)
        
        # Communication
        elif cmd == 'say':
            self.player_say(username, ' '.join(parts[1:]))
        
        # Help
        elif cmd == 'help':
            if len(parts) > 1:
                # Help with category
                self.show_help(username, parts[1])
            else:
                # Show help menu
                self.show_help(username)
        
        else:
            self.send_to_player(username, "Unknown command. Type 'help' for available commands.\n")
    
    def move_player(self, username, direction):
        """Move player to a new location."""
        player = self.players[username]
        current_loc = LOCATIONS[player['location']]
        
        if direction in current_loc['exits']:
            new_location = current_loc['exits'][direction]
            player['location'] = new_location
            
            self.broadcast(f"[INFO] {username} traveled {direction}.", exclude=username)
            self.send_to_player(username, f"\nYou travel {direction}...\n")
            self.show_location(username)
        else:
            self.send_to_player(username, "You can't go that way!\n")
    
    def show_location(self, username):
        """Show current location details."""
        player = self.players[username]
        loc = LOCATIONS[player['location']]
        
        msg = f"\n{'='*60}\n"
        msg += f"LOCATION: {loc['name']}\n"
        msg += f"{'='*60}\n"
        msg += f"{loc['description']}\n\n"
        
        # Show exits
        exits = ', '.join(loc['exits'].keys())
        msg += f"Exits: {exits}\n"
        
        # Show other players here
        players_here = [p for p, data in self.players.items() 
                       if data['location'] == player['location'] and p != username]
        if players_here:
            msg += f"Players here: {', '.join(players_here)}\n"
        
        # Show enemies
        if loc['enemies']:
            msg += f"[!] Enemies: {', '.join([ENEMIES[e]['name'] for e in loc['enemies']])}\n"
        
        msg += f"{'='*60}\n"
        self.send_to_player(username, msg)
    
    def show_status(self, username):
        """Show player status."""
        player = self.players[username]
        weapon = WEAPONS[player['weapon']]
        
        msg = f"\n{'='*60}\n"
        msg += f"CHARACTER: {username} - Level {player['level']} Adventurer\n"
        msg += f"{'='*60}\n"
        msg += f"Health: {player['health']}/{player['max_health']}\n"
        msg += f"Mana: {player['mana']}/{player['max_mana']}\n"
        msg += f"EXP: {player['exp']}/{player['exp_to_level']}\n"
        msg += f"Gold: {player['gold']}\n"
        msg += f"Weapon: {weapon['name']} (Damage: {weapon['damage']})\n"
        msg += f"Spells: {len(player['spells'])}\n"
        msg += f"{'='*60}\n"
        
        self.send_to_player(username, msg)
    
    def show_inventory(self, username):
        """Show player inventory."""
        player = self.players[username]
        weapon = WEAPONS[player['weapon']]
        
        msg = f"\n{'='*60}\n"
        msg += f"INVENTORY\n"
        msg += f"{'='*60}\n"
        msg += f"Equipped Weapon: {weapon['name']} (Damage: {weapon['damage']})\n\n"
        
        if player['spells']:
            msg += "Known Spells:\n"
            for spell_id in player['spells']:
                spell = SPELLS[spell_id]
                msg += f"  - {spell['name']}: {spell['damage']} damage, {spell['mana_cost']} mana\n"
        else:
            msg += "No spells learned yet.\n"
        
        msg += f"{'='*60}\n"
        
        self.send_to_player(username, msg)
    
    def attack(self, username, parts):
        """Handle combat."""
        player = self.players[username]
        loc = LOCATIONS[player['location']]
        
        if not loc['enemies']:
            self.send_to_player(username, "There are no enemies here to fight!\n")
            return
        
        if len(parts) < 2:
            self.send_to_player(username, f"Usage: attack <enemy>\nAvailable: {', '.join(loc['enemies'])}\n")
            return
        
        enemy_type = parts[1]
        if enemy_type not in loc['enemies']:
            self.send_to_player(username, "That enemy is not here!\n")
            return
        
        # Combat!
        enemy = copy.deepcopy(ENEMIES[enemy_type])
        weapon = WEAPONS[player['weapon']]
        
        self.send_to_player(username, f"\n[COMBAT] Battle started with {enemy['name']}!\n")
        self.broadcast(f"[COMBAT] {username} is fighting a {enemy['name']}!", exclude=username)
        
        while enemy['health'] > 0 and player['health'] > 0:
            # Player attacks
            player_damage = weapon['damage'] + random.randint(-2, 5)
            enemy['health'] -= player_damage
            
            self.send_to_player(username, f"You strike for {player_damage} damage! Enemy health: {max(0, enemy['health'])}\n")
            
            if enemy['health'] <= 0:
                break
            
            # Enemy attacks
            enemy_damage = enemy['damage'] + random.randint(-2, 3)
            player['health'] -= enemy_damage
            
            self.send_to_player(username, f"Enemy hits you for {enemy_damage} damage! Your health: {max(0, player['health'])}\n")
        
        # Combat resolution
        if player['health'] > 0:
            player['exp'] += enemy['exp_reward']
            player['gold'] += enemy['gold_reward']
            
            self.send_to_player(username, f"\n[VICTORY] You gained {enemy['exp_reward']} EXP and {enemy['gold_reward']} gold!\n")
            self.send_to_player(username, f"\n[INFO] You now have {player['health']} health, {player['mana']} mana, {player['gold']} gold, and {player['exp']} EXP.\n")
            self.broadcast(f"[COMBAT] {username} defeated a {enemy['name']}!", exclude=username)
            
            # Check for level up
            if player['exp'] >= player['exp_to_level']:
                self.level_up(username)
        else:
            player['health'] = player['max_health'] // 2
            player['location'] = 'town_square'
            player['gold'] = max(0, player['gold'] - 20)
            
            self.send_to_player(username, "\n[DEFEAT] You were defeated! You wake up in the town square with reduced gold.\n")
            self.broadcast(f"[COMBAT] {username} was defeated by a {enemy['name']}!", exclude=username)
            self.show_location(username)
    
    def cast_spell(self, username, parts):
        """Cast a spell."""
        player = self.players[username]
        
        if len(parts) < 2:
            self.send_to_player(username, "Usage: cast <spell_name>\n")
            return
        
        spell_id = parts[1]
        if spell_id not in player['spells']:
            self.send_to_player(username, "You don't know that spell!\n")
            return
        
        spell = SPELLS[spell_id]
        
        if player['mana'] < spell['mana_cost']:
            self.send_to_player(username, f"Not enough mana! Need {spell['mana_cost']}, have {player['mana']}\n")
            return
        
        player['mana'] -= spell['mana_cost']
        
        # Healing spell
        if spell['damage'] < 0:
            heal_amount = abs(spell['damage'])
            player['health'] = min(player['max_health'], player['health'] + heal_amount)
            self.send_to_player(username, f"[SPELL] You cast {spell['name']} and restore {heal_amount} health!\n")
        else:
            # Attack spell (similar to attack command but with spell damage)
            loc = LOCATIONS[player['location']]
            if not loc['enemies']:
                self.send_to_player(username, "There are no enemies here!\n")
                player['mana'] += spell['mana_cost']  # Refund mana
                return
            
            enemy_type = loc['enemies'][0]
            enemy = copy.deepcopy(ENEMIES[enemy_type])
            damage = spell['damage'] + random.randint(-3, 3)
            
            self.send_to_player(username, f"[SPELL] You cast {spell['name']} for {damage} damage!\n")
            self.broadcast(f"[MAGIC] {username} casts {spell['name']}!", exclude=username)
    
    def level_up(self, username):
        """Level up a player."""
        player = self.players[username]
        player['level'] += 1
        player['exp'] = 0
        player['exp_to_level'] = int(player['exp_to_level'] * 1.5)
        player['max_health'] += 20
        player['health'] = player['max_health']
        player['max_mana'] += 10
        player['mana'] = player['max_mana']
        
        msg = f"\n*** LEVEL UP! You are now level {player['level']}! ***\n"
        msg += f"Max Health: +20 (now {player['max_health']})\n"
        msg += f"Max Mana: +10 (now {player['max_mana']})\n"
        
        self.send_to_player(username, msg)
        self.broadcast(f"[SERVER] {username} reached level {player['level']}!", exclude=username)
    
    def show_shop(self, username):
        """Show the shop."""
        player = self.players[username]
        current_weapon = player['weapon']
        player_spells = player['spells']
        player_gold = player['gold']
        
        msg = f"\n{'='*60}\n"
        msg += f"SHOP - Your Gold: {player_gold}\n"
        msg += f"{'='*60}\n\n"
        
        msg += "WEAPONS:\n"
        for weapon_id, weapon in WEAPONS.items():
            owned = "[EQUIPPED]" if weapon_id == current_weapon else ""
            affordable = "" if player_gold >= weapon['cost'] else "[TOO EXPENSIVE]"
            msg += f"  {weapon_id:20s} - {weapon['name']:25s} "
            msg += f"Dmg: {weapon['damage']:3d} | Cost: {weapon['cost']:4d} gold  "
            msg += f"{owned} {affordable}\n"
        
        msg += "\nSPELLS:\n"
        for spell_id, spell in SPELLS.items():
            owned = "[OWNED]" if spell_id in player_spells else ""
            affordable = "" if player_gold >= spell['cost'] else "[TOO EXPENSIVE]"
            effect = f"{spell['damage']} dmg" if spell['damage'] > 0 else f"+{abs(spell['damage'])} heal"
            msg += f"  {spell_id:20s} - {spell['name']:25s} "
            msg += f"{effect:10s} | Cost: {spell['cost']:4d} gold  "
            msg += f"{owned} {affordable}\n"
        
        msg += f"\n{'='*60}\n"
        msg += "Usage: buy <item_id>\n"
        msg += "Example: buy iron_sword  OR  buy fireball\n"
        msg += f"{'='*60}\n"
        
        self.send_to_player(username, msg)
    
    def buy_item(self, username, parts):
        """Buy an item from the shop."""
        player = self.players[username]
        
        if len(parts) < 2:
            self.send_to_player(username, "Usage: buy <item_id>\n")
            return
        
        item_id = parts[1]
        
        if item_id in WEAPONS:
            weapon = WEAPONS[item_id]
            if player['gold'] >= weapon['cost']:
                player['gold'] -= weapon['cost']
                player['weapon'] = item_id
                self.send_to_player(username, f"[OK] Purchased {weapon['name']}!\n")
            else:
                self.send_to_player(username, f"Not enough gold! Need {weapon['cost']}, have {player['gold']}\n")
        
        elif item_id in SPELLS:
            spell = SPELLS[item_id]
            if item_id in player['spells']:
                self.send_to_player(username, "You already know this spell!\n")
            elif player['gold'] >= spell['cost']:
                player['gold'] -= spell['cost']
                player['spells'].append(item_id)
                self.send_to_player(username, f"[OK] Learned {spell['name']}!\n")
            else:
                self.send_to_player(username, f"Not enough gold! Need {spell['cost']}, have {player['gold']}\n")
        else:
            self.send_to_player(username, "Item not found!\n")
    
    def show_players(self, username):
        """Show all connected players."""
        msg = f"\n{'='*60}\n"
        msg += "ONLINE PLAYERS\n"
        msg += f"{'='*60}\n"
        
        for player_name, player_data in self.players.items():
            if player_name in self.client_sockets:
                location = LOCATIONS[player_data['location']]['name']
                msg += f"  {player_name} - Level {player_data['level']} - {location}\n"
        
        msg += f"{'='*60}\n"
        self.send_to_player(username, msg)
    
    def player_say(self, username, message):
        """Player chat."""
        if message:
            self.broadcast(f"[{username}]: {message}", exclude=None)
        else:
            self.send_to_player(username, "Usage: say <message>\n")
    
    def show_help(self, username, category=None):
        """Show help message with categories."""
        if category is None:
            # Show category menu
            msg = f"\n{'='*60}\n"
            msg += "HELP MENU - Select a Category\n"
            msg += f"{'='*60}\n\n"
            msg += ">> [1] Movement     - How to navigate the world\n"
            msg += "   [2] Combat       - Fighting enemies and using spells\n"
            msg += "   [3] Information  - Checking stats and surroundings\n"
            msg += "   [4] Shopping     - Buying weapons and spells\n"
            msg += "   [5] Social       - Interacting with other players\n"
            msg += "   [6] All          - Show all commands\n\n"
            msg += f"{'='*60}\n"
            msg += "Type a number (1-6) or category name to see details\n"
            msg += "Example: help 2  OR  help combat\n"
            msg += f"{'='*60}\n"
        else:
            msg = self.get_help_category(category)
        
        self.send_to_player(username, msg)
    
    def get_help_category(self, category):
        """Get help text for a specific category."""
        category = category.lower()
        
        # Map numbers and names to categories
        category_map = {
            '1': 'movement', 'movement': 'movement',
            '2': 'combat', 'combat': 'combat',
            '3': 'information', 'info': 'information', 'information': 'information',
            '4': 'shopping', 'shop': 'shopping', 'shopping': 'shopping',
            '5': 'social', 'social': 'social',
            '6': 'all', 'all': 'all'
        }
        
        category = category_map.get(category, None)
        
        if category is None:
            return "Invalid category. Type 'help' to see available categories.\n"
        
        msg = f"\n{'='*60}\n"
        
        if category == 'movement' or category == 'all':
            msg += "MOVEMENT COMMANDS\n"
            msg += f"{'='*60}\n"
            msg += "  north / n    - Move north\n"
            msg += "  south / s    - Move south\n"
            msg += "  east / e     - Move east\n"
            msg += "  west / w     - Move west\n"
            if category != 'all':
                msg += f"{'='*60}\n"
            else:
                msg += "\n"
        
        if category == 'combat' or category == 'all':
            if category == 'all':
                msg += "COMBAT COMMANDS\n"
                msg += f"{'='*60}\n"
            msg += "  attack <enemy>  - Attack an enemy in your location\n"
            msg += "                    Example: attack goblin\n"
            msg += "  cast <spell>    - Cast a spell (requires mana)\n"
            msg += "                    Example: cast fireball\n"
            if category != 'all':
                msg += f"{'='*60}\n"
            else:
                msg += "\n"
        
        if category == 'information' or category == 'all':
            if category == 'all':
                msg += "INFORMATION COMMANDS\n"
                msg += f"{'='*60}\n"
            msg += "  status       - View your character stats\n"
            msg += "  look         - Look around your current location\n"
            msg += "  inventory    - View your inventory and equipment\n"
            msg += "  inv          - Shortcut for inventory\n"
            msg += "  players      - See all online players and locations\n"
            if category != 'all':
                msg += f"{'='*60}\n"
            else:
                msg += "\n"
        
        if category == 'shopping' or category == 'all':
            if category == 'all':
                msg += "SHOPPING COMMANDS\n"
                msg += f"{'='*60}\n"
            msg += "  shop            - View available weapons and spells\n"
            msg += "  buy <item_id>   - Purchase an item from the shop\n"
            msg += "                    Example: buy iron_sword\n"
            msg += "                    Example: buy fireball\n"
            if category != 'all':
                msg += f"{'='*60}\n"
            else:
                msg += "\n"
        
        if category == 'social' or category == 'all':
            if category == 'all':
                msg += "SOCIAL COMMANDS\n"
                msg += f"{'='*60}\n"
            msg += "  say <message>   - Send a message to all players\n"
            msg += "                    Example: say Hello everyone!\n"
            if category != 'all':
                msg += f"{'='*60}\n"
            else:
                msg += "\n"
        
        if category == 'all':
            msg += "OTHER COMMANDS\n"
            msg += f"{'='*60}\n"
            msg += "  help            - Show help menu\n"
            msg += "  help <category> - Show help for specific category\n"
            msg += "  quit / exit     - Disconnect from server\n"
            msg += f"{'='*60}\n"
        else:
            msg += "\nType 'help' to return to the help menu.\n"
        
        return msg


if __name__ == "__main__":
    # Basic server startup without menu (use server_launcher.py for menu)
    print("Starting server without save file selection...")
    print("Use server_launcher.py for save file menu.")
    server = GameServer(host='0.0.0.0', port=5555)
    server.start()

