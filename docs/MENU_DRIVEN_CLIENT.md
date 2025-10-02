# Menu-Driven Client Guide

## Overview

The **Menu-Driven Client** (`game_client_menu.py`) provides a **persistent, context-aware menu** that stays active throughout gameplay and updates based on your location and situation.

## How It Works

### Persistent Menu

Unlike traditional clients where you type commands, this client shows you a **menu of available actions** that you navigate with arrow keys:

```
============================================================
GAME ACTIONS - What would you like to do?
============================================================

>> [1] Move North        - Travel north
   [2] Move South        - Travel south
   [3] Move East         - Travel east
   [4] Move West         - Travel west
   [5] Look Around       - Examine your current location
   [6] Attack Enemy      - Fight an enemy in this location
   [7] View Status       - Check your health, level, and stats
   [8] View Inventory    - See your equipment and spells
   ...

============================================================
Use ↑/↓ arrows to navigate, ENTER to select, or type number:
```

### Context-Aware Updates

The menu **changes based on your situation**:

#### In Town Square (Safe Zone)
```
>> Move North
   Move South
   Move East
   Move West
   Look Around
   View Status
   View Inventory
   Shop
   See Players
   Send Message
   Help
   Quit Game
```
**Note:** No "Attack Enemy" option - there are no enemies here!

#### In Dark Forest (with Enemies)
```
>> Move South          ← Only available exits
   Move East
   Look Around
   Attack Enemy        ← Combat option appears!
   Cast Spell          ← Magic option appears!
   View Status
   View Inventory
   Shop
   ...
```
**Note:** Menu shows only valid exits AND adds combat options!

## Key Features

### 1. Dynamic Movement Options
- Menu shows **only available exits** for current location
- Parsed from server's location description
- No more trying invalid directions!

### 2. Context-Based Combat
- "Attack Enemy" appears **only when enemies are present**
- "Cast Spell" appears **only in combat situations**
- No combat options in safe zones

### 3. Always-Available Actions
These options are **always present**:
- Look Around
- View Status
- View Inventory
- Shop
- See Players
- Send Message
- Help
- Quit Game

### 4. Persistent Interface
- Menu **stays active** - no toggling
- Select action → Server processes → Menu updates
- Continuous gameplay flow

## Gameplay Example

**Starting in Town Square:**
```
[1] Move North
[2] Move South
[3] Move East
[4] Move West
[5] Look Around
...
```

**You select: [1] Move North**
```
You travel north...

LOCATION: Dark Forest
A dense, dark forest. Strange sounds echo through the trees.

Exits: south, east
[!] Enemies: Goblin, Wolf
```

**Menu automatically updates:**
```
>> [1] Move South         ← Only valid exits
   [2] Move East
   [3] Look Around
   [4] Attack Enemy       ← Combat appears!
   [5] Cast Spell
   [6] View Status
   ...
```

**You select: [4] Attack Enemy**
```
Enter enemy name: goblin

[COMBAT] Battle started with Goblin!
You strike for 8 damage!
...
```

**Menu refreshes after combat:**
```
>> [1] Move South
   [2] Move East
   [3] Look Around
   [4] View Status       ← Combat cleared if no more enemies
   ...
```

## How Server Communication Works

### The Architecture

```
Player                Client                  Server
  |                     |                       |
  | Select "Move North" |                       |
  |-------------------->|                       |
  |                     | Send "north"          |
  |                     |---------------------->|
  |                     |                       |
  |                     |                       | Process move
  |                     |                       | Generate response
  |                     |                       |
  |                     | Text: "Dark Forest... |
  |                     |        Exits: s, e    |
  |                     |        Enemies: Goblin"|
  |                     |<----------------------|
  |                     |                       |
  |                     | Parse response        |
  |                     | Extract: exits, enemies|
  |                     | Build new menu       |
  |                     |                       |
  | Show updated menu   |                       |
  |<--------------------|                       |
```

### Key Points

1. **Server sends text** (not JSON) - works with existing server!
2. **Client parses text** to extract game state
3. **Menu rebuilds** based on parsed information
4. **Selection converted** to text command
5. **Cycle repeats**

## Starting the Menu Client

### Method 1: Via Launcher

```bash
python __main__.py
```

Select: **[2] Game Client - Menu Driven (RECOMMENDED)**

### Method 2: Direct

```bash
python game_client_menu.py
```

## Comparison of Clients

| Feature | Menu Driven | Interactive | Classic |
|---------|-------------|-------------|---------|
| Persistent Menu | ✅ Yes | ❌ No (toggles) | ❌ No menu |
| Context-Aware | ✅ Yes | ❌ No | ❌ No |
| Arrow Navigation | ✅ Yes | ✅ Yes | ❌ No |
| Shows Valid Exits Only | ✅ Yes | ❌ No | ❌ No |
| Combat When Enemies | ✅ Yes | ❌ No | ❌ No |
| Best For | **New players** | Explorers | Veterans |

## What Gets Parsed

The client parses server messages to extract:

### 1. Available Exits
```
From: "Exits: north, south, east"
To:   Menu shows only these directions
```

### 2. Enemy Presence
```
From: "[!] Enemies: Goblin, Wolf"
To:   Menu adds combat options
```

### 3. Location Name
```
From: "LOCATION: Dark Forest"
To:   Client knows current location
```

## Tips

1. **Let the menu guide you** - Available options = possible actions
2. **Combat appears dynamically** - Only when needed
3. **Invalid moves prevented** - Menu only shows valid exits
4. **Shop always available** - Can browse items anywhere
5. **Help when needed** - Help option always present

## Technical Details

### State Management

The client maintains a simple state:
```python
{
    'last_update': "full server response text",
    'available_exits': ['north', 'south'],
    'has_enemies': True
}
```

### Menu Building Logic

```python
1. Parse last server response
2. Extract exits → Add movement options
3. Check for enemies → Add combat options
4. Add always-available options
5. Display menu with arrow keys
6. Convert selection to command
7. Send to server
8. Repeat
```

### Why This Works

- **No server changes needed** - Parses existing text responses
- **Context awareness** - Reads server messages for state
- **Dynamic adaptation** - Menu changes as you play
- **Simple protocol** - Text in, text out

## Future Enhancements

Potential improvements:
- Parse player health to show "Rest" when low
- Detect shop locations to highlight shop option
- Show enemy list in combat menu
- Display available spells in cast menu
- Color-code dangerous vs safe areas

## Troubleshooting

**Menu doesn't update exits:**
- Make sure you "Look Around" after moving
- Server sends exit info with location descriptions
- Menu will show all directions until you look

**Combat options don't appear:**
- Use "Look Around" to check for enemies
- Server must send enemy info for client to detect
- Menu updates when "Enemies:" appears in text

**Menu feels slow:**
- Small delay after actions is normal
- Allows server response to arrive
- Can be adjusted in code if needed

---

Enjoy the streamlined, menu-driven gameplay! 🎮

