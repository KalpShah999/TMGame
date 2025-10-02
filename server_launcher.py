#!/usr/bin/env python3
"""
Server Launcher with Save File Selection
Provides a terminal menu to select and load save files.
"""

import os
import sys
from datetime import datetime
from game_server import GameServer
from menu_utils import interactive_menu, clear_screen


def get_save_files():
    """Get list of all .tms save files."""
    saves_dir = "saves"
    if not os.path.exists(saves_dir):
        os.makedirs(saves_dir)
        return []
    
    files = [f for f in os.listdir(saves_dir) if f.endswith('.tms')]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(saves_dir, x)), reverse=True)
    return files


def display_save_file_info(filename):
    """Display information about a save file."""
    import json
    
    save_path = os.path.join("saves", filename)
    try:
        with open(save_path, 'r') as f:
            data = json.load(f)
        
        saved_at = data.get("saved_at", "Unknown")
        player_count = len(data.get("players", {}))
        
        # Get player names
        players = list(data.get("players", {}).keys())
        player_preview = ", ".join(players[:3])
        if len(players) > 3:
            player_preview += f" (+{len(players) - 3} more)"
        
        return {
            "saved_at": saved_at,
            "player_count": player_count,
            "players": player_preview if players else "None"
        }
    except:
        return None


def select_save_file():
    """Display menu and let user select a save file."""
    save_files = get_save_files()
    
    clear_screen()
    
    if not save_files:
        print("No save files found. Starting a new world...")
        return None
    
    # Build menu options
    options = []
    descriptions = []
    
    for filename in save_files:
        info = display_save_file_info(filename)
        options.append(filename)
        if info:
            desc = f"Saved: {info['saved_at']} | Players: {info['player_count']} ({info['players']})"
            descriptions.append(desc)
        else:
            descriptions.append("")
    
    # Add special options
    options.append("Start a new world")
    descriptions.append("Create a fresh world with no existing players")
    
    options.append("Quit")
    descriptions.append("Exit the launcher")
    
    # Show interactive menu
    selected_idx = interactive_menu(
        "Terminal Multiplayer RPG - Server Launcher",
        options,
        descriptions,
        show_indices=True
    )
    
    # Handle selection
    if selected_idx == -1 or selected_idx == len(options) - 1:  # Quit
        print("\nExiting...")
        sys.exit(0)
    elif selected_idx == len(options) - 2:  # New world
        return None
    else:
        selected = save_files[selected_idx]
        print(f"\n[OK] Selected: {selected}")
        return selected


def main():
    """Main launcher function."""
    # Select save file
    save_file = select_save_file()
    
    print()
    print("="*70)
    
    if save_file:
        print(f"Loading world from: {save_file}")
    else:
        print("Starting a new world!")
        # Create a default save file name for the new world
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_file = f"world_{timestamp}.tms"
        print(f"Save file will be: {save_file}")
    
    print("="*70)
    print()
    
    # Start the server
    try:
        server = GameServer(host='0.0.0.0', port=5555, save_file=save_file)
        server.start()
    except KeyboardInterrupt:
        print("\nServer interrupted by user.")
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

