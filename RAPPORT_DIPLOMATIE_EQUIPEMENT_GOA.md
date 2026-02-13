# Rapport Complet : Diplomatie, Stats, Equipement & Donjons - GoA (CK2)

## 1. Systeme de Classes WoW (wc_class_traits.txt - 3,342 lignes)

### Classes implementees (10 niveaux chacune) :
| Classe | Stat principale | Combat Rating (1->10) | Bonus unique |
|--------|----------------|----------------------|--------------|
| Mage | Learning | 5->50 | Conjure Food, Sharp Mind, Study Secrets, Siege Speed |
| Hunter | Martial/Intrigue | 5->50 | Inspire Army, Supply Limit, Levy Reinforce |
| Warrior | Martial | 10->55 | Command Modifier, Land Morale, Levy Size |
| Rogue | Intrigue | 5->50 | Plot Power, Murder Plot, Stealth |
| Priest (Holy) | Learning | 5->45 | Healing, Piety, Disease Defense |
| Warlock | Intrigue/Learning | 5->50 | Dark Magic, Summoning, Fel Power |
| Paladin | Martial/Learning | 5->50 | Holy Strike, Healing, Light Power |
| Druid | Learning | 5->45 | Shapeshifting (druid_forms.txt), Nature Magic |
| Shaman | Learning/Martial | 5->50 | Elemental Powers, Spirit Walk |
| Death Knight | Martial | 10->55 | Raise Dead, Frost Power, Disease |
| Monk | Martial/Intrigue | 5->50 | Chi, Healing, Combat |

**Sous-classes** : dark_shaman, moon_priest

### Progression :
- Niveau 1-3 : Faible (0-1 attribute points)
- Niveau 4-6 : Moyen (2 attribute points)
- Niveau 7-9 : Fort (3-4 attribute points)
- Niveau 10 : Legendaire (4+ attribute points, toutes abilities debloquees)

### Constats :
- Le systeme est bien fait mais les classes n'interagissent PAS entre elles
- Pas de "group finder", pas de synergie de groupe
- Pas de specialisations (pas de Fire/Frost/Arcane mage, pas de Arms/Fury/Prot warrior)
- Les abilities sont surtout passives (text_effect flags)

---

## 2. Traits Raciaux (wc_race_traits.txt - 2,154 lignes)

### Races implementees :
| Race | Stats | Duree de vie | Special |
|------|-------|-------------|---------|
| Human (creature_human) | +2 Diplo | 70 ans | Ambition |
| Orc (creature_orc) | +2 Martial, +10 Combat | 70 ans | Honor |
| Troll (creature_troll) | -1 Diplo, +1 Martial | 70 ans | Regeneration |
| Dwarf (creature_dwarf) | +1 Stewardship | 250 ans (immortal) | - |
| Gnome (creature_gnome) | +1 Diplo, +2 Stew, +2 Learn | 300 ans (immortal) | -10 Combat |
| High Elf (creature_high_elf) | +2 Learning | 1000 ans (immortal) | - |
| Blood Elf (creature_blood_elf) | +1 Martial, +1 Learning | 1000 ans (immortal) | - |
| Night Elf | +2 Learning | Immortel | Nature |
| Naga | +10 Combat | 1500 ans (immortal) | - |
| Draenei | +1 Learning, +2 Diplo | ~25,000 ans (immortal) | - |
| Tauren | +2 Martial | 100 ans | - |
| Murloc | -2 Diplo, -1 Martial, +1.0 Fertility | 70 ans | -20 Combat |
| Gnoll | -4 Diplo, +10 Combat | 70 ans | Aggressive |
| Kobold | -2 Martial, -2 Learning | 70 ans | - |
| Ogre | -2 Diplo, +0.7 Health, +20 Combat | 70 ans | - |
| Dragons (rouge, bleu, vert, bronze, noir) | Varies par age | Immortel | whelp->drake->dragon->wyrm |
| Demons | Varies | Immortel | - |
| Elementals | Varies | Immortel | - |
| Undead | Varies | Immortel | - |

### Constats :
- Plus de 30 races avec traits detailles
- Les dragons ont 4 stades d'evolution (whelp, drake, dragon, wyrm) avec combat_rating allant de 0 a 100+
- Les races "monstres" (murloc, gnoll, kobold) ont des malus significatifs
- **Manque** : pas de trait "reputation raciale" dynamique entre races

---

## 3. Systeme d'Artefacts (10,877 lignes, 26 fichiers)

### Slots d'equipement :
| Slot | Nombre | Equivalent WoW |
|------|--------|---------------|
| weapon | 1 | Main Hand + Off Hand (combine) |
| crown | 1 | Head |
| wrist | 1 | Hands/Wrists |
| neck | 1 | Neck |
| torso | 1 | Chest (armor) |
| ceremonial_torso | 1 | Back (cape/cloak) |
| ring | 2 | Ring x2 |
| relic | 1 | Trinket |
| library | 4 | - (livres/parchemins) |
| leader | 1 | Banner/Horn/Drum |
| **TOTAL** | **14** | |

### Qualite d'artefacts :
| Qualite | Nom WoW | Exemples GoA |
|---------|---------|-------------|
| 1 | Common (blanc) | Cloak of Trollbanes, Tabard of the Silver Hand |
| 2 | Uncommon (vert) | Belt of Lothar, Band of the Ranger General, Gauntlets of Trollbanes |
| 3 | Rare (bleu) | Justice Gaze, Ring of Trollbanes, Naga Scimitar, Dark Crystal |
| 4 | Epic (violet) | Ironfoe, Chalice of Trollbanes |
| 5 | Legendary (orange) | Felo'melorn, Ashbringer, Doomhammer, Scythe of Elune, Trol'kalar, Aluneth, Skull of Gul'dan, Horn of Cenarius, Heart of Y'Shaarj, The Silver Hand |

