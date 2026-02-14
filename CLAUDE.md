# GoA Modding Project - Claude Code Context

## Project Overview
This repository contains **two submods** for Warcraft: Guardians of Azeroth (CK2 total conversion mod):

1. **GoA_Improved_Economy/** - Economic buildings, cultural buildings, trade, unique capitals
2. **GoA_Heroes_of_Azeroth/** - WoW-style tier sets, crafting, dungeon raids, diplomacy

## CK2 PDXScript Reference

### File Structure
- `common/artifacts/` - Artifact definitions (slots: weapon, crown, wrist, neck, torso, ring, relic, library, leader)
- `common/buildings/` - Building chains per holding type (castle, city, temple, tribal, trade_post)
- `common/event_modifiers/` - Character and province modifiers
- `common/scripted_triggers/` - Reusable trigger blocks
- `common/traits/` - Character traits
- `decisions/` - Player/AI decisions with potential/allow/effect blocks
- `events/` - Namespaced events with options and ai_chance
- `localisation/` - CSV files: CODE;ENGLISH;FRENCH;GERMAN;;SPANISH;;;;;;;;;x

### GoA Class System
11 WoW classes, 10 levels each:
- warrior, mage, paladin, rogue, hunter, shaman, priest, warlock, druid, death_knight, monk
- Trait format: `class_<name>_<level>` (e.g. `class_warrior_5`)
- Magic classes: mage, warlock, priest, druid, shaman

### GoA Race System
30+ races as traits: `creature_human`, `creature_orc`, `creature_nightelf`, `creature_dwarf`, `creature_gnome`, `creature_troll`, `creature_tauren`, `creature_undead`, `creature_bloodelf`, `creature_draenei`, `creature_goblin`, `creature_worgen`, etc.

### Artifact Quality Scale
1=Common, 2=Uncommon (green), 3=Rare (blue), 4=Epic (purple), 5=Legendary (orange)

### Key Scripted Triggers (our mod)
- `has_any_class_trigger` - Character has any of the 11 classes
- `is_<class>_class_trigger` - Character has specific class (any level)
- `is_magic_class_trigger` - Character is mage/warlock/priest/druid/shaman

### Naming Conventions
- Prefix: `hoa_` for Heroes of Azeroth, `ie_` for Improved Economy
- Events: `hoa_dungeon.1`, `hoa_diplo.1`, etc.
- Artifacts: `hoa_t1_warrior_crown`, `hoa_crafted_sword_epic`, etc.
- Modifiers: `hoa_ragnaros_slayer`, `hoa_crafting_cooldown`, etc.

### Event Outcome Pattern
For dungeon/combat events, use 4 tiers:
- Great Success (15-35%): Boss kill + class-specific loot + permanent title
- Moderate Success (30-35%): Some loot + gold
- Failure (20-30%): Wounded + prestige loss
- Catastrophe (10-25%): Severely injured + major losses

Weight modifiers by: martial, class level (7+), traits (brave/craven), equipped artifacts.

### Balance Guidelines
- Gold costs: Easy=100, Medium=200-400, Hard=400-800
- Cooldowns: Minor=180 days, Standard=365-730 days, Major=1825 days
- Combat Rating per item: Uncommon=3-8, Rare=5-12, Epic=10-16, Legendary=15-25
- Stat bonuses per item: max +3 to any single stat, max +5 for legendary
- Prestige rewards: scale with difficulty (50-500 range)
- ROI for raids: 1.5-3x gold investment on success

## Tools
- `tools/goa_agent_generator.py` - Agent SDK mod generator
- `tools/mcp_servers/ck2_parser.py` - MCP server for CK2 save parsing
- `tools/templates/` - Generation templates

## Reports
- `RAPPORT_ECONOMIE_GOA.md` - Economy analysis
- `RAPPORT_DIPLOMATIE_EQUIPEMENT_GOA.md` - Diplomacy/equipment analysis
- `RAPPORT_HEROES_OF_AZEROTH.md` - Heroes of Azeroth submod documentation
