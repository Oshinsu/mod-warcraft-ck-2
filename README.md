# GoA: Improved Economy & Buildings

A submod for **Warcraft: Guardians of Azeroth** (CK2) that overhauls the economic system with Warcraft-themed buildings, cultural economic specializations, and economic events.

## Features

### New Universal Buildings (Castle)
- **Mines** (5 tiers) - Terrain-gated (mountain/hills/desert), themed copper > iron > mithril > thorium > saronite
- **Arcane Workshop** (4 tiers) - Magic-based income + tech growth
- **War Forge** (4 tiers) - Military-economic crossover, requires barracks
- **Merchant Quarter** (4 tiers) - Trade income for farmlands/plains
- **Lumber Mill** (4 tiers) - Forest/jungle terrain economy

### Cultural Economic Buildings (Castle)
Each major race gets unique economic buildings:
- **Goblin**: Engineering Works + Trade Emporium (highest income, tech bonuses)
- **Dwarf**: Deep Mine + Master Forge (mining + military economy)
- **Human**: Merchant Guild + Royal Academy (balanced income + tech)
- **Orc**: War Trophy Market + Peon Labor Camp (prestige + income)
- **Night Elf**: Moonwell Garden (piety + culture tech)
- **Troll**: Voodoo Market (piety + culture tech)
- **Tauren**: Plains Ranch (supply + income)
- **Draenei**: Crystal Workshop (piety + all tech)
- **Gnome**: Inventor's Workshop (all three techpoints)
- **High Elf/Blood Elf**: Sunstrider Bazaar (prestige + culture tech)
- **Undead**: Royal Apothecary Society (military tech + disease defense)

### Tribal Economic Buildings
- **Tribal Market** (4 tiers) - Basic income for tribal holdings
- **Gathering Ground** (3 tiers) - Prestige + income
- **Hunting Grounds** (3 tiers) - Supply + income

### Unique Capital Buildings
- **Stormwind**: Trade District (castle) + Old Town Markets (city)
- **Orgrimmar**: Great War Forge
- **Ironforge**: Hall of Explorers
- **Thunder Bluff**: Elder Rise Markets
- **Gnomeregan**: Innovation Hub
- **Boralus**: Grand Admiral's Harbor
- **Dalaran**: Violet Citadel Commerce
- **Darnassus**: Temple of the Moon Treasury
- **Silvermoon**: Sunstrider Spire Commerce

### Economic Events
- Gold Vein Discovery (mountain provinces)
- Trade Caravan Arrival (farmland/plains)
- Arcane Market Boom (magic cultures)
- Goblin Investor (risk/reward investment)
- Harvest Festival (vassal opinion + economy)

### Economic Decisions
- Establish Trade Agreements (diplomacy + economy)
- Commission Grand Construction (capital boost)
- Develop Mining Operations (mountain provinces)
- Hire Goblin Financial Advisor (tax optimization)

## Installation

1. Install Warcraft: Guardians of Azeroth (v1.10.0+)
2. Copy the `GoA_Improved_Economy` folder to your CK2 mod directory
3. Enable the submod in the CK2 launcher (it should appear below GoA)

## Compatibility

- Requires: Warcraft: Guardians of Azeroth v1.10.0+
- Compatible with: CK2 3.3.x
- This submod only ADDS new buildings and events, it does NOT override any existing GoA files

## Design Philosophy

- Buildings have Warcraft-appropriate costs and build times
- Cultural buildings provide economic identity to each race
- Terrain-gated buildings encourage strategic province selection
- Events add narrative flavor while providing economic choices
- All values balanced against vanilla GoA ca_town (2 gold/tier, 1620 gold total for 12/month)

## File Structure

```
GoA_Improved_Economy/
  GoA_Improved_Economy.mod          # Mod descriptor
  common/
    buildings/
      ie_castle_economy.txt         # Universal castle economic buildings
      ie_culture_economy.txt        # Culture-specific economic buildings
      ie_unique_capitals.txt        # Unique capital city buildings
      ie_tribal_economy.txt         # Tribal economic buildings
    event_modifiers/
      ie_event_modifiers.txt        # Province event modifiers
      ie_character_modifiers.txt    # Character modifiers for decisions
  decisions/
    ie_economy_decisions.txt        # Economic decisions
  events/
    ie_economy_events.txt           # Economic events
  localisation/
    ie_buildings.csv                # Building name/description localization
    ie_events.csv                   # Event text localization (EN/FR/DE/ES)
```

## Report

See [RAPPORT_ECONOMIE_GOA.md](RAPPORT_ECONOMIE_GOA.md) for the full analysis of the original GoA economy system.
