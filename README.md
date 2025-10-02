# Terminal Multiplayer RPG Game

A text-based adventure RPG that supports multiple players in a shared world! Explore locations, battle enemies, level up, learn spells, and chat with other players in real-time.

## Features

🎮 **Multiplayer** - Multiple players can connect and play in the same world simultaneously  
🗺️ **Multiple Locations** - Explore different areas from town squares to dragon peaks  
⚔️ **Combat System** - Fight various enemies with weapons and spells  
✨ **Magic System** - Learn and cast different spells  
📈 **Leveling System** - Gain experience, level up, and become stronger  
💰 **Economy** - Earn gold and buy better weapons and spells  
💬 **Chat** - Communicate with other players in real-time  

## Game World

### Locations
- **Town Square** - Safe starting area with access to all regions
- **Dark Forest** - Dangerous woods filled with goblins and wolves
- **Haunted Grove** - Eerie area with ghosts and wraiths
- **Mountain Path** - Steep paths with trolls
- **Dragon's Peak** - The ultimate challenge - face the ancient dragon!
- **Peaceful Riverside** - Safe place to rest
- **Ancient Ruins** - Explore ruins with skeletons and stone guardians

### Enemies
From weakest to strongest:
- Wolves and Goblins (beginner)
- Skeletons and Ghosts (intermediate)
- Trolls and Wraiths (advanced)
- Stone Guardians (expert)
- Ancient Dragon (legendary)

### Weapons
- Rusty Sword (starter)
- Iron Sword
- Steel Sword
- Enchanted Blade
- Legendary Dragon Slayer

### Spells
- Fireball
- Ice Shard
- Lightning Bolt
- Heal
- Meteor Strike

## Installation & Setup

### Requirements
- Python 3.6 or higher
- No external libraries needed (uses only Python standard library)

### Running the Game

#### 1. Start the Server

You have two options for starting the server:

**Option A: With Save File Menu (Recommended)**

```bash
python server_launcher.py
```

This will show a menu where you can:
- Load an existing save file
- Start a new world
- View save file details (player count, save date, etc.)

**Option B: Quick Start Without Menu**

```bash
python game_server.py
```

This starts a new world without the save file selection menu.

The server will start on `0.0.0.0:5555` by default, accepting connections from any IP address.

**Note:** If you want to host for friends over the internet, you'll need to:
- Forward port 5555 on your router
- Share your public IP address with players
- Or use a service like ngrok to expose your local server

#### 2. Connect Clients

Players can connect using the client:

```bash
python game_client.py
```

When prompted:
- **For local testing:** Use `localhost` as the server IP
- **For LAN play:** Use the server's local IP (e.g., `192.168.1.100`)
- **For internet play:** Use the server's public IP or ngrok URL
- **Port:** Use `5555` (default) or whatever port you configured

#### 3. Create Your Character

When you connect, you'll be prompted to enter a username. This will be your character name in the game!

## How to Play

### Movement Commands
- `north` or `n` - Move north
- `south` or `s` - Move south
- `east` or `e` - Move east
- `west` or `w` - Move west

### Combat Commands
- `attack <enemy>` - Attack an enemy in your location
  - Example: `attack goblin`
- `cast <spell>` - Cast a spell
  - Example: `cast fireball`

### Information Commands
- `status` - View your character stats
- `look` - Look around your current location
- `inventory` or `inv` - View your inventory
- `players` - See all online players

### Shopping Commands
- `shop` - View available weapons and spells
- `buy <item_id>` - Purchase an item
  - Example: `buy iron_sword`
  - Example: `buy fireball`

### Social Commands
- `say <message>` - Chat with other players
  - Example: `say Hello everyone!`

### Other Commands
- `help` - Display categorized help menu
- `help <category>` - Show help for specific category
  - Example: `help 2` or `help combat`
  - Categories: Movement, Combat, Information, Shopping, Social
- `quit` or `exit` - Disconnect from the game

## Gameplay Tips

1. **Start Safe** - Begin in the Town Square and explore the Riverside first
2. **Earn Gold** - Fight weaker enemies (goblins, wolves) to earn gold
3. **Upgrade Equipment** - Buy better weapons and spells at the shop
4. **Level Up** - Gain experience to increase your health and mana
5. **Team Up** - Use the `players` command to see where others are and team up!
6. **Strategic Combat** - Higher level areas have stronger enemies but better rewards
7. **Use Spells Wisely** - Manage your mana; use the heal spell when needed

