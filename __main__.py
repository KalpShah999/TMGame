"""
Terminal Multiplayer RPG - Quick Launcher
This is a convenience script to quickly start either the server or client.
"""

import sys


def main():
    print("="*60)
    print("Terminal Multiplayer RPG")
    print("="*60)
    print("\nWhat would you like to run?")
    print("1. Game Server (host a game)")
    print("2. Game Client (join a game)")
    print("3. Exit")
    print("="*60)
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\nStarting game server...\n")
        from server_launcher import main
        # server = GameServer(host='0.0.0.0', port=5555)
        # server.start()
        main()
    
    elif choice == "2":
        print("\nStarting game client...\n")
        from game_client import main as client_main
        client_main()
    
    elif choice == "3":
        print("\nGoodbye!")
        sys.exit(0)
    
    else:
        print("\nInvalid choice. Please run the script again.")
        sys.exit(1)


if __name__ == "__main__":
    main()

