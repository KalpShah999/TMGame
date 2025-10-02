# Interactive Menu System

The game now features an interactive menu system with arrow key navigation!

## Features

### Dual Input Methods

You can navigate menus in TWO ways:

1. **Arrow Keys** (recommended)
   - Use ↑/↓ arrow keys to highlight options
   - Press ENTER to select the highlighted option
   - Visual feedback with `>>` indicator

2. **Type Input** (traditional)
   - Type the number of the option (e.g., `1`, `2`, `3`)
   - Type the name of the option (e.g., `combat`, `shop`)
   - Works alongside arrow key navigation

### Platform Support

- **macOS/Linux**: Full arrow key navigation with curses
- **Windows**: Fallback to text-based input
- **All platforms**: Number/name input always available

## Where Menus Are Used

### 1. Main Launcher (`__main__.py`)

When you run the game:
```bash
python __main__.py
```

You'll see:
```
============================================================
Terminal Multiplayer RPG - Main Menu
============================================================

>> [1] Game Server (host a game)
      Start the server with save file selection menu

   [2] Game Client (join a game)
      Connect to a running game server as a player

   [3] Exit
      Exit the launcher

============================================================
Use ↑/↓ arrows to navigate, ENTER to select, or type number:
```

**Controls:**
- ↑/↓ to highlight
- ENTER to select
- Or type: `1`, `2`, `3`

### 2. Server Launcher (`server_launcher.py`)

When starting a server:
```bash
python server_launcher.py
```

You'll see:
```
============================================================
Terminal Multiplayer RPG - Server Launcher
============================================================

>> [1] world_20251002_143045.tms
      Saved: 2025-10-02T14:30:45 | Players: 2 (Hero, Warrior)

   [2] world_20251002_120000.tms
      Saved: 2025-10-02T12:00:00 | Players: 1 (Mage)

   [3] Start a new world
      Create a fresh world with no existing players

   [4] Quit
      Exit the launcher

============================================================
Use ↑/↓ arrows to navigate, ENTER to select, or type number:
```

**Controls:**
- ↑/↓ to navigate saves
- ENTER to select
- Or type: `1`, `2`, `3`, `4`

### 3. In-Game Help Menu

When you type `help` in-game:
```
============================================================
HELP MENU - Select a Category
============================================================

>> [1] Movement     - How to navigate the world
   [2] Combat       - Fighting enemies and using spells
   [3] Information  - Checking stats and surroundings
   [4] Shopping     - Buying weapons and spells
   [5] Social       - Interacting with other players
   [6] All          - Show all commands

============================================================
Type a number (1-6) or category name to see details
Example: help 2  OR  help combat
============================================================
```

**Note:** In-game menus use text input (not arrow keys) since they work through the server-client architecture.

### 4. Shop Menu

The shop now shows better visual indicators:
```
============================================================
SHOP - Your Gold: 235
============================================================

WEAPONS:
  rusty_sword          - Rusty Sword               Dmg:   5 | Cost:    0 gold  [EQUIPPED]
  iron_sword           - Iron Sword                Dmg:  12 | Cost:   50 gold  
  steel_sword          - Steel Sword               Dmg:  20 | Cost:  150 gold  
  enchanted_blade      - Enchanted Blade           Dmg:  30 | Cost:  300 gold  [TOO EXPENSIVE]
  legendary_sword      - Legendary Dragon Slayer   Dmg:  45 | Cost:  600 gold  [TOO EXPENSIVE]

SPELLS:
  fireball             - Fireball                  15 dmg     | Cost:  100 gold  
  ice_shard            - Ice Shard                 20 dmg     | Cost:  150 gold  
  lightning            - Lightning Bolt            25 dmg     | Cost:  200 gold  [TOO EXPENSIVE]
  heal                 - Heal                      +20 heal   | Cost:  150 gold  
  meteor               - Meteor Strike             40 dmg     | Cost:  400 gold  [TOO EXPENSIVE]

============================================================
Usage: buy <item_id>
Example: buy iron_sword  OR  buy fireball
============================================================
```

## Technical Details

### Menu Utilities Module

Location: `menu_utils.py`

Functions:
- `interactive_menu()` - Main menu function with arrow key support
- `clear_screen()` - Clear terminal screen
- `confirm_prompt()` - Yes/no confirmation
- `display_info()` - Display formatted information boxes
- `wait_for_key()` - Wait for Enter key

### How It Works

1. **Arrow Key Detection**: Uses Python's built-in `curses` library
2. **Curses Menu**: Interactive TUI with real-time key detection
3. **Fallback**: If curses fails (Windows/errors), falls back to text input
4. **Hybrid Input**: Always accepts both arrow keys AND typed input

### Example Usage

```python
from menu_utils import interactive_menu

options = ["Option 1", "Option 2", "Option 3"]
descriptions = ["First option", "Second option", "Third option"]

selected = interactive_menu(
    "My Menu Title",
    options,
    descriptions,
    show_indices=True
)

if selected == 0:
    print("Selected Option 1")
elif selected == 1:
    print("Selected Option 2")
elif selected == 2:
    print("Selected Option 3")
elif selected == -1:
    print("User quit")
```

## Benefits

✅ **More Approachable** - Visual navigation is easier for new users  
✅ **Faster Navigation** - Arrow keys are quicker than typing  
✅ **Better UX** - Clear visual feedback with `>>` indicator  
✅ **Backward Compatible** - Text input still works  
✅ **Cross-Platform** - Graceful fallback on Windows  
✅ **No Dependencies** - Uses Python standard library only  

## Tips

- **macOS/Linux users**: Use arrow keys for best experience
- **Windows users**: Type numbers or option names
- **Everyone**: Both methods work on all platforms!
- Press `Ctrl+C` to cancel/quit at any time

Enjoy the improved menu experience! 🎮

