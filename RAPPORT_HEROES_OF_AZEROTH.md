# RAPPORT : GoA Heroes of Azeroth - Submod Complet

## Vue d'Ensemble

**Nom** : GoA: Heroes of Azeroth
**Type** : Submod pour Warcraft: Guardians of Azeroth (CK2)
**Fichiers** : 10 fichiers, ~2,500 lignes de script
**Localisation** : 4 langues (EN/FR/DE/ES)

Ce submod ajoute des systemes inspires de World of Warcraft au mod GoA :
- Systeme de **Tier Sets** (T1, T2) avec loot specifique par classe
- Systeme de **Crafting** (forge, enchantement, desenchantement)
- **Donjons et Raids** (Molten Core, Blackwing Lair, Naxxramas)
- **Diplomatie amelioree** (duels, pactes, ambassades, mentorat)

---

## 1. SYSTEME DE TIER SETS (Artefacts WoW)

### T1 - Molten Core (Qualite 3 / Rare)

| Classe   | Set              | Pieces          | Stats Principales                          |
|----------|------------------|-----------------|--------------------------------------------|
| Warrior  | Battlegear of Might | Crown, Torso, Wrist | martial +4, combat_rating +18, health +0.3 |
| Mage     | Arcanist Regalia    | Crown, Torso, Wrist | learning +5, combat_rating +11, tech +0.02 |
| Paladin  | Lawbringer Armor    | Crown, Torso     | martial +2, learning +1, piety +0.25       |
| Rogue    | Nightslayer Armor   | Crown, Torso     | intrigue +3, combat_rating +11, murder +0.02|
| Hunter   | Giantstalker Armor  | Crown, Torso     | martial +2, combat_rating +10, archers +3% |
| Shaman   | The Earthfury       | Crown, Torso     | learning +2, martial +1, piety +0.25       |

**Condition d'activation** : Classe niveau 5+ OU flag `hoa_t1_<class>_earned`

### T2 - Blackwing Lair (Qualite 4 / Epic)

| Classe   | Set                 | Pieces       | Stats Principales                              |
|----------|---------------------|--------------|-------------------------------------------------|
| Warrior  | Battlegear of Wrath | Crown, Torso | martial +5, combat_rating +22, morale +3%/+3%  |
| Mage     | Netherwind Regalia  | Crown, Torso | learning +5, combat_rating +14, tech_growth +10%|

**Condition d'activation** : Flag `hoa_t2_<class>_earned` (obtenu en battant le boss)

### Equipements Craftes

| Type         | Uncommon (Q2)          | Rare (Q3)               | Epic (Q4)                   |
|-------------|------------------------|-------------------------|-----------------------------|
| Epee        | martial +1, CR +8      | martial +2, CR +12      | martial +2, diplo +1, CR +16|
| Baton       | learning +1, CR +6     | learning +2, CR +10     | -                           |
| Armure      | martial +1, HP +0.2    | martial +1, HP +0.4     | -                           |
| Anneau      | HP +0.3                | HP +0.5, tax +2%        | -                           |
| Amulette    | diplo +1, HP +0.2      | diplo +1, learn +1      | -                           |

**Total** : 20 artefacts uniques (14 tier set + 11 craftes = 25 definitions)

---

## 2. SYSTEME DE CRAFTING (Decisions)

### Forge d'Equipement (Uncommon)
- **Cout** : 100 or
- **Conditions** : martial >= 8 OU stewardship >= 10 OU nain/gobelin
- **Resultat** : Arme, armure ou bijou aleatoire (qualite Uncommon)
- **Cooldown** : 1 an
- **Repartition** : 50% arme (staff si mage, epee sinon), 30% armure, 20% bijou

### Forge d'Equipement Superieur (Rare)
- **Cout** : 300 or
- **Conditions** : martial >= 12 OU stewardship >= 14, doit etre nain/gobelin/humain ou posseder un craft
- **Resultat** : Equipement rare aleatoire
- **Cooldown** : 2 ans

### Forge de Chef-d'Oeuvre (Epic)
- **Cout** : 750 or
- **Conditions** : martial >= 14, stewardship >= 12, nain/gobelin OU posseder un artefact craft Q3+
- **Resultat** : Epee epique (martial +2, diplo +1, CR +16)
- **Cooldown** : 5 ans

