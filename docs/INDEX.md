# Documentation Index

Welcome to the Terminal Multiplayer RPG documentation!

## Documentation Files

### [README.md](README.md)
**Main Documentation** - Complete game guide with all features, commands, and gameplay tips.

Contains:
- Game features and world description
- Installation and setup instructions
- Complete command reference
- Multiplayer setup guide
- Gameplay tips and examples
- Technical architecture details

### [SAVE_SYSTEM.md](SAVE_SYSTEM.md)
**Save System Guide** - Everything about saving and loading game state.

Contains:
- How the save system works
- Save file format and structure
- Managing and editing save files
- Backup and sharing worlds
- Troubleshooting save issues
- Advanced usage examples

### [HELP_MENU_EXAMPLE.md](HELP_MENU_EXAMPLE.md)
**Help Menu Reference** - Interactive help system examples.

Contains:
- Help menu navigation
- Category breakdowns
- Command examples
- Usage patterns

### [EMOJI_TO_ASCII_CHANGES.md](EMOJI_TO_ASCII_CHANGES.md)
**ASCII Conversion Notes** - Reference for emoji to ASCII replacements.

Contains:
- Complete list of emoji replacements
- Before/after examples
- ASCII tag reference
- Design rationale

## Quick Links

**Getting Started:**
1. Read [README.md](README.md) sections 1-3 for setup
2. Start with the Quick Start guide
3. Use in-game `help` command for commands

**For Server Admins:**
1. Check [SAVE_SYSTEM.md](SAVE_SYSTEM.md) for save management
2. Use `server_launcher.py` for save file selection

**For Players:**
1. Use `help` command in-game
2. Refer to [HELP_MENU_EXAMPLE.md](HELP_MENU_EXAMPLE.md) for command reference

**For Developers:**
1. See [README.md](README.md) "Technical Details" section
2. Check [EMOJI_TO_ASCII_CHANGES.md](EMOJI_TO_ASCII_CHANGES.md) for UI conventions

## Project Structure

```
TMGame/
├── docs/                    # Documentation (you are here!)
│   ├── INDEX.md            # This file
│   ├── README.md           # Main documentation
│   ├── SAVE_SYSTEM.md      # Save system guide
│   ├── HELP_MENU_EXAMPLE.md # Help menu reference
│   └── EMOJI_TO_ASCII_CHANGES.md # ASCII conversion notes
├── saves/                   # Save files (.tms)
├── game_server.py          # Game server
├── game_client.py          # Game client
├── server_launcher.py      # Server launcher with save selection
├── game_data.py            # Game content (locations, enemies, items)
├── __main__.py             # Entry point
└── requirements.txt        # Dependencies (none needed!)
```

## Need Help?

- **In-game help**: Type `help` in the game
- **Server issues**: Check [README.md](README.md) Troubleshooting section
- **Save problems**: See [SAVE_SYSTEM.md](SAVE_SYSTEM.md) Troubleshooting

Enjoy your adventure!

