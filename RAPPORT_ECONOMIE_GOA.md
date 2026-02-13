# Rapport Complet : Economie et Batiments - Warcraft: Guardians of Azeroth (CK2)

## 1. Vue d'ensemble du mod

**Warcraft: Guardians of Azeroth** (GoA) est le mod Warcraft de reference pour Crusader Kings II. Il recree le monde d'Azeroth avec 1419 provinces, des dizaines de cultures (humains, orcs, elfes de la nuit, nains, trolls, gobelins, draenei, etc.), des religions uniques et un systeme economique adapte a l'univers Warcraft.

- **Version** : v1.10.0 (compatible CK2 3.3.x)
- **Date de depart** : 583 (Premiere Guerre)
- **Date de fin** : 900
- **Provinces** : 1419
- **Fichiers de batiments** : 21 fichiers (~26,839 lignes)

---

## 2. Systeme de Batiments - Analyse Complete

### 2.1 Batiments de Chateau (Castle)

**Fichier principal** : `00_Castle.txt` (1106 lignes)

| Batiment | Niveaux | Cout total (or) | Bonus principal |
|----------|---------|------------------|-----------------|
| Murailles (ca_wall) | 5 | 500 | Fort +3.5, Tax +1.3/mois |
| Qualite des murs (ca_wall_q) | 5 | 350 | Fort +2.5 |
| Donjon (ca_keep) | 6 | 2050 | Levy +1.05, Garrison +0.7 |
| Caserne milice (ca_militia_barracks) | 4 | 720 | Infantry+Archers |
| Caserne (ca_barracks) | 6 | 1620 | Heavy Infantry |
| Terrain d'entrainement (ca_training) | 3 | 750 | Morale +0.45, Retinue +60 |
| Ecuries (ca_stable) | 6 | 810 | Light Cavalry |
| **Voliere WC (wcca_aviary)** | 6 | 810 | **Knights (aerien)** |
| Ville du chateau (ca_town) | 6 | 1620 | **Tax +12/mois, Court +6** |
| Chantier naval (ca_shipyard) | 4 | 400 | Galleys |
| Fortif. Bloodline Castellan | 4 | 1575 | Fort, Morale, Garrison |
| Fortif. Bloodline Murder | 4 | 1125 | Revolt risk, Prestige |

**Observations critiques** :
- La **Voliere** (`wcca_aviary`) est le seul batiment Warcraft-specifique dans les chateaux de base - elle remplace les ecuries pour les unites aeriennes (knights = griffons, wyvernes, etc.)
- Le **ca_town** est le seul batiment generateur d'or dans les chateaux : +2 or/mois par niveau, soit +12 or max pour 1620 or investi
- **ROI ca_town** : 1620 or / 12 or par mois = 135 mois (11.25 ans) pour se rembourser - mediocre
- Les murailles donnent un faible +0.2 or/mois par niveau (sauf niveau 5 qui donne +0.5)

### 2.2 Batiments de Cite (City)

**Fichier** : `00_buildings.txt` (2407 lignes, section city)

| Batiment | Niveaux | Bonus principal |
|----------|---------|-----------------|
| Murailles cite (ct_wall) | 5 | Fort, Levy, Tax +1.3 |
| Arsenal republique (ct_rep_arsenal) | 3 | Fort, Levy, Galleys |
| Marketplace | 6 | **Tax principal des cites** |
| Port | 4 | Tax, Galleys |
| Garde civique | Multiple | Troops |

**Observation** : Les cites sont la source principale de revenus fiscaux dans le jeu vanilla, mais GoA n'a pas ajoute de batiments economiques specifiques a Warcraft pour les cites.

### 2.3 Batiments Tribaux

**Fichiers** : `00_tribal.txt` (919 lignes), `00_tribalCulture.txt` (4955 lignes)

- Systeme vanilla standard avec piliers tribaux
- Les batiments culturels tribaux sont **purement militaires** (troupes)
- **Aucun batiment tribal ne genere du revenu** significatif - c'est un probleme connu

### 2.4 Batiments Culturels (Warcraft-specifiques)

**Fichier** : `wc_castle_culture.txt` (6682 lignes - le plus gros fichier !)

Cultures ayant des batiments specifiques :
- **Dryades** : Horse Archers (4 niveaux, 150-375 or)
- **Vulpera** : Archers avec bonus off/def
- **Gobelins** : (probablement ingenierie/machines)
- **Nains** : (forge, militaire)
- **Elfes de la nuit** : (probablement archers/casters)
- **Orcs** : (probablement heavy infantry)
- **Humains** : (mixte)
- **Trolls** : (tirailleurs)
- **Tauren** : (cavalerie lourde)
- **Draenei** : (mixte sacre)
- **Et beaucoup d'autres...**

**Observation critique** : Ces batiments sont **100% militaires**. Aucun batiment culturel ne donne de bonus economique (tax_income, local_tax_modifier, economy_techpoints).

### 2.5 Batiments Uniques Warcraft

