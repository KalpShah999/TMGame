"""
Game Data Module
Contains all game world data including locations, items, enemies, and spells.
"""

# Game Locations
LOCATIONS = {
    "town_square": {
        "name": "Town Square",
        "description": "A bustling town square with merchants and travelers. You see paths leading in multiple directions.",
        "exits": {"north": "dark_forest", "east": "mountain_path", "south": "riverside", "west": "ancient_ruins"},
        "enemies": []
    },
    "dark_forest": {
        "name": "Dark Forest",
        "description": "A dense, dark forest. Strange sounds echo through the trees.",
        "exits": {"south": "town_square", "east": "haunted_grove"},
        "enemies": ["goblin", "wolf"]
    },
    "haunted_grove": {
        "name": "Haunted Grove",
        "description": "An eerie grove where the air feels cold. Spirits seem to linger here.",
        "exits": {"west": "dark_forest"},
        "enemies": ["ghost", "wraith"]
    },
    "mountain_path": {
        "name": "Mountain Path",
        "description": "A steep mountain path with breathtaking views. The air is thin here.",
        "exits": {"west": "town_square", "north": "dragon_peak"},
        "enemies": ["troll"]
    },
    "dragon_peak": {
        "name": "Dragon's Peak",
        "description": "The highest peak of the mountain. You can see the entire realm from here. A powerful presence looms.",
        "exits": {"south": "mountain_path"},
        "enemies": ["dragon"]
    },
    "riverside": {
        "name": "Peaceful Riverside",
        "description": "A calm river flows gently. This seems like a safe place to rest.",
        "exits": {"north": "town_square", "east": "ancient_ruins"},
        "enemies": []
    },
    "ancient_ruins": {
        "name": "Ancient Ruins",
        "description": "Crumbling stone structures from a forgotten civilization. Treasure might be hidden here.",
        "exits": {"east": "town_square", "west": "riverside"},
        "enemies": ["skeleton", "guardian"]
    }
}

# Enemy types
ENEMIES = {
    "goblin": {
        "name": "Goblin",
        "health": 30,
        "damage": 5,
        "exp_reward": 15,
        "gold_reward": 10
    },
    "wolf": {
        "name": "Wolf",
        "health": 25,
        "damage": 7,
        "exp_reward": 12,
        "gold_reward": 5
    },
    "skeleton": {
        "name": "Skeleton Warrior",
        "health": 40,
        "damage": 8,
        "exp_reward": 20,
        "gold_reward": 15
    },
    "troll": {
        "name": "Mountain Troll",
        "health": 60,
        "damage": 12,
        "exp_reward": 30,
        "gold_reward": 25
    },
    "ghost": {
        "name": "Restless Ghost",
        "health": 35,
        "damage": 10,
        "exp_reward": 25,
        "gold_reward": 20
    },
    "wraith": {
        "name": "Dark Wraith",
        "health": 50,
        "damage": 15,
        "exp_reward": 35,
        "gold_reward": 30
    },
    "guardian": {
        "name": "Stone Guardian",
        "health": 80,
        "damage": 18,
        "exp_reward": 50,
        "gold_reward": 50
    },
    "dragon": {
        "name": "Ancient Dragon",
        "health": 150,
        "damage": 25,
        "exp_reward": 100,
        "gold_reward": 100
    }
}

# Weapons
WEAPONS = {
    "rusty_sword": {
        "name": "Rusty Sword",
        "damage": 5,
        "cost": 0,
        "description": "A worn sword, better than nothing."
    },
    "iron_sword": {
        "name": "Iron Sword",
        "damage": 12,
        "cost": 50,
        "description": "A sturdy iron blade."
    },
    "steel_sword": {
        "name": "Steel Sword",
        "damage": 20,
        "cost": 150,
        "description": "A well-crafted steel weapon."
    },
    "enchanted_blade": {
        "name": "Enchanted Blade",
        "damage": 30,
        "cost": 300,
        "description": "A magical blade that glows with power."
    },
    "legendary_sword": {
        "name": "Legendary Dragon Slayer",
        "damage": 45,
        "cost": 600,
        "description": "A legendary weapon forged to slay dragons."
    }
}

# Spells
SPELLS = {
    "fireball": {
        "name": "Fireball",
        "damage": 15,
        "mana_cost": 10,
        "cost": 100,
        "description": "Launch a ball of fire at your enemy."
    },
    "lightning": {
        "name": "Lightning Bolt",
        "damage": 25,
        "mana_cost": 15,
        "cost": 200,
        "description": "Strike your foe with lightning from the sky."
    },
    "ice_shard": {
        "name": "Ice Shard",
        "damage": 20,
        "mana_cost": 12,
        "cost": 150,
        "description": "Fire sharp shards of ice."
    },
    "heal": {
        "name": "Heal",
        "damage": -20,  # Negative damage = healing
        "mana_cost": 15,
        "cost": 150,
        "description": "Restore your health."
    },
    "meteor": {
        "name": "Meteor Strike",
        "damage": 40,
        "mana_cost": 25,
        "cost": 400,
        "description": "Call down a meteor to devastate your enemy."
    }
}

# Starting player stats
STARTING_STATS = {
    "health": 100,
    "max_health": 100,
    "mana": 50,
    "max_mana": 50,
    "level": 1,
    "exp": 0,
    "exp_to_level": 50,
    "gold": 50,
    "location": "town_square",
    "weapon": "rusty_sword",
    "spells": [],
    "inventory": []
}

