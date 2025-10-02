# Save System Guide

## Quick Start

### Starting the Server with Save Menu

```bash
python server_launcher.py
```

You'll see a menu like this:

```
======================================================================
🎮 Terminal Multiplayer RPG - Server Launcher
======================================================================

Available save files:

  [1] world_20251002_143045.tms
      Saved: 2025-10-02T14:30:45
      Players: 3 (Hero, Warrior, Mage)

  [2] autosave_20251002_120000.tms
      Saved: 2025-10-02T12:00:00
      Players: 1 (Hero)

  [N] Start a new world
  [Q] Quit

======================================================================

Select a save file (number, N for new, Q to quit):
```

### How It Works

1. **New World**: Select `N` to create a fresh world
   - A new `.tms` file will be created automatically
   - File format: `world_YYYYMMDD_HHMMSS.tms`

2. **Load Existing**: Select a number to load that save file
   - All player data will be restored
   - Players can reconnect with their existing characters

3. **Auto-Save**: While running, the server auto-saves every 5 minutes
   - Progress is saved automatically
   - No player action required

4. **Graceful Shutdown**: Press `Ctrl+C` to stop the server
   - Game state is saved before shutdown
   - All player progress preserved

## Save File Format

Save files are JSON (`.tms` = Terminal Multiplayer Save):

```json
{
  "saved_at": "2025-10-02T14:30:45.123456",
  "players": {
    "Hero": {
      "health": 120,
      "max_health": 140,
      "mana": 65,
      "max_mana": 70,
      "level": 5,
      "exp": 45,
      "exp_to_level": 112,
      "gold": 235,
      "location": "dark_forest",
      "weapon": "iron_sword",
      "spells": ["fireball", "heal"],
      "inventory": []
    },
    "Warrior": {
      ...
    }
  },
  "server_info": {
    "host": "0.0.0.0",
    "port": 5555
  }
}
```

## Managing Save Files

### Location
All save files are in: `saves/` directory

### Backup
```bash
# Backup all saves
cp -r saves/ saves_backup/

# Backup specific save
cp saves/world_20251002_143045.tms ~/backups/
```

### Manual Editing
You can edit save files manually:

```bash
# Open in text editor
nano saves/world_20251002_143045.tms

# Make changes (e.g., give yourself more gold, level up)
# Save and exit

# Load the modified save
python server_launcher.py
```

### Sharing Worlds
Share your world with friends:

```bash
# Send them the .tms file
# They place it in their saves/ directory
# They can then load it using server_launcher.py
```

## Tips & Tricks

### Cheat Mode (Manual Editing)
Edit save files to:
- Give players more gold
- Change player levels
- Modify health/mana
- Change starting location
- Add spells to inventory

Example - Make yourself rich and powerful:
```json
"Hero": {
  "health": 500,
  "max_health": 500,
  "level": 99,
  "gold": 9999,
  "weapon": "legendary_sword",
  "spells": ["fireball", "lightning", "meteor", "heal"]
}
```

### Regular Backups
Set up automatic backups:

```bash
# Add to cron (Linux/Mac)
# Backup saves every day at midnight
0 0 * * * cp -r /path/to/TMGame/saves /path/to/backups/saves_$(date +\%Y\%m\%d)
```

### Multiple Worlds
Create different worlds for different groups:

```
saves/
  ├── beginner_world.tms      (for new players)
  ├── hardcore_world.tms      (for experienced players)
  ├── pvp_arena.tms           (for PvP battles)
  └── testing_world.tms       (for testing new features)
```

Select which world to load when starting the server!

## Troubleshooting

### "Save file not found"
- Check that the file is in the `saves/` directory
- Ensure the file has `.tms` extension
- Check file permissions (should be readable)

### "Failed to load game"
- Save file might be corrupted
- Check JSON syntax is valid
- Restore from backup if needed

### "Failed to save game"
- Check disk space
- Ensure `saves/` directory exists
- Check write permissions

### Invalid JSON
If you manually edited and broke the JSON:

```bash
# Validate JSON
python -m json.tool saves/world_20251002_143045.tms

# If invalid, restore from backup or fix syntax
```

## Advanced Usage

### Programmatic Save Management

```python
from game_server import GameServer

# Create server with specific save file
server = GameServer(save_file="my_custom_world.tms")

# Save at any time
server.save_game()

# Save to different file
server.save_game("backup_save.tms")
```

### Migration Script
If you want to migrate old player data:

```python
import json

# Load old save
with open('saves/old_world.tms', 'r') as f:
    old_data = json.load(f)

# Migrate/modify data
new_data = old_data.copy()
# ... modify as needed ...

# Save new version
with open('saves/new_world.tms', 'w') as f:
    json.dump(new_data, f, indent=2)
```

## Best Practices

1. **Regular Backups**: Auto-save is great, but keep backups!
2. **Descriptive Names**: Rename important saves (e.g., `beginner_world.tms`)
3. **Test Edits**: Test manual edits on a copy first
4. **Version Control**: Consider using git for important worlds
5. **Document Changes**: Keep notes about what each world contains

Happy gaming! 🎮✨