### Enchantement d'Arme
- **Cout** : 200 or
- **Conditions** : learning >= 10, classe magique (mage/warlock/priest/druid/shaman) ou gnome/gobelin
- **Effet** : +5 combat_rating, +1 martial pendant 10 ans
- **Cooldown** : 2 ans

### Desenchantement
- **Conditions** : learning >= 6, posseder un artefact non equipe
- **Resultat par qualite** :
  - Epic (Q4+) : 300 or + 50 prestige
  - Rare (Q3) : 150 or + 25 prestige
  - Uncommon (Q2) : 75 or + 10 prestige
  - Common (Q1) : 25 or
- **Cooldown** : 6 mois

---

## 3. SYSTEME DE DONJONS ET RAIDS

### Declenchement
- Event aleatoire (MTTH = 8 ans)
- Conditions : dirigeant adulte, classe active, martial/learning/intrigue >= 10
- Accelerateurs : trait brave/ambitieux (-50%), martial >= 15 (-30%), possede tier set (-20%)

### Molten Core (Le Coeur du Magma)
- **Difficulte** : Normale (martial >= 10)
- **Cout d'entree** : 100 or + 50 prestige
- **Duree** : 30 jours
- **Boss** : Ragnaros le Seigneur du Feu

| Resultat | Chance | Modifieurs | Recompenses |
|----------|--------|------------|-------------|
| Grand Succes | 35% | +50% si martial>=15, +30% si classe 7+, +20% si brave | 200 or, 150 prestige, T1 piece + titre "Slayer of Ragnaros" |
| Succes Modere | 35% | - | 75 or, 50 prestige, anneau/amulette uncommon |
| Echec | 20% | -50% si martial>=15 | -50 prestige, trait Wounded |
| Catastrophe | 10% | -70% si martial>=15, x2 si craven | -100 prestige, trait Severely Injured, -50 or |

**Loot T1 par classe** : piece aleatoire parmi le set (couronne, torse, ou poignets selon la classe)

### Blackwing Lair (Le Repaire de l'Aile Noire)
- **Difficulte** : Difficile (martial >= 14, necessite T1)
- **Cout d'entree** : 200 or + 100 prestige
- **Duree** : 45 jours
- **Boss** : Nefarian, fils d'Aile de Mort

| Resultat | Chance | Recompenses |
|----------|--------|-------------|
| Grand Succes | 25% | 400 or, 250 prestige, T2 piece + titre "Slayer of Nefarian" |
| Succes Modere | 35% | 150 or, 75 prestige, anneau/armure rare |
| Echec | 25% | -75 prestige, trait Wounded |
| Catastrophe | 15% | -150 prestige, Severely Injured, -1 sante |

### Naxxramas (La Citadelle de l'Effroi)
- **Difficulte** : Extreme (martial >= 16, learning >= 12, necessite T2)
- **Cout d'entree** : 400 or + 200 prestige
- **Duree** : 60 jours
- **Boss** : Kel'Thuzad, l'Archliche

| Resultat | Chance | Recompenses |
|----------|--------|-------------|
| Grand Succes | 15% | 800 or, 500 prestige, 100 piete, arme epic + titre "Slayer of Kel'Thuzad" |
| Succes Modere | 30% | 250 or, 150 prestige, armure rare |
| Echec | 30% | -100 prestige, Severely Injured |
| Catastrophe | 25% | -200 prestige, Severely Injured, -3 sante (potentiellement mortel!) |

### Progression de Difficulte

```
Molten Core (10 martial) → Blackwing Lair (14 martial + T1) → Naxxramas (16 martial + T2)
     Facile                      Difficile                         Extreme
   T1 Rare (Q3)               T2 Epic (Q4)                    Epique + Legendaire
```

---

## 4. SYSTEME DIPLOMATIQUE

### Duel de Champions (Decision)
- **Cout** : 100 prestige
- **Conditions** : martial >= 12 OU combat_rating >= 20, avoir un rival dirigeant
- **Deroulement** :
  1. Decision lancee, rival selectionne aleatoirement
  2. Le rival recoit l'evenement et peut accepter ou refuser
  3. Si accepte : duel resolu par combat_rating, martial, et qualite d'arme
  4. Victoire : +200 prestige + modificateur "Champion of Honor" (10 ans)
  5. Defaite : -150 prestige + blessure
  6. Rival refuse : -100 prestige et -25 opinion pour le lache
