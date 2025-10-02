# Help Menu Examples

## Initial Help Menu

When you type `help`:

```
============================================================
📖 HELP MENU - Select a Category
============================================================

  [1] Movement     - How to navigate the world
  [2] Combat       - Fighting enemies and using spells
  [3] Information  - Checking stats and surroundings
  [4] Shopping     - Buying weapons and spells
  [5] Social       - Interacting with other players
  [6] All          - Show all commands

============================================================
Usage: help <number> or help <category>
Example: help 2  OR  help combat
============================================================
```

## Category Examples

### Help 1 - Movement

```
============================================================
🚶 MOVEMENT COMMANDS
============================================================
  north / n    - Move north
  south / s    - Move south
  east / e     - Move east
  west / w     - Move west
============================================================

Type 'help' to return to the help menu.
```

### Help 2 - Combat

```
============================================================
⚔️  COMBAT COMMANDS
============================================================
  attack <enemy>  - Attack an enemy in your location
                    Example: attack goblin
  cast <spell>    - Cast a spell (requires mana)
                    Example: cast fireball
============================================================

Type 'help' to return to the help menu.
```

### Help 3 - Information

```
============================================================
ℹ️  INFORMATION COMMANDS
============================================================
  status       - View your character stats
  look         - Look around your current location
  inventory    - View your inventory and equipment
  inv          - Shortcut for inventory
  players      - See all online players and locations
============================================================

Type 'help' to return to the help menu.
```

### Help 4 - Shopping

```
============================================================
🏪 SHOPPING COMMANDS
============================================================
  shop            - View available weapons and spells
  buy <item_id>   - Purchase an item from the shop
                    Example: buy iron_sword
                    Example: buy fireball
============================================================

Type 'help' to return to the help menu.
```

### Help 5 - Social

```
============================================================
💬 SOCIAL COMMANDS
============================================================
  say <message>   - Send a message to all players
                    Example: say Hello everyone!
============================================================

Type 'help' to return to the help menu.
```

## Usage Options

You can access categories in multiple ways:

- `help 1` - By number
- `help 2` - By number
- `help movement` - By full name
- `help combat` - By full name
- `help info` - By shorthand (for information)
- `help shop` - By shorthand (for shopping)
- `help social` - By full name
- `help 6` or `help all` - Show everything at once

## Invalid Category

If you type an invalid category:

```
> help xyz
Invalid category. Type 'help' to see available categories.
```

