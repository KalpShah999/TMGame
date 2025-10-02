# Terminal Multiplayer RPG

A text-based adventure RPG that supports multiple players in a shared world!

## Quick Start

**Quick start (recommended):**
```bash
python __main__.py
```
This gives you a menu to choose server or client.

**Or start components directly:**

Server:
```bash
python server_launcher.py
```

Client (menu-driven, RECOMMENDED):
```bash
python game_client_menu.py
```

Client (with action menus):
```bash
python game_client_interactive.py
```

Client (text only):
```bash
python game_client.py
```

## Features

- **Menu-driven interface** - Persistent menu that updates based on location/context
- **Arrow key navigation** - Navigate all menus with arrow keys (or type numbers/names)
- **Context-aware actions** - Menu shows only valid actions (available exits, combat when enemies present)
- **Multiplayer support** - Real-time gameplay with other players
- **Combat system** - Fight enemies with weapons and spells
- **Character progression** - Level up and become stronger
- **Multiple locations** - Explore different areas
- **Persistent save system** - Your progress is automatically saved
- **Player chat** - Communicate with other players

## Documentation

For detailed documentation, see the [`docs/`](docs/) folder:

- **[Main Documentation](docs/README.md)** - Complete game guide and features
- **[Save System Guide](docs/SAVE_SYSTEM.md)** - How to manage save files
- **[Interactive Menus](docs/MENU_SYSTEM.md)** - Arrow key navigation guide
- **[Help Menu Examples](docs/HELP_MENU_EXAMPLE.md)** - Command reference
- **[ASCII Changes](docs/EMOJI_TO_ASCII_CHANGES.md)** - Emoji to ASCII conversion notes

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## License

This is a learning project - feel free to modify, extend, and use it however you like!

Happy adventuring!

