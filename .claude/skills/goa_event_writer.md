# GoA Event Writer Skill

You are an expert CK2 event writer specialized in Warcraft: Guardians of Azeroth modding.

## Event Structure (PDXScript)

```
namespace = hoa_<system>

character_event = {
    id = hoa_<system>.<number>
    desc = hoa_<system>.<number>.desc
    picture = GFX_evt_<type>

    # For random events:
    trigger = { <conditions> }
    mean_time_to_happen = {
        years = <base>
        modifier = { factor = <mult> <condition> }
    }

    # For triggered events:
    is_triggered_only = yes

    # Use immediate block for random outcome calculation
    immediate = {
        random_list = {
            <weight> = {
                modifier = { factor = <mult> <condition> }
                set_character_flag = hoa_<event>_<outcome>
            }
        }
    }

    option = {
        name = hoa_<system>.<number>.<letter>
        trigger = { has_character_flag = hoa_<event>_<outcome> }
        <effects>
        clr_character_flag = hoa_<event>_<outcome>
        ai_chance = { factor = <weight> }
    }
}
```

## Outcome Weighting Rules

For dungeon/raid events, always use 4 outcome tiers:

| Tier | Base % | Positive Modifiers | Negative Modifiers |
|------|--------|-------------------|-------------------|
| Great Success | 15-35% | martial>=15 (+50%), class 7+ (+30%), brave (+20%), good artifacts (+20%) |  |
| Moderate Success | 30-35% | (base, no modifiers) | |
| Failure | 20-30% | | martial>=15 (-50%) |
| Catastrophe | 10-25% | | martial>=15 (-70%), craven (x2) |

## Class-Specific Loot Pattern

```
hidden_tooltip = {
    if = {
        limit = { is_warrior_class_trigger = yes }
        set_character_flag = hoa_<tier>_warrior_earned
        random_list = {
            50 = { add_artifact = hoa_<tier>_warrior_crown }
            50 = { add_artifact = hoa_<tier>_warrior_torso }
        }
    }
    else_if = {
        limit = { is_mage_class_trigger = yes }
        # ... same pattern for each class
    }
    else = {
        # Generic loot for unhandled classes
        add_artifact = hoa_crafted_ring_rare
    }
}
```

## Difficulty Scaling

| Difficulty | Entry Martial | Entry Cost | Success Gold | Boss Title Stats |
|-----------|--------------|-----------|-------------|-----------------|
| Easy (T1) | 10 | 100g + 50 prest | 200g | martial +2, CR +5 |
| Medium (T2) | 14 | 200g + 100 prest | 400g | martial +3, CR +8 |
| Hard (T3) | 16 | 400g + 200 prest | 800g | martial +4, CR +12 |
| Extreme | 18+ | 600g + 300 prest | 1200g | martial +5, CR +15 |

## Event Pictures (available in GoA)
- `GFX_evt_burning_house` - Fire, destruction, raids
- `GFX_evt_battle` - Combat, duels, wars
- `GFX_evt_council` - Diplomacy, meetings, trade
- `GFX_evt_throne_room` - Court events, ceremonies
- `GFX_evt_castle` - Building, fortification
- `GFX_evt_mysterious_stranger` - Unknown encounters

## Cooldown Pattern
Always add a hidden cooldown modifier after the event chain:
```
set_character_flag = hoa_<event>_cooldown
# OR use timed modifier:
add_character_modifier = {
    name = hoa_<event>_cooldown
    duration = <days>
    hidden = yes
}
```

## Localization Format
CSV with semicolons: `CODE;ENGLISH;FRENCH;GERMAN;;SPANISH;;;;;;;;;x`
- Every event desc, option name, tooltip, and modifier name needs a localization entry
- French: full translation with Warcraft lore terms preserved (Ragnaros, Nefarian, etc.)
- German/Spanish: can be abbreviated if needed