**Fichier** : `wc_uniques.txt` (211 lignes)

| Batiment | Localisation | Cout | Bonus |
|----------|-------------|------|-------|
| tp_nordrassil (Nordrassil) | b_nordrassil | 5000 piete | Tax +25%, Prestige, Pikemen 75, Fort +2 |
| ca_vault_of_archavon | b_wintergrasp_2 | 1 or | Tax +1, Fort +2.5 |
| ca_eye_of_eternity | b_nexus | 1 or | Prestige, Infantry 150, Fort +1.5 |
| wc_dwarf_armory5 | b_great_forge | 1250 or | Prestige, Tech militaire, Morale |
| **Frozen Throne** (commente) | b_icecrown | 1 or | Undead 2500, Fort +2 |
| **Icecrown Citadel** (commente) | b_icecrown | 3000 or | Undead 7500, Fort +5 |

**Observation** : Les batiments uniques sont interessants mais tres peu nombreux (seulement 4 actifs). Le Frozen Throne et la Citadelle de la Couronne de Glace sont COMMENTES et non-fonctionnels.

### 2.6 Batiments Druidiques

**Fichier** : `wc_druidic.txt` (69 lignes)

| Batiment | Cout | Bonus |
|----------|------|-------|
| Arbre-Monde (tp_world_tree) | 2500 piete | Tax +15%, Prestige, Pikemen 50, Fort +1 |
| Arbre Cauchemar (tp_nightmare_tree) | 2500 piete | Levy +25%, Morale +25%, Fort +1 |

### 2.7 Forts

**Fichier** : `wc_fort.txt` (49 lignes)

| Batiment | Cout | Bonus |
|----------|------|-------|
| Tour de guet (wcfo_tower) | 10-20 or | Fort +1/+2 |
| Garnison (wcfo_patrols) | 10-20 or | Garrison +75%/+150% |

### 2.8 Hopitaux Warcraft

**Fichier** : `wc_hospital.txt` (36 lignes)

- **Enclave Cenarienne** (hp_cenarion_enclave) : Disease defense +20%, Tax +0.5, Tech growth +25%
- Doublon temple/hopital selon DLC Reaper's Due

### 2.9 Postes de Commerce (Trade Posts)

**Fichiers** : `00_tradepost.txt`, `01_tradepost.txt`, `wc_tradepost.txt`, `wc_tradepost_culture.txt`, `wc_tradepost_religion.txt`

**Vanilla** : Ports (tradevalue +10/15/20), Enclaves (tax +1/1.5/2)

**Warcraft-specifique** :
- **Plantation de bananes** (3 niveaux) : trade_route_wealth +5/10/15, tradevalue +100/150/200
- **Distillerie de rhum banane** : trade_route_wealth +5, economy_techpoints

**Postes culturels** (necessitent TECH_TRADE_PRACTICES 3) :
| Culture | Cout | Bonus special |
|---------|------|---------------|
| Gobelin | 250 | Tech growth +12.5%, trade_wealth +1 |
| Elfe de la nuit | 225 | Piete, Tech culture |
| Humain/Haut-elfe/Draenei | 475 | Trade wealth +4, tradevalue +30 |
| Tauren/Tuskarr/Orc | 275 | Retinue +30, trade_wealth +1 |
| Harpy | 300 | Tech growth +12.5% |
| Troll | 325 | Tech culture, trade_wealth +2 |
| Nain | 375 | Garrison +150%, retinue +10 |
| Kobold | 200 | Economy+Culture tech |
| Gnome | 200 | All 3 techpoints |
| Murloc | 400 | Tech growth +20%, tradevalue +25 |
| Generique | 275 | Garrison +50%, tradevalue +20 |

**Religion** :
- Arcane Religion : Tech growth +30%, all techpoints

---

## 3. Systeme Commercial (Trade Routes)

### 7 routes commerciales definies :

| Route | Richesse base | Bonus tax |
|-------|--------------|-----------|
| Eastern Kingdoms Nord | 50 | +14% castle/city/temple/tribal |
| Eastern Kingdoms Sud | ? | +14% |
| Eastern Kingdoms Mer Ouest | ? | ? |
| Great Sea | ? | ? |
| Kalimdor | ? | ? |
| Kalimdor Mer Est | ? | ? |
| Pandaria | ? | ? |

**Observation** : La route EK Nord donne +14% tax et +28% tech growth a toutes les provinces traversees. Les routes commerciales sont un multiplicateur puissant mais mal exploite - seules les bananeraies ont des batiments WC dedies.

---

## 4. Lois Economiques

### Systeme d'obligations (ze_obligation_laws.txt)

Slider Tax/Levy pour chaque type de vassal :
- Feudal, Iqta, Republique, Theocratie, Tribal
- 4 niveaux allant de "focus levy" a "focus tax"

**Observation** : Systeme vanilla standard, pas de modification Warcraft.

---

## 5. Defines et Modificateurs Statiques