## Example Gameplay Session

```
> status
⚔️  Hero - Level 1 Adventurer
❤️  Health: 100/100
✨ Mana: 50/50
⭐ EXP: 0/50
💰 Gold: 50

> look
📍 Town Square
A bustling town square with merchants and travelers.
Exits: north, south, east, west

> north
You travel north...

📍 Dark Forest
A dense, dark forest. Strange sounds echo through the trees.
Exits: south, east
⚔️  Enemies: Goblin, Wolf

> attack goblin
⚔️  Combat started with Goblin!
You strike for 8 damage! Enemy health: 22
Enemy hits you for 6 damage! Your health: 94
...
🎉 Victory! You gained 15 EXP and 10 gold!

> status
⚔️  Hero - Level 1 Adventurer
❤️  Health: 94/100
💰 Gold: 60

> shop
🏪 SHOP
WEAPONS:
  iron_sword: Iron Sword - 12 damage - 50 gold

> buy iron_sword
✅ Purchased Iron Sword!

> say I just got an iron sword!
[Hero]: I just got an iron sword!
```

## Multiplayer Features

- **Shared World** - All players exist in the same world simultaneously
- **See Other Players** - Use `look` to see who else is in your location
- **Player Tracking** - Use `players` to see all online players and their locations
- **Global Chat** - Use `say` to communicate with everyone
- **Shared Notifications** - See when players join, leave, level up, or defeat enemies

## Save System

### How Saves Work

The game features an automatic save system that preserves player progress:

- **Save Files** - All saves are stored in the `saves/` directory as `.tms` files (Terminal Multiplayer Save)
- **Format** - Save files use JSON format, making them human-readable and easy to edit
- **Auto-Save** - Game automatically saves every 5 minutes
- **Graceful Shutdown** - Pressing `Ctrl+C` saves the game before shutting down

### Save File Contents

Each `.tms` file contains:
- All player data (stats, inventory, location, etc.)
- Timestamp of when it was saved
- Server configuration

Example save file structure:
```json
{
  "saved_at": "2025-10-02T14:30:45",
  "players": {
    "Hero": {
      "health": 120,
      "level": 5,
      "location": "dark_forest",
      ...
    }
  },
  "server_info": {
    "host": "0.0.0.0",
    "port": 5555
  }
}
```

### Managing Save Files

- **View Saves** - Use `server_launcher.py` to see all available saves
- **Load Save** - Select from the menu when starting the server
- **Edit Saves** - Save files are JSON, so you can edit them manually if needed
- **Backup** - Simply copy `.tms` files from the `saves/` directory

## Technical Details

### Architecture
- **Server** (`game_server.py`) - Handles all game logic and manages player connections
- **Client** (`game_client.py`) - Provides the terminal interface for players
- **Game Data** (`game_data.py`) - Contains all game content (locations, enemies, items)
- **Server Launcher** (`server_launcher.py`) - Save file selection menu

### Networking
- Uses TCP sockets for reliable communication
- Multi-threaded server handles multiple concurrent connections
- Each player connection runs in its own thread

### Data Persistence
- Player data is saved to `.tms` files in JSON format
- Automatic periodic saves every 5 minutes
- Graceful shutdown saves on Ctrl+C
- Save files persist across server restarts

## Future Enhancement Ideas

- Add more locations, enemies, and items
- Implement a quest system
- Add player-vs-player combat
- Create character classes (warrior, mage, rogue)
- Add equipment slots (armor, accessories)
- Implement a party/group system
- Add rare item drops
- Create boss battles requiring multiple players
- Add a trade system between players

## Troubleshooting

**Can't connect to server?**
- Make sure the server is running first
- Check that you're using the correct IP address and port
- For internet play, ensure port forwarding is configured correctly
- Check firewall settings

**Server crashes?**
- Check that no other program is using port 5555
- Try running with sudo/admin privileges if needed
- Check Python version (3.6+ required)

**Connection lost?**
- Server may have crashed or restarted
- Network connection may be unstable
- Simply reconnect with the client

## License

This is a learning project - feel free to modify, extend, and use it however you like!

## Contributing

This is a starter project! Feel free to:
- Add new features
- Create more content (locations, enemies, items)
- Improve the combat system
- Add better error handling
- Implement data persistence
- Enhance the UI with colors and ASCII art

Have fun and happy adventuring! ⚔️✨