### Artefacts legendaires identifies :
- **Armes 1H** : Felo'melorn, Ironfoe, Hammer of the Twilight, Serathil, Naga weapons
- **Armes 2H** : Ashbringer, Doomhammer, Scythe of Elune, Trol'kalar, Aluneth, The Silver Hand
- **Runeblades** : (fichier dedie pour les epees runiques DK)
- **Couronnes/Casques** : Justice Gaze, + generiques
- **Capes/Robes** : Mantle of Gorak Tul, Robe of the Warlock
- **Anneaux** : Ring of Trollbanes, Ring of the Kaldorei Empire, Band of the Ranger General
- **Reliques** : Skull of Gul'dan, Horn of Cenarius, Heart of Y'Shaarj

### Artefacts generiques (meme/random) :
- Fichiers `*_generic_meme.txt` : armes generiques randomisees
- Fichier `wc_artifacts_generic_random_spawn.txt` : evenements de spawn aleatoire

### Constats :
- **AUCUN set bonus** - pas de concept de "Tier Set" comme dans WoW
- **Pas de crafting** - les artefacts sont obtenus par evenements ou pre-places
- **Pas de slot chest/legs/feet/shoulders** - seulement torso generique
- **Les generiques sont "meme"** - fichiers humoristiques avec artefacts generiques
- Pas de systeme d'enchantement sur les artefacts existants
- Pas de gemmes/sockets

---

## 4. Societes Secretes (wc_societies.txt)

### Societes Warcraft :
| Societe | Type | Religion | Pouvoirs |
|---------|------|----------|----------|
| Cult of the Damned | Secret/Criminal | Undead | Abduction, Raise Dead, Tainted Touch, Monstrous Undead |
| Shadow Council | Secret/Criminal | Fel | Dark magic, summoning |
| Twilight's Hammer Cult | Secret/Criminal | Old Gods | Void magic |
| Cenarion Circle | Open | Druidism | Nature magic, healing |
| Sisterhood of Elune | Open | Kaldorei | Moon magic |
| Hermetics (various) | Semi-secret | Various | Research, alchemy |

### Constats :
- Le systeme de quetes (WCQUE namespace) est lie aux societes
- Les quetes sont un "tombola" aleatoire base sur la societe
- **Pas de donjon/raid** en tant que tel - les quetes sont individuelles
- **Pas de boss fights** mechanique

---

## 5. Diplomatie (wc_diplomacy_events.txt, wc_cb_types.txt)

### Casus Belli Warcraft :
| CB | Type | Conditions |
|----|------|-----------|
| total_invasion | Conquete totale | Independant, 500 prestige + 250 piete |
| stop_invader | Defensive | Contre envahisseurs d'Azeroth |
| (+ CBs vanilla adaptes) | Varies | Adaptes au contexte WC |

### Interactions diplomatiques WC :
- **Alliance Nain-Gnome** (WCDIP.9-10) : Alliance automatique entre Ironforge et Gnomeregan
- **Diplomatie raciale** : Modificateurs d'opinion par race (same_opinion vs general_opinion)
- **Relations Horde/Alliance** : Via les religions et cultures

### Constats :
- La diplomatie est **largement vanilla** avec des modifications cosmetiques
- **Pas de pacte de faction** (Alliance/Horde officielle)
- **Pas de negotiations specifiques** (echange d'artefacts, demande d'aide heroique)
- **Pas de duels rituels** entre champions
- **Pas de tournois WoW-style** (arene PvP)
- **Pas de systeme d'ambassade** entre races
- **Pas de commerce d'artefacts** entre personnages

---

## 6. Ce qui MANQUE - Opportunites d'amelioration

### 6.1 Equipement / Crafting
- Pas de **tier sets WoW** (T1 Molten Core, T2 BWL, T3 Naxx, etc.)
- Pas de **crafting** (forgeage d'armes, enchantement, joaillerie)
- Pas de **slots supplementaires** (shoulders, legs, feet, off-hand)
- Pas de **set bonus** (2pc/4pc comme dans WoW)
- Pas de **qualite d'arme variable** (pas de "of the Bear", "of the Eagle")
- Pas de **desenchantement** / recyclage

### 6.2 Donjons & Raids
- Pas de **systeme de donjon** (MC, BWL, AQ, Naxx, Kara)
- Pas de **boss encounters** scriptees
- Pas de **loot table** par donjon
- Pas de **progression PvE** (attunement, pre-requis)
- Pas de **groupe/raid** (former un groupe de 5/10/25)

### 6.3 Diplomatie
- Pas de **systeme de faction** Alliance/Horde formel
- Pas de **duels d'honneur** entre champions
- Pas de **echange/commerce d'artefacts**
- Pas de **missions diplomatiques** specifiques (emissaire, ambassade)
- Pas de **pactes de non-agression** raciaux
- Pas de **conseil de guerre** inter-races

### 6.4 Stats / Classes
- Pas de **specialisations** de classe
- Pas de **talents** (arbre de talents)
- Pas de **monture** comme equipement
- Pas de **familier** (pet pour hunter, demon pour warlock)
