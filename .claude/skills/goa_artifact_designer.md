# GoA Artifact Designer Skill

You are an artifact/equipment designer for Warcraft: Guardians of Azeroth (CK2 mod).

## Artifact Definition Template

```
hoa_<tier>_<class>_<slot> = {
    quality = <1-5>
    flags = { <slot_type> <category_flags> }
    active = {
        <activation_conditions>
    }
    stacking = <yes/no>
    <stat_bonuses>
    picture = "<GFX_name>"
    slot = <slot_name>
}
```

## Slots Available
| Slot | Key | Stacking | Notes |
|------|-----|----------|-------|
| Weapon | weapon | no | Swords, axes, staffs, bows |
| Crown | crown | no | Helms, circlets, hoods |
| Wrist | wrist | no | Bracers, gauntlets, gloves |
| Neck | neck | no | Amulets, necklaces |
| Torso | torso | no | Chest armor, robes |
| Ring | ring | yes (x2) | Can equip 2 rings |
| Relic | relic | no | Class-specific relics |

## WoW Tier Set Design Rules

### Naming Convention
- T1 sets: Use classic WoW T1 names (Might, Arcanist, Lawbringer, Nightslayer, etc.)
- T2 sets: Use classic WoW T2 names (Wrath, Netherwind, Judgement, Bloodfang, etc.)
- T3 sets: Use Naxxramas names (Dreadnaught, Frostfire, Redemption, Bonescythe, etc.)

### Class-to-Armor Mapping
| Class | Armor Type | Primary Stat | Secondary Stat |
|-------|-----------|-------------|----------------|
| Warrior | Plate | martial | combat_rating, health |
| Paladin | Plate | martial + learning | piety, combat_rating |
| Death Knight | Plate | martial | combat_rating, health |
| Mage | Cloth | learning | combat_rating, tech |
| Warlock | Cloth | learning + intrigue | combat_rating |
| Priest | Cloth | learning | piety, health |
| Rogue | Leather | intrigue | combat_rating, murder |
| Monk | Leather | martial + learning | health |
| Druid | Leather | learning + diplomacy | health, piety |
| Hunter | Mail | martial + intrigue | supply, archers cmd |
| Shaman | Mail | learning + martial | piety, combat_rating |

### Stat Budget by Quality
| Quality | Total Stat Points | Max Single Stat | Max CR |
|---------|------------------|----------------|--------|
| Q2 (Uncommon) | 3-5 | +2 | 8 |
| Q3 (Rare/T1) | 5-8 | +3 | 12 |
| Q4 (Epic/T2) | 8-12 | +4 | 16 |
| Q5 (Legendary) | 12-18 | +5 | 25 |

### Activation Conditions

**Tier Sets** (class-gated):
```
active = {
    is_adult = yes
    OR = {
        has_character_flag = hoa_<tier>_<class>_earned
        trait = class_<name>_<min_level>  # Level 5+ for T1, earned-only for T2+
        # ... list all levels from min to 10
    }
}
```

**Crafted Items** (universal):
```
active = {
    # Physical weapons
    shared_physical_weapon_trigger = yes
    # OR magical weapons
    shared_magical_weapon_trigger = yes
    # OR just
    is_adult = yes
}
```

### Command Modifiers (for military items)
```
command_modifier = {
    # Unit type bonuses
    heavy_infantry = 0.03    # Warrior/Paladin plate
    light_infantry = 0.03    # Rogue leather
    archers = 0.03           # Hunter mail
    cavalry = 0.03           # Death Knight plate
    # Combat modifiers
    morale_offence = 0.03    # Aggressive sets
    morale_defence = 0.03    # Defensive sets
    defence = 0.02           # Tank armor
}
```

### WoW Raid-to-Tier Mapping
| Raid | Tier | Quality | Min Class Level |
|------|------|---------|----------------|
| Molten Core | T1 | 3 (Rare) | 5 |
| Blackwing Lair | T2 | 4 (Epic) | earned only |
| Ahn'Qiraj | T2.5 | 4 (Epic) | earned only |
| Naxxramas | T3 | 4-5 (Epic-Legendary) | earned only |
| Karazhan | T4 | 4 (Epic) | earned only |
| Serpentshrine/TK | T5 | 4-5 | earned only |
| Black Temple/Hyjal | T6 | 5 (Legendary) | earned only |
| Icecrown Citadel | T10 | 5 (Legendary) | earned only |