### defines.txt
- **Minimaliste** : Le mod ne modifie PAS les defines economiques de base !
- Les sections `character`, `diplomacy`, `economy`, `military` sont toutes VIDES
- Cela signifie que tous les parametres economiques de base (taux de taxe, couts, etc.) sont ceux de vanilla CK2

### static_modifiers.txt
- Modificateurs d'occupation : jusqu'a -150% tax quand occupe
- Nouvelle administration : -30% tax
- Pillage : -25% tax
- Jizya tax : +25% tax
- Risque de revolte : -1% tax par point
- **Aucun modificateur Warcraft-specifique** pour l'economie

---

## 6. Gouvernements

5 types de gouvernement (fichiers vanilla) :
- Feodal, Nomade, Republique, Theocratie, Tribal

**Observation** : Pas de gouvernement Warcraft-specifique (pas de "Horde council", pas de "Kirin Tor magocracy", etc.)

---

## 7. Problemes Identifies et Faiblesses

### 7.1 Economie trop faible
- Les batiments economiques sont essentiellement les memes que vanilla
- ca_town est le seul batiment generateur d'or dans les chateaux, avec un ROI tres lent
- **Aucun batiment culturel ne donne de revenus** - ils sont 100% militaires
- Les defines economiques ne sont pas modifies (sections vides)

### 7.2 Manque de diversite economique
- Pas de batiments de mine (or, mithril, thorium, saronite...)
- Pas de batiments de magie (enchantement, alchimie, portails...)
- Pas de batiments de production (forge, ingenierie gobeline, joaillerie...)
- Pas de batiments d'agriculture specifiques aux races (champignonniere Undead, ferme Tauren...)

### 7.3 Batiments uniques sous-exploites
- Seulement 4 batiments uniques actifs sur tout Azeroth (1419 provinces !)
- Frozen Throne/Icecrown commentes et non-fonctionnels
- Pas de batiment unique pour : Orgrimmar, Thunder Bluff, Darnassus, Gnomeregan, Undercity, Dalaran, Silvermoon (en tant que batiments de prestige/economie)

### 7.4 Commerce incomplet
- Routes commerciales presentes mais sous-exploitees
- Plantations de bananes comme seul batiment WC de trade post
- Pas de mines sur routes commerciales
- Pas de batiments de commerce inter-continental

### 7.5 Systeme de technologie non-adapte
- Le mod utilise le systeme tech vanilla sans modification
- Pas de "tech magique" ou "tech ingenerie" propre a Warcraft
- Les techpoints generes par les batiments sont identiques a vanilla

### 7.6 Desequilibre racial
- Les cultures "riches" (humains, hauts-elfes, nains) n'ont pas d'avantage economique
- Les gobelins, censurees etre les maitres du commerce, n'ont rien de special
- Les cultures tribales (trolls, taurens) n'ont aucune economie viable

---

## 8. Recommandations pour le Submod "Improved Economy"

### 8.1 Nouveaux batiments economiques par type de holding
- **Mines** (or, fer, mithril, thorium, saronite, gemmes) avec revenus par terrain
- **Ateliers magiques** (enchantement, alchimie, ingenierie) avec revenus + tech
- **Marches specialises** par race/culture
- **Batiments de production** adaptes aux cultures

### 8.2 Batiments culturels economiques
- Chaque groupe culturel devrait avoir 1-2 batiments economiques uniques :
  - Gobelins : Comptoir Commercial, Usine d'Ingenierie
  - Nains : Grande Forge, Mine Profonde
  - Elfes : Jardin Lunaire, Tour d'Enchantement
  - Humains : Guilde des Marchands, Academie
  - Orcs : Marche des Trophees, Forge de Guerre
  - Undead : Atelier des Abominations, Mine de Saronite
  - Trolls : Marche Voodoo, Temple des Esprits
  - Taurens : Ranch des Plaines, Totem Commerce

### 8.3 Batiments uniques pour les capitales majeures
- Stormwind : District Commercial (+tax, +trade)
- Orgrimmar : Grande Forge de la Horde (+military tech, +tax)
- Ironforge : Grande Forge des Profondeurs (+economy tech, +tax)
- Undercity : Quartier des Apothicaires (+disease, +tax)
- Darnassus : Enclave du Temple (+piety, +tax, +culture tech)
- Silvermoon : Promenade du Soleil (+prestige, +tax, +magic)
- Thunder Bluff : Plateaux Sacres (+piety, +morale, +tax)
- Dalaran : Cite Magique Violette (+all tech, +tax)
- Gnomeregan : Atelier des Inventeurs (+military tech, +economy tech)
- Boralus : Grand Port (+trade, +galleys, +tax)

### 8.4 Equilibrage
- Augmenter les revenus de base des batiments existants de ~20-30%
- Reduire les couts de construction de ~15% pour accelerer le developpement
- Ajouter des bonus economiques aux batiments culturels existants
- Creer des synergies entre batiments (ex: mine + forge = bonus)
