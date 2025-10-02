#!/usr/bin/env python3
"""
Server Launcher with Save File Selection
Provides a terminal menu to select and load save files.
"""

import os
import sys
from datetime import datetime
from game_server import GameServer


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
    
    print("="*70)
    print("🎮 Terminal Multiplayer RPG - Server Launcher")
    print("="*70)
    print()
    
    if not save_files:
        print("No save files found. Starting a new world...")
        return None
    
    print("Available save files:")
    print()
    
    # Display save files with details
    for i, filename in enumerate(save_files, 1):
        info = display_save_file_info(filename)
        print(f"  [{i}] {filename}")
        if info:
            print(f"      Saved: {info['saved_at']}")
            print(f"      Players: {info['player_count']} ({info['players']})")
        print()
    
    print(f"  [N] Start a new world")
    print(f"  [Q] Quit")
    print()
    print("="*70)
    
    while True:
        choice = input("\nSelect a save file (number, N for new, Q to quit): ").strip().upper()
        
        if choice == 'Q':
            print("Exiting...")
            sys.exit(0)
        
        if choice == 'N':
            return None
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(save_files):
                selected = save_files[index]
                print(f"\n✓ Selected: {selected}")
                return selected
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(save_files)}, N, or Q.")
        except ValueError:
            print("Invalid input. Please enter a number, N, or Q.")


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