- **Cooldown** : 5 ans

### Pacte Defensif (Decision)
- **Cout** : 200 prestige
- **Conditions** : independant, rang > Comte, diplomacy >= 10, voisin avec 25+ opinion
- **Effet** : +30 opinion avec tous les dirigeants voisins (20 ans) + bonus garnison/levy
- **Cooldown** : 20 ans

### Envoi d'Emissaire (Decision)
- **Cout** : 50 or
- **Conditions** : diplomacy >= 8, rang > Comte
- **Effet** : +15 opinion avec tous les dirigeants independants voisins (5 ans) + 25 prestige
- **Cooldown** : 5 ans

### Sommet Diplomatique (Evenement)
- **Declenchement** : MTTH 15 ans, rang > Duc, independant
- **Option A** : Grand sommet (-150 or, +100 prestige, +20 opinion voisins, bonus province)
- **Option B** : Accords commerciaux (-100 or, +50 prestige, +8% taxe globale pendant 10 ans)

### Echange d'Artefacts (Evenement)
- **Declenchement** : MTTH 10 ans, possede artefact Q2+ non equipe
- **Option A** : Vendre contre 200 or (artefact transfere a un vassal)
- **Option B** : Offrir pour faveur politique (+100 prestige, +25 opinion 10 ans)
- **Option C** : Garder tout

### Mentorat de Classe (Evenement)
- **Declenchement** : MTTH 12 ans, classe niveau 7+, courtisan jeune (<30 ans)
- **Effet** : Courtisan gagne +2 martial, +1 learning, +20 opinion
- **Modificateur** : "Wise Mentor" (+2 learning, +1 diplomacy, +0.1 piete/mois) pendant 10 ans

---

## 5. MODIFICATEURS ET TITRES

### Titres Permanents (Boss Kill)

| Titre | Stats |
|-------|-------|
| Slayer of Ragnaros | martial +2, CR +5, prestige +0.2/mois, vassal +5 |
| Slayer of Nefarian | martial +3, CR +8, prestige +0.3/mois, vassal +8 |
| Slayer of Kel'Thuzad | martial +4, CR +12, prestige +0.5/mois, vassal +10, opinion +5 |

### Modificateurs Temporaires

| Modificateur | Duree | Effets |
|-------------|-------|--------|
| Champion of Honor | 10 ans | martial +2, CR +5, prestige +0.3/mois |
| Enchanted Weapon | 10 ans | CR +5, martial +1 |
| Defensive Pact Leader | 20 ans | diplomacy +2, garrison +10%, levy +5% |
| Diplomatic Center (province) | 10 ans | tax +10%, tech_growth +15% |
| Trade Summit Bonus | 10 ans | global_tax +8%, diplomacy +1 |
| Wise Mentor | 10 ans | learning +2, diplomacy +1, piety +0.1/mois |

### Modificateurs d'Opinion

| Modificateur | Valeur | Contexte |
|-------------|--------|----------|
| Refused Duel | -25 | Refuser un duel de champion |
| Duel Victor | +15 | Gagner un duel |
| Hosted Summit | +20 | Organiser un sommet |
| Defensive Pact | +30 | Former un pacte defensif |
| Sent Emissary | +15 | Envoyer un emissaire |
| Generous Gift | +25 | Offrir un artefact |

---

## 6. TRIGGERS ET CLASSES SUPPORTEES

Le submod detecte les 11 classes de GoA via des scripted triggers :

| Trigger | Classes (niveaux 1-10) |
|---------|------------------------|
| `is_warrior_class_trigger` | class_warrior_1 a class_warrior_10 |
| `is_mage_class_trigger` | class_mage_1 a class_mage_10 |
| `is_paladin_class_trigger` | class_paladin_1 a class_paladin_10 |
| `is_rogue_class_trigger` | class_rogue_1 a class_rogue_10 |
| `is_hunter_class_trigger` | class_hunter_1 a class_hunter_10 |
| `is_shaman_class_trigger` | class_shaman_1 a class_shaman_10 |
| `is_priest_class_trigger` | class_priest_1 a class_priest_10 |
| `is_warlock_class_trigger` | class_warlock_1 a class_warlock_10 |
| `is_druid_class_trigger` | class_druid_1 a class_druid_10 |
| `is_deathknight_class_trigger` | class_death_knight_1 a class_death_knight_10 |
| `is_monk_class_trigger` | class_monk_1 a class_monk_10 |
| `is_magic_class_trigger` | Mage, Warlock, Priest, Druid, Shaman |
| `has_any_class_trigger` | Toutes les 11 classes |

