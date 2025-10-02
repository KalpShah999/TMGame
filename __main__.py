"""
Terminal Multiplayer RPG - Quick Launcher
This is a convenience script to quickly start either the server or client.
"""

import sys
from menu_utils import interactive_menu, clear_screen


def main():
    clear_screen()
    
    options = [
        "Game Server (host a game)",
        "Game Client - Menu Driven (RECOMMENDED)",
        "Game Client - Interactive",
        "Game Client - Classic",
        "Exit"
    ]
    
    descriptions = [
        "Start the server with save file selection menu",
        "Persistent menu that updates based on location/context",
        "Action menus you can toggle in/out of",
        "Traditional text-only commands",
        "Exit the launcher"
    ]
    
    choice = interactive_menu(
        "Terminal Multiplayer RPG - Main Menu",
        options,
        descriptions,
        show_indices=True
    )
    
    if choice == 0:  # Server
        print("\nStarting game server...\n")
        from server_launcher import main as server_main
        server_main()
    
    elif choice == 1:  # Menu Client
        print("\nStarting menu-driven game client...\n")
        from game_client_menu import main as menu_client_main
        menu_client_main()
    
    elif choice == 2:  # Interactive Client
        print("\nStarting interactive game client...\n")
        from game_client_interactive import main as interactive_client_main
        interactive_client_main()
    
    elif choice == 3:  # Classic Client
        print("\nStarting classic game client...\n")
        from game_client import main as client_main
        client_main()
    
    elif choice == 4 or choice == -1:  # Exit
        print("\nGoodbye!")
        sys.exit(0)
    
    else:
        print("\nInvalid choice. Please run the script again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
