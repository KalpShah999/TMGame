# Interactive Client Guide

## Why Two Clients?

### The Problem with Server-Side Menus

The original help menu couldn't use arrow keys because of the client-server architecture:

```
Player types "help"
    ↓
Client sends text to server
    ↓
Server processes and sends back text
    ↓
Client displays text
```

**Arrow keys can't work here** because the server just sends text - it can't create an interactive curses menu over the network socket.

### The Solution: Client-Side Menus

The **Interactive Client** solves this by handling menus locally:

```
Player presses 'm' for menu
    ↓
Client shows interactive menu (with arrow keys!)
    ↓
Player selects action with arrows
    ↓
Client sends command to server
    ↓
Server processes and responds
```

## Two Client Options

### 1. Interactive Client (RECOMMENDED) 
**File:** `game_client_interactive.py`

**Features:**
- 🎯 **Main Action Menu** - Press `m` or type `menu` anytime
- ⬆️ **Arrow Key Navigation** - For all game actions
- 📋 **Organized Categories** - Movement, Combat, Magic, Info, Shop, Social
- 🎮 **User-Friendly** - Perfect for new players
- ⌨️ **Still Accepts Text** - Type commands if you prefer

**Start it:**
```bash
python game_client_interactive.py
```

### 2. Classic Client
**File:** `game_client.py`

**Features:**
- ⌨️ **Text Commands Only** - Traditional RPG experience
- 🚀 **Lightweight** - Minimal interface
- 🎯 **Direct** - For experienced players who know commands

**Start it:**
```bash
python game_client.py
```

## Interactive Client Features

### Main Action Menu

Press `m`, `menu`, or `actions` anytime to open:

```
============================================================
ACTION MENU - What would you like to do?
============================================================

>> [1] Movement          - Move to a different location
   [2] Combat            - Attack enemies
   [3] Magic             - Cast spells
   [4] Character Info    - View status, inventory, and other players
   [5] Shop              - Buy weapons and spells
   [6] Social            - Chat with other players
   [7] Help              - View help and commands
   [8] Back to Game      - Return to typing commands

============================================================
Use ↑/↓ arrows to navigate, ENTER to select, or type number:
```

### Available Submenus

#### 1. Movement Menu
- North, South, East, West
- Look Around (examine location)
- Uses arrow keys to select direction

#### 2. Combat Menu
- Prompts for enemy name
- Sends attack command

#### 3. Magic Menu
- View Inventory (see your spells)
- Cast Spell (prompts for spell name)

#### 4. Character Info Menu
- Status (view stats)
- Inventory (equipment and spells)
- Online Players (who's online)
- Look Around (current location)

#### 5. Shop
- Opens shop display
- Type commands to buy items

#### 6. Social Menu
- Prompts for message
- Broadcasts to all players

#### 7. Help Menu
- Select help category with arrows
- Movement, Combat, Information, Shopping, Social, All

### How to Use

**Option 1: Use the Main Menu**
1. Press `m` or type `menu`
2. Navigate with arrow keys
3. Press ENTER to select
4. Follow submenu prompts

**Option 2: Type Commands Directly**
- `status` - See your stats
- `look` - Look around
- `north` - Move north
- `attack goblin` - Attack a goblin
- `help` - Open help menu
- etc.

**Option 3: Mix Both!**
- Use menu for common actions
- Type directly for quick commands
- Whatever feels natural!

## Starting the Interactive Client

### Method 1: Via Main Launcher

```bash
python __main__.py
```

Then select:
```
[2] Game Client - Interactive (RECOMMENDED)
```

### Method 2: Directly

```bash
python game_client_interactive.py
```

Enter server details when prompted.

## Example Gameplay Session

```
> m                     # Open menu

[Select "Movement" with arrows]
[Select "North"]

> status               # Type command directly

> menu                 # Open menu again

[Select "Combat"]
Enemy name: goblin

> m                    # Menu again

[Select "Character Info"]
[Select "Inventory"]

> shop                # Direct command

> buy iron_sword      # Direct command
```

## Comparison

| Feature | Interactive Client | Classic Client |
|---------|-------------------|----------------|
| Arrow Key Menus | ✅ Yes | ❌ No |
| Main Action Menu | ✅ Yes | ❌ No |
| Text Commands | ✅ Yes | ✅ Yes |
| Help Menu (arrows) | ✅ Yes | ❌ No |
| Best For | New players | Experienced players |
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Speed (experts) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## Tips

1. **New to the game?** Use Interactive Client and press `m` often
2. **Know the commands?** Type directly - menu is optional
3. **Forgot a command?** Press `m` and browse categories
4. **Quick actions?** Type commands for speed
5. **Exploring menus?** Use arrow keys for visual feedback

## Technical Details

### How It Works

The Interactive Client:
1. Connects to server like normal client
2. Intercepts certain commands (help, menu, etc.)
3. Shows local interactive menus
4. Converts selections to server commands
5. Sends commands to server
6. Displays server responses

### Architecture

```
Player Input
    ↓
Is it 'menu' or 'help'?
    ↓
Yes → Show local interactive menu
    ↓
Convert selection to command
    ↓
Send to server
    
No → Send directly to server
```

### Benefits

✅ **Best of Both Worlds** - Menus AND text commands  
✅ **No Server Changes** - Works with existing server  
✅ **Backward Compatible** - Classic client still works  
✅ **Flexible** - Use what feels right  
✅ **Discoverable** - New players can explore menus  

## Troubleshooting

**Menus don't show arrow navigation:**
- You're on Windows - use text input instead
- Type numbers or option names
- Works the same, just no visual arrows

**Menu doesn't open:**
- Make sure you type `m` or `menu`
- Case doesn't matter
- Must be connected to server first

**Commands not working:**
- After menu selection, commands are sent normally
- If server is down, client will show disconnect error
- Try classic client to verify server connection

## Future Enhancements

Potential features:
- Dynamic menus based on current location
- Show available exits in movement menu
- List enemies in combat menu
- Show spell list in magic menu
- Price display in shop menu
- Color support for better visuals

---

Enjoy the enhanced gameplay experience! 🎮