---

## 7. STRUCTURE DES FICHIERS

```
GoA_Heroes_of_Azeroth/
├── GoA_Heroes_of_Azeroth.mod          # Descripteur (depend de GoA)
├── common/
│   ├── artifacts/
│   │   └── hoa_tier_sets.txt           # 25 artefacts (571 lignes)
│   ├── event_modifiers/
│   │   └── hoa_modifiers.txt           # 13 modificateurs (93 lignes)
│   └── scripted_triggers/
│       └── hoa_triggers.txt            # 13 triggers de classe (192 lignes)
├── decisions/
│   ├── hoa_crafting_decisions.txt      # 5 decisions de craft (301 lignes)
│   └── hoa_diplomacy_decisions.txt     # 3 decisions diplo (192 lignes)
├── events/
│   ├── hoa_dungeon_events.txt          # 4 events de donjon (479 lignes)
│   └── hoa_diplomacy_events.txt        # 6 events diplo (406 lignes)
└── localisation/
    ├── hoa_events.csv                  # Trad events (37 lignes, 4 langues)
    └── hoa_decisions.csv               # Trad decisions (33 lignes, 4 langues)
```

**Total** : 10 fichiers, ~2,500 lignes

---

## 8. COMPATIBILITE ET INSTALLATION

- **Dependance** : Warcraft: Guardians of Azeroth (requis)
- **Compatible** : GoA Improved Economy (notre premier submod)
- **Conflits** : Aucun conflit connu (fichiers 100% nouveaux, prefixe `hoa_`)
- **Installation** : Copier le dossier dans `Documents/Paradox Interactive/Crusader Kings II/mod/`

---

## 9. GAMEPLAY : BOUCLE DE JEU TYPIQUE

```
1. DEBUT : Personnage avec une classe (ex: Warrior niveau 5)
   │
   ├─→ CRAFTING : Forge d'equipement uncommon (100 or)
   │   └─→ Obtient une epee uncommon (+1 martial, +8 CR)
   │
   ├─→ DONJON : Event Molten Core se declenche (~8 ans)
   │   ├─→ Succes → T1 Battlegear of Might (crown/torso/wrist)
   │   │   └─→ Titre permanent "Slayer of Ragnaros"
   │   └─→ Echec → Blessure, perte d'or
   │
   ├─→ DIPLOMATIE : Duel de champion contre un rival
   │   └─→ Victoire → "Champion of Honor" (+2 martial, +5 CR)
   │
   ├─→ CRAFT AVANCE : Forge d'equipement rare (300 or)
   │   └─→ Enchantement de l'arme (+5 CR, +1 martial, 10 ans)
   │
   ├─→ DONJON AVANCE : Blackwing Lair (necessite T1)
   │   └─→ Succes → T2 Battlegear of Wrath (+22 CR total!)
   │
   ├─→ DIPLOMATIE : Pacte defensif + sommet
   │   └─→ +30 opinion voisins, +10% garnison
   │
   └─→ DONJON ULTIME : Naxxramas (necessite T2, martial 16+)
       └─→ Succes → 800 or + arme epique + "Slayer of Kel'Thuzad"
           └─→ Le personnage le plus puissant d'Azeroth !
```

---

## 10. STATISTIQUES RECAPITULATIVES

| Categorie | Quantite |
|-----------|----------|
| Artefacts definis | 25 |
| Tier Sets complets | 8 (6 T1 + 2 T2) |
| Decisions joueur | 8 (5 craft + 3 diplo) |
| Events | 10 (4 donjon + 6 diplo) |
| Modificateurs | 13 (6 permanents + 7 opinion) |
| Scripted Triggers | 13 |
| Langues supportees | 4 (EN/FR/DE/ES) |
| Lignes de code | ~2,500 |
| Fichiers | 10 |

---

## Combine avec GoA Improved Economy

Les deux submods ensemble ajoutent :
- **~5,700 lignes** de contenu script
- **23 fichiers** de mod
- Economie amelioree (batiments culturels, mines, marches)
- Systeme heroique complet (raids, craft, diplomatie)
- Support de **11 classes WoW** et **30+ races**
- Localisation complete en **4 langues**
