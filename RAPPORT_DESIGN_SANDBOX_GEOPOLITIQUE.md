# Design Document : Sandbox & Geopolitique - GoA Submods

## Vue d'ensemble

Ce document capture les recommandations de design pour transformer les submods GoA (Heroes of Azeroth + Improved Economy) en une experience sandbox politique de niveau SOTA. Il s'appuie sur l'audit complet du contenu existant et identifie les lacunes majeures par rapport aux standards de CK2 (Conclave, Way of Life, Monks & Mystics) et EU4.

**Constat central** : Le mod actuel est un excellent dungeon crawler (raids, tier sets, crafting) greffe sur CK2, mais le jeu politique entre personnages - le coeur de CK2 - est quasi-inexistant. Les conseillers, commandants, vassaux et courtisans n'ont aucune mecanique specifique au mod.

---

## PARTIE 1 : AUDIT DE L'EXISTANT

### 1.1 Ce qui existe dans le mod GoA de base

| Systeme | Fichier source | Contenu |
|---------|---------------|---------|
| 11 classes WoW (10 niveaux) | `wc_class_traits.txt` | warrior, mage, paladin, rogue, hunter, shaman, priest, warlock, druid, death_knight, monk |
| 30+ races | `wc_race_traits.txt` | human, orc, nightelf, dwarf, gnome, troll, tauren, undead, bloodelf, draenei, goblin, worgen, naga, dragons... |
| 6 societes secretes | `wc_societies.txt` | Cult of the Damned, Shadow Council, Twilight's Hammer, Cenarion Circle, Sisterhood of Elune, Hermetics |
| Artefacts legendaires | 26 fichiers, 10,877 lignes | Ashbringer, Doomhammer, Felo'melorn, Skull of Gul'dan, etc. |
| 7 routes commerciales | `wc_traderoutes.txt` | EK Nord, EK Sud, Great Sea, Kalimdor, etc. |
| Diplomatie raciale | `wc_diplomacy_events.txt` | Alliance Nain-Gnome, opinion raciale |
| 2 casus belli WC | `wc_cb_types.txt` | total_invasion, stop_invader |
| 5 gouvernements vanilla | non modifie | feodal, nomade, republique, theocratie, tribal |

### 1.2 Ce que les submods ajoutent (Heroes of Azeroth + Improved Economy)

| Systeme | Fichiers | Contenu |
|---------|---------|---------|
| Tier Sets T1/T2 | `hoa_tier_sets.txt` | 6 classes x T1 (Rare) + 2 classes x T2 (Epic) |
| Dungeon drops T0/T0.5 | `hoa_t0_sets.txt` | 5 dungeons T0 + 3 dungeons T0.5 + 1 raid 20-man + 4 raids 40-man |
| Crafting | `hoa_crafting_decisions.txt` | Forge uncommon/rare/epic, enchantement, desenchantement |
| 14 decisions "power" | `hoa_power_decisions.txt` | Walk streets, tavern, feast, tour, monument, train, trade, magic enterprise, arena, study, arts, infrastructure, bodyguard, explore |
| 3 decisions diplo | `hoa_diplomacy_decisions.txt` | Duel de champion, pacte defensif, emissaire |
| Batiments economiques | `ie_castle_economy.txt`, `ie_culture_economy.txt` | Mines (5 tiers), ateliers arcaniques, forges, marches, scieries + 11 batiments culturels |
| Capitales uniques | `ie_unique_capitals.txt` | Stormwind, Orgrimmar, Ironforge, Thunderbluff, Gnomeregan, Boralus, Dalaran, Darnassus, Silvermoon |
| Retinues raciales | `hoa_race_retinues.txt` | ~30 unites specifiques par race (962 lignes) |
| Events economiques | `ie_economy_events.txt` | Gold vein, trade caravan, arcane boom, goblin investor, harvest |

### 1.3 Ce qui manque - Le diagnostic

| Domaine | Score actuel | Probleme |
|---------|-------------|----------|
| **Chancelier** | 0/10 | Aucune mecanique au-dela de vanilla |
| **Intendant** | 1/10 | 1 seule decision (trade company) sans lien avec le stewardship de l'intendant |
| **Maitre-espion** | 0/10 | Zero mecanique, zero event, zero decision |
| **Marechal** | 0/10 | Aucune mecanique au-dela de vanilla |
| **Commandants** | 1/10 | Retinues raciales mais 0 gameplay de commandement |
| **Politique interne** | 0/10 | Factions vanilla non etendues |
| **Gouvernements** | 0/10 | Vanilla pur, aucun gouvernement Warcraft |
| **Cour** | 0/10 | Courtisans inactifs au-dela de vanilla |
| **Impact de la classe** | 2/10 | La classe impacte les raids mais pas la politique |
| **Reputation** | 0/10 | Aucun systeme de reputation internationale |

---

## PARTIE 2 : 10 RECOMMANDATIONS SANDBOX

Ces recommandations ajoutent des systemes de gameplay emergeant qui generent des histoires uniques a chaque partie.

### 2.1 Specialisation de Classe (Talent Trees)

**Concept** : Au niveau de classe 5, le joueur choisit une specialisation via decision. La spec modifie les bonus de trait et debloque des decisions exclusives.

**Specs par classe** :

| Classe | Spec A | Spec B | Spec C |
|--------|--------|--------|--------|
| Warrior | Arms (+4 martial, burst damage) | Protection (+1 health, +30% garrison, vassal opinion) | Fury (double-wield, berserker trait, risque blessure) |
| Mage | Frost (CC, diplomacy, slow enemies) | Fire (raw damage, AOE province devastation) | Arcane (tech growth, economy, enchanting power) |
| Rogue | Assassination (murder plot +100%, poison) | Subtlety (spy network +50%, scheme power) | Outlaw (piracy income, naval, gold steal) |
| Paladin | Holy (healing +2, piety bonus) | Protection (fort level +1, garrison) | Retribution (combat rating +15, smite) |
| Hunter | Beast Mastery (companion pet, +2 martial) | Marksmanship (archer command +15%) | Survival (exploration bonus, herb finding) |
| Shaman | Elemental (combat spells, siege bonus) | Enhancement (melee hybrid, +martial +combat) | Restoration (healing, disease defense +30%) |
| Priest | Holy (healing, +piety, disease defense) | Discipline (shield, +health, hybrid) | Shadow (void power, +intrigue, corruption risk) |
| Warlock | Affliction (DOT, weaken enemies over time) | Demonology (summon demon companion) | Destruction (raw power, risk of self-damage) |
| Druid | Balance (spellcaster, +learning, +tech) | Feral (shapeshifter, +martial, +combat) | Restoration (nature healing, +health, +piety) |
| Death Knight | Blood (lifesteal, +health regen) | Frost (burst damage, +combat rating) | Unholy (raise dead, summon ghouls, +intrigue) |
| Monk | Brewmaster (tank, +health, +garrison) | Windwalker (agile, +combat, +intrigue) | Mistweaver (healing, +learning, +diplo) |

**Implementation CK2** :
- Decision `hoa_choose_specialization` avec condition `class_X_5` minimum
- Ajoute un trait `spec_X_Y` qui modifie les bonus du trait de classe
- Les decisions exclusives par spec sont gated par `has_trait = spec_X_Y`

**Fichiers a creer** :
- `common/traits/hoa_spec_traits.txt` - 33 nouveaux traits (11 classes x 3 specs)
- `decisions/hoa_spec_decisions.txt` - 11 decisions de choix de spec
- `events/hoa_spec_events.txt` - event chains par spec
- `localisation/hoa_specs.csv`

---

### 2.2 Artefacts Evolutifs (Heirloom + Socket System)

**Concept** : Les artefacts gagnent de l'XP via des victoires (raids, duels, guerres). A certains seuils, un event fire et l'item monte de tier. Certains items sont "heirloom" et passent a l'heritier.

**Mecaniques** :

| Composant | Implementation |
|-----------|---------------|
| XP tracking | Hidden character modifier `hoa_weapon_xp_X` (1-5) ajoute apres chaque victoire |
| Evolution | Event chain quand XP atteint le seuil : l'item est detruit et remplace par la version superieure |
| Gemmes | Nouveaux artefacts slot=relic : gemme_force, gemme_agilite, gemme_intellect, gemme_endurance |
| Socketing | Decision `hoa_socket_gem` : detruit la gemme, ajoute un modifier permanent a l'arme |
| Heirloom | Flag `hoa_heirloom_weapon` sur l'artefact, on_death event transfere a l'heritier |
| Corruption | Si porteur a trait cruel/possessed, MTTH 5 ans : event "l'arme murmure" → choix : accepter (bonus +5 combat, -1 health/an) ou resister |

**Seuils d'evolution** :
- Uncommon → Rare : 3 victoires (raids ou guerres)
- Rare → Epic : 5 victoires + 1 boss kill
- Epic → Legendary : 10 victoires + 2 boss kills + 500 prestige

**Fichiers a creer** :
- `common/artifacts/hoa_evolving_artifacts.txt`
- `common/artifacts/hoa_gems.txt`
- `events/hoa_artifact_evolution.txt`
- `decisions/hoa_socket_decisions.txt`

---

### 2.3 Extension des Societes Secretes Existantes

**Concept** : Etendre les 6 societes existantes du mod GoA de base avec des rangs plus profonds, des missions inter-joueurs, et des interactions avec les systemes du submod (raids, crafting, diplomatie).

**IMPORTANT** : Les societes suivantes existent DEJA dans `wc_societies.txt` :
- Cult of the Damned (criminal/undead)
- Shadow Council (criminal/fel)
- Twilight's Hammer (criminal/old gods)
- Cenarion Circle (open/druidism)
- Sisterhood of Elune (open/kaldorei)
- Hermetics (semi-secret)

**Extensions proposees** :

#### Cult of the Damned - Extension Scourge
| Rang | Pouvoir actuel | Pouvoir ajoute |
|------|---------------|----------------|
| 1 | Tainted Touch | Bonus +5% en raid Naxxramas |
| 2 | Raise Dead | Decision "Corrompre un courtisan" (change sa religion en Undead) |
| 3 | Abduction | Decision "Plague Cauldron" (devastation province cible) |
| 4 | Monstrous Undead | Decision "Phylactere" (1 resurrection apres la mort, 1 seule fois) |

#### Cenarion Circle - Extension Nature
| Rang | Pouvoir actuel | Pouvoir ajoute |
|------|---------------|----------------|
| 1 | Nature magic | Bonus +10% en raid Maraudon/Dire Maul |
| 2 | Healing | Decision "Purifier une province" (retire corruption/devastation) |
| 3 | - | Decision "Appel de la Foret" (+500 levies temporaires pendant 2 ans) |
| 4 | - | Decision "Treant Guardian" (artefact companion, +10 combat, +1 health) |

#### Nouvelles societes a ajouter (via le submod)
| Societe | Type | Theme | Classes privilegiees |
|---------|------|-------|---------------------|
| Kirin Tor | Semi-secret | Magie/Savoir | Mage, Warlock |
| Argent Crusade | Open | Lumiere/Justice | Paladin, Priest |
| Earthen Ring | Open | Elements/Nature | Shaman |
| Ravenholdt | Secret | Ombres/Vol | Rogue |

**Fichiers a creer** :
- `common/societies/hoa_societies.txt` - 4 nouvelles societes
- `events/hoa_society_events.txt` - missions et interactions
- `decisions/hoa_society_decisions.txt` - pouvoirs par rang

---

### 2.4 World Bosses Dynamiques

**Concept** : Toutes les 5-15 ans, un World Boss spawn sur une province aleatoire. Le comte perd ses levies et ses taxes. N'importe quel dirigeant adjacent peut tenter de le tuer. Le premier qui reussit gagne un titre permanent et un artefact unique.

**Pool de World Bosses** :

| Boss | Biome | Difficulte | Loot unique |
|------|-------|-----------|-------------|
| Dragon Enrage | Montagne | Moyenne | Ecaille Draconique (torso, +8 combat, +0.5 health) |
| Elementaire Dechaine | Desert/Volcanique | Moyenne | Coeur Elementaire (relic, +2 martial, +5 combat) |
| Abomination Geante | Marecage/Plaine | Facile | Os du Geant (weapon, +10 combat) |
| Demon Errant | Foret | Difficile | Lame Gangrenee (weapon, +15 combat, -0.2 health) |
| Hydre Ancienne | Cote/Jungle | Difficile | Ecaille d'Hydre (wrist, +6 combat, +0.3 health, regen) |
| Pit Lord | N'importe | Extreme | Armure de Pit Lord (torso, +20 combat, +1 martial, trait "feared") |

**Escalade** :
- Annee 0-2 : Boss niveau 1 (base)
- Annee 2-4 : Boss niveau 2 (se deplace vers province adjacente, stats x1.5)
- Annee 4+ : Boss niveau 3 (ravage un duche entier, stats x2, crise majeure)

**Implementation** :
- Province event MTTH = 10 ans, ajoute modifier `hoa_world_boss_present`
- Decision `hoa_fight_world_boss` accessible a tout dirigeant controlant une province adjacente
- Resolution similaire aux raids (random_list avec modificateurs martial, classe, equipement)

**Fichiers a creer** :
- `events/hoa_world_boss_events.txt`
- `decisions/hoa_world_boss_decisions.txt`
- `common/event_modifiers/hoa_world_boss_modifiers.txt`
- `common/artifacts/hoa_world_boss_loot.txt`

---

### 2.5 Arene PvP & Systeme de Classement

**Concept** : Systeme de duels competitifs avec saisons de 5 ans. Classement par combat rating. Recompenses saisonnieres.

**Mecaniques** :

| Composant | Detail |
|-----------|--------|
| Arena 1v1 | Decision `hoa_arena_challenge` : challenge n'importe quel dirigeant. Resolution par combat_rating + martial + equipement |
| Arena 3v3 | Decision `hoa_arena_team` : selectionne 2 champions de ta cour. Score = somme des combat_rating des 3 |
| Saisons | Tous les 5 ans (1825 jours), event global reset les classements |
| Betting | Les dirigeants non-participants peuvent parier (event chain) |
| Death match | Option "a mort" : le perdant meurt. +500 prestige au vainqueur |

**Recompenses saisonnieres** :

| Rang | Titre | Bonus |
|------|-------|-------|
| Champion (#1) | Gladiateur | +3 martial, +10 combat, +0.5 prestige/mois, monture unique |
| Top 3 | Rival | +2 martial, +5 combat |
| Top 10 | Challenger | +1 martial, +3 combat |

**Fichiers a creer** :
- `events/hoa_arena_events.txt`
- `decisions/hoa_arena_decisions.txt`
- `common/event_modifiers/hoa_arena_modifiers.txt`

---

### 2.6 Auction House (Marche aux Artefacts)

**Concept** : Systeme d'echange d'items entre personnages via events.

**Mecaniques** :

| Action | Implementation |
|--------|---------------|
| Mettre en vente | Decision `hoa_sell_artifact` : choisit un artefact non equipe, fixe un prix (100/200/500) |
| Achat IA | Event MTTH 6 mois : personnages IA evaluent les items en vente basee sur classe/stats |
| Encheres | Si 2+ acheteurs, le prix augmente de 50% par round |
| Marche noir | Membres de la Guilde des Ombres (Ravenholdt) vendent a -30% mais 20% chance de detection |
| Arnaque | Trait "deceitful" : peut vendre un faux (artefact Q4 visuellement, Q1 reellement, se revele apres 1 an) |

**Fichiers a creer** :
- `events/hoa_auction_events.txt`
- `decisions/hoa_auction_decisions.txt`

---

### 2.7 Champions / Compagnons de Cour

**Concept** : Nouveau slot de "Champion" - un courtisan special qui accompagne le dirigeant en raid, duel et guerre.

**Mecaniques** :

| Composant | Detail |
|-----------|--------|
| Recrutement | Decision `hoa_recruit_champion` (200 gold). Event propose 3 candidats aleatoires avec classe/race/stats |
| Loyaute | Score de loyaute base sur traitement (gift = +10, ignore = -5/an, artefact offert = +20) |
| Synergie | Champion mage + dirigeant warrior = +15% en raid (combo tank+DPS) |
| Trahison | Loyaute < 20 : 10%/an que le champion deserte vers un rival |
| Rivalite | 2 champions dans la cour : 20%/an qu'ils deviennent rivaux (duel potentiel) |
| Legendaire | 5% chance que le candidat soit "legendaire" (stats 18+, artefact unique) |

**Fichiers a creer** :
- `events/hoa_champion_events.txt`
- `decisions/hoa_champion_decisions.txt`
- `common/event_modifiers/hoa_champion_modifiers.txt`

---

### 2.8 Exploration Procedurale (Roguelike Dungeons)

**Concept** : Decision "Explorer l'Inconnu" genere un mini-donjon aleatoire avec 3 salles, chaque salle = un event avec choix.

**Tables de generation** :

| Pool | Options |
|------|---------|
| Biome | Caverne, Ruines, Foret maudite, Tour abandonnee, Crypte, Mine effondree |
| Modifier | Hante (+danger, +loot magic), Infeste (+mobs, +XP), Piege (+intrigue check), Maudit (+risque maladie, +artefact rare) |
| Boss | Pool de 20+ mini-boss generiques avec loot tables |
| Salle 1 | Combat (martial check), Puzzle (learning check), Piege (intrigue check), Negoce (diplomacy check) |
| Salle 2 | Idem avec difficulte +2 |
| Salle 3 | Boss fight OU tresor cache OU embuscade |

**Decouvertes speciales** :
- 5% chance de decouvrir un "Mega Dungeon" → ajoute une decision permanente dans la province
- Systeme de cartes : 5 fragments = localisation d'un tresor legendaire

**Implementation** :
- Decision `hoa_explore_unknown` (100 gold, cooldown 180 jours)
- 3 events enchaines avec random_list pour chaque salle
- Hidden modifiers pour tracker les fragments de carte

**Fichiers a creer** :
- `events/hoa_exploration_events.txt`
- `decisions/hoa_exploration_decisions.txt`
- `common/event_modifiers/hoa_exploration_modifiers.txt`

---

### 2.9 Systeme de Corruption / Pouvoir Interdit

**Concept** : Compteur de corruption (0-100%) sur chaque personnage, alimentee par des choix tentants. Chaque palier donne un pouvoir plus grand mais avec des consequences croissantes.

**Sources de corruption** :

| Action | Corruption gagnee |
|--------|-------------------|
| Utiliser un artefact maudit | +5% par an |
| Rejoindre Shadow Council / Twilight's Hammer | +10% a l'entree |
| Sacrifier un prisonnier (decision) | +15% |
| Lire un grimoire interdit (decision) | +10% |
| Utiliser "Drain de Vie" (rang 40%) | +5% |
| "Forme Demon" (rang 80%) | +20% |

**Paliers de pouvoir** :

| Seuil | Pouvoir debloque | Consequence |
|-------|-----------------|-------------|
| 20% | +2 intrigue, yeux changes (trait cosmetique) | Trait visible par tous |
| 40% | +2 martial, +5 combat, decision "Drain de Vie" | Pretres te refusent audience |
| 60% | +3 toutes stats, decision "Terreur" (0% revolte 2 ans) | -20 opinion clerge |
| 80% | Decision "Forme Demon" (+20 combat, +5 martial, 1 an) | -40 opinion tous |
| 100% | Transformation permanente. Stats de dingue | TOUS vassaux -100 opinion. Heritier declare la guerre. Croisade contre toi |

**Purification** :
- Decision `hoa_purify_corruption` : event chain difficile (3 stages, learning/piety checks)
- Succes : corruption tombe a 0%, perd tous les bonus
- Echec : corruption augmente de 10%, perd 1 health

**Heredite** :
- Enfants d'un parent corruption 60%+ : 30% chance du trait `hoa_tainted_blood`
- Tainted blood : +1 intrigue, corruption gagne 2x plus vite

**Fichiers a creer** :
- `common/traits/hoa_corruption_traits.txt`
- `events/hoa_corruption_events.txt`
- `decisions/hoa_corruption_decisions.txt`
- `common/event_modifiers/hoa_corruption_modifiers.txt`

---

### 2.10 Bloodlines Dynamiques

**Concept** : Les exploits du joueur creent des lignees hereditaires permanentes. Chaque personnage ne peut creer qu'une seule bloodline.

**Bloodlines disponibles** :

| Bloodline | Condition de creation | Bonus hereditaire permanent |
|-----------|----------------------|---------------------------|
| Tueur de Dieux | Tuer C'Thun + Kel'Thuzad (meme personnage) | +2 martial, +5 combat, +0.1 prestige/mois |
| Gladiateur Eternel | Gagner 3 saisons d'arene consecutives | +3 combat, casus belli "Duel de Champion" |
| Marchand-Prince | Accumuler 5000 gold + 3 trade posts | +10% tax globale, heritier commence avec +200 gold |
| Corrompu Repenti | Atteindre 80% corruption puis se purifier | Immunite Tainted Blood, +2 learning |
| Maitre Forgeron | Crafter 10 artefacts Epic+ | Items craftes commencent Rare minimum |
| Explorateur Legendaire | Decouvrir 3 Mega Dungeons | Explorations -50% cout, +1 fragment carte/run |
| Grand Maitre | Atteindre Rang 4 dans une societe | Descendants commencent Rang 2 |
| Dracotue | Tuer 3 World Bosses dragons | +3 martial, immunite debuff "Peur draconique" |
| Unificateur | Former 3 pactes defensifs consecutifs | +5 diplomatie opinion, -50% cout actions diplo |
| Champion Ultime | Atteindre combat_rating 80+ | +5 combat, +1 martial, duels automatiquement gagnes vs CR < 50 |

**Implementation CK2** :
- Utilise le systeme de bloodlines de Holy Fury DLC
- `common/bloodlines/hoa_dynamic_bloodlines.txt`
- Events trackers via hidden modifiers (compteurs)
- `on_actions` pour detecter les conditions

**Fichiers a creer** :
- `common/bloodlines/hoa_dynamic_bloodlines.txt`
- `events/hoa_bloodline_events.txt`

---

## PARTIE 3 : 10 RECOMMANDATIONS GEOPOLITIQUES

Ces recommandations ajoutent de la profondeur politique a chaque position de conseil, creent des factions internes, et font de la classe du dirigeant un facteur politique majeur.

### 3.1 Le Chancelier comme Moteur Diplomatique

**Decisions ajoutees** :

#### Decision : Envoyer le Chancelier negocier un traite
```
hoa_chancellor_negotiate = {
    potential = { job_chancellor = { always = yes } }
    allow = {
        job_chancellor = { diplomacy >= 12 }
        wealth >= 100
        war = no
    }
    effect = {
        # Le chancelier part 90 jours
        # Resultat base sur SON diplomacy, pas celui du dirigeant
        # diplo 15+ : traite commercial (+15% tax bilateral, 10 ans)
        # diplo 20+ : pacte de non-agression incassable
        # diplo 25+ : mariage arrange automatique
    }
}
```

#### Decision : Organiser un Sommet via le Chancelier
- Le chancelier invite 3 dirigeants voisins
- Son diplomacy determine qui accepte (seuil 12/15/18 par invite)
- Chaque present donne +10 opinion
- Si chancelier est humain (bonus racial diplo) : peut obtenir un accord secret

#### Event chain : Le Chancelier a ete capture
- 10% chance si chancelier en mission dans royaume hostile
- Options : payer rancon (200 gold), envoyer marechal (event militaire), abandonner (-30 opinion courtisans)

#### Passive : Reseau diplomatique
- Chancelier diplo 14+ : modifier `hoa_diplomatic_network` (+5% succes actions diplo)
- Chancelier diplo 20+ : alerte sur alliances en formation ("X negocie avec Y")

**Fichiers** : `decisions/hoa_chancellor_decisions.txt`, `events/hoa_chancellor_events.txt`

---

### 3.2 L'Intendant comme Gouverneur Economique Actif

**Decisions ajoutees** :

#### Decision : Audit du Royaume
- L'intendant inspecte les provinces (180 jours)
- Stew 12+ : decouvre province sous-developpee → -20% cout batiment recommande
- Stew 16+ : decouvre vassal qui vole des impots → event chain (confronter vs laisser faire)
- Stew 20+ : opportunite commerciale → +25% tax province pendant 5 ans

#### Decision : Lever un impot special
- Montant = stewardship de l'intendant x 10 gold
- Chaque vassal perd -15 opinion (reduit a -8 si intendant a trait "just")
- Si intendant "greedy" : prend 20% pour lui

#### Passive : Gestion du tresor
- Intendant stew 16+ : modifier `hoa_efficient_treasury` (+5% global tax)
- Se perd si intendant change et le nouveau a stew < 16

#### Event : L'intendant propose un investissement
- MTTH 5 ans si intendant stew 14+
- Investir 200-500 gold, retour 150-300% en 5 ans (basee sur stew)
- Si intendant "deceitful" : 25% chance qu'il detourne les fonds

**Fichiers** : `decisions/hoa_steward_decisions.txt`, `events/hoa_steward_events.txt`

---

### 3.3 Le Maitre-Espion comme Arme Geopolitique

**Decisions ajoutees** :

#### Decision : Infiltrer une cour etrangere
- Maitre-espion absent 180 jours
- Resolution : son intrigue vs intrigue du maitre-espion adverse
- Victoire nette (+5) : rapport complet (stats courtisans, complots, tresors)
- Victoire faible (+1-4) : decouvre 1 secret
- Echec : rien
- Echec critique (-5) : capture, CB espionnage contre toi, -50 opinion

#### Decision : Saboter l'economie
- Cout 100 gold, cible une province ennemie
- Resultat : -30% tax, -20% levy pendant 2 ans sur la province
- Si detecte : casus belli adverse

#### Decision : Destabiliser un vassal
- Cible un vassal d'un dirigeant ennemi
- Intrigue 16+ : le vassal rejoint une faction contre son liege
- Intrigue 20+ : le vassal peut changer de camp vers toi (si adjacent)

#### Passive : Reseau d'ombres
- Intrigue 16+ : alertes quand un complot te vise
- Intrigue 20+ : identite du leader du complot revelee
- Intrigue 25+ : peut retourner le complot (event chain contre-attaque)

#### Event chain : Guerre de l'ombre
- Si deux maitres-espions s'infiltrent mutuellement
- 5 rounds, chaque round le meilleur gagne un avantage
- Perdant final assassine ou retourne comme agent double

**Fichiers** : `decisions/hoa_spymaster_decisions.txt`, `events/hoa_spymaster_events.txt`

---

### 3.4 Le Marechal comme Chef de Guerre Strategique

**Decisions ajoutees** :

#### Decision : Planifier une campagne militaire
- Marechal planifie 90 jours
- Martial 14+ : +10% morale troupes prochaine guerre
- Martial 18+ : +10% morale ET -20% attrition
- Martial 22+ : + avantage tactique premiere bataille
- Expire apres premiere guerre ou 2 ans

#### Decision : Fortifier la frontiere
- Marechal choisit un duche frontalier
- Toutes provinces du duche : +1 fort level pendant 5 ans
- Cout reduit de 30% si marechal a trait "architect"

#### Bonus raids : Le marechal influence les dungeons
- Martial du marechal / 5 = bonus % chance de succes en raid
- Marechal martial 20 = +4% par stage de dungeon

#### Event : Le marechal propose un assaut decisif
- Si en guerre depuis >1 an, marechal martial 15+
- Accepter : bataille forcee dans 30 jours
- Victoire : war score +50% d'un coup
- Defaite : war score -30%

#### Passive : Doctrine militaire (se developpe apres 3 ans en poste)
| Classe du marechal | Doctrine | Bonus |
|-------------------|----------|-------|
| Warrior | Charge | +15% heavy infantry |
| Hunter | Embuscade | +15% archers, -10% attrition |
| Mage | Arcanique | +10% toutes unites, siege magique |
| Death Knight | Terreur | +20% morale, -10 opinion provinces conquises |
| Paladin | Lumiere | +10% morale, +10% disease defense |
| Rogue | Guerilla | +20% light infantry, +15% dans les forets |
| Shaman | Elementaire | +10% toutes unites, bonus terrain montagne |

**Fichiers** : `decisions/hoa_marshal_decisions.txt`, `events/hoa_marshal_events.txt`

---

### 3.5 Les Commandants comme Heros de Guerre Nommes

**Mecaniques ajoutees** :

#### Trait "Heros de Guerre"
- 3 batailles victorieuses consecutives → trait permanent `hoa_war_hero`
- +2 martial, +5 combat, +10 vassal opinion
- Tracked via hidden modifier incrementant a chaque victoire

#### Decision : Promouvoir un commandant en champion
- Le commandant recoit un artefact mineur + titre honorifique
- S'il meurt en bataille : -50 prestige, -15% morale troupes pendant 1 an

#### Synergie raciale commandant + retinue
- Meme race = +10% toutes stats de l'unite
- Implementation via `commander_modifier` conditionnel

#### Event : Rivalite entre commandants
- 2+ commandants martial 15+ : 30%/an rivalite
- Choix : soutenir l'un, l'autre, ou medier
- Le non-soutenu peut deserter (amenant ses troupes)

#### Decision : Raid eclair
- Commandant martial 12+ envoye en raid solo sur province adjacente ennemie
- Resultat : pillage gold + chance capture prisonniers
- Risque : commandant tue ou capture

**Fichiers** : `events/hoa_commander_events.txt`, `decisions/hoa_commander_decisions.txt`

---

### 3.6 Factions Internes avec Dents

**4 factions specifiques au mod** :

#### Parti de la Guerre
- **Membres** : Vassaux martial 12+
- **Demande** : Guerre contre un voisin specifique
- **Si ignore 3 ans** : -30 opinion, revolte possible
- **Si satisfait** : +25% levy bonus pendant la guerre
- **Interaction marechal** : s'il est dans la faction, peut la renforcer ou calmer

#### Guilde des Marchands
- **Membres** : Vassaux stewardship 12+
- **Demande** : Loi de commerce libre
- **Si adoptee** : +15% global tax, -10% levy
- **Si refusee** : Embargo (-20% tax pendant 2 ans)

#### Cercle des Mages
- **Membres** : Courtisans avec classe magique
- **Demande** : Autonomie magique
- **Si satisfait** : +20% tech growth, decision "Barriere Magique" (+2 fort level capitale)
- **Si mecontent** : Sabotage magique (events negatifs aleatoires)

#### Vieux Sang
- **Membres** : Vassaux de la meme race que le dirigeant
- **Demande** : Purete raciale (pas de conseillers d'autres races)
- **Si satisfait** : +20 opinion mais provinces autres races -10% tax
- **Si refuse** : -15 opinion par conseiller etranger

#### Mecanique de tipping point
- Faction a 80% military power → ultimatum
- 30 jours pour ceder ou combattre
- Option secrete : envoyer maitre-espion assassiner le leader

**Fichiers** : `common/factions/hoa_factions.txt`, `events/hoa_faction_events.txt`

---

### 3.7 Gouvernements Warcraft Uniques

**4 nouveaux types de gouvernement** :

#### Magocratie (Dalaran, Silvermoon)
- Dirigeant DOIT etre classe magique
- Conseil = Conclave des Mages (5 Archimages)
- Succession par election des mages
- Decision unique "Experience Arcanique" : 50% breakthrough tech, 20% explosion

#### Conseil de Guerre de la Horde (Orgrimmar, clans orcs)
- Warchef elu par les chefs de clan
- Marechal a pouvoir legislatif (loi de guerre : +30% levy, -20% tax)
- Decision unique "Mak'gora" : vassal peut defier le Warchef en duel pour le titre

#### Theocratie Naturelle (Darnassus, druides)
- Piete remplace prestige pour les victoires
- Succession favorise le plus pieux
- Decision unique "Communion avec la Nature" : transe (incapable 30j), puis vision prophetique

#### Republique Marchande Gobeline (Undermine, cartels)
- Or remplace prestige pour TOUT
- Elections aux encheres (le plus riche gagne)
- Decision unique "Hostile Takeover" : absorber un comte voisin sans guerre (cout massif en gold)

**Fichiers** : `common/governments/hoa_governments.txt`, `events/hoa_government_events.txt`

---

### 3.8 Systeme de Cour Vivante

**Mecaniques ajoutees** :

#### Event chain "Intrigues de Cour"
- MTTH 3 ans
- 2 courtisans forment une rivalite basee sur traits opposes
- Event : "Votre marechal accuse votre intendant de corruption"
- Options : soutenir A, soutenir B, enqueter (100 gold, 50% verite)

#### Decision : Tenir audience
- 1x par an. 3 courtisans presentent des requetes (random)
- Exemples :
  - Vassal demande un titre → donner (+20 opinion lui, -10 autres) ou refuser (-15)
  - Marchand propose investissement → accepter (event chain eco) ou refuser
  - Espion rapporte complot → agir (event intrigue) ou ignorer

#### Passive : Prestige de la Cour
- 3+ courtisans stats 15+ : +0.2 prestige/mois
- 5+ courtisans stats 15+ : +0.4 prestige/mois, +5 vassal opinion
- Courtisans brillants sont aussi ambitieux (plus susceptibles de comploter)

**Fichiers** : `events/hoa_court_events.txt`, `decisions/hoa_court_decisions.txt`

---

### 3.9 Diplomatie de Classe

**1 decision diplomatique unique par classe** :

| Classe | Decision | Effet |
|--------|----------|-------|
| Warrior | Ultimatum Martial | Force traite si martial > cible. Echec = CB adverse |
| Rogue | Reseau de Contrebande | +2 gold/mois par province frontiere en paix. -10 opinion si decouvert |
| Mage | Portail Diplomatique | -50% cooldown toutes actions diplo |
| Paladin | Jugement de la Lumiere | Accuse publiquement un dirigeant tyrannique. Si vrai : -20 opinion vassaux adverses |
| Priest | Excommunication | Demande excommunication basee sur piete comparative |
| Warlock | Pacte Sombre | Alliance incassable, -1 piety/mois pour les deux. Si l'un meurt : -2 toutes stats |
| Druid | Prediction Naturelle | Predit resultat de guerre (70% precision). Si correct : +50 prestige |
| Hunter | Pistage de Fugitif | +50% capture rate sur personnages en fuite |
| Shaman | Appel aux Elements | Bonus terrain en guerre (montagne, plaine, cote selon element invoque) |
| Death Knight | Terreur Glaciale | -20 opinion de toutes troupes ennemies dans la province (morale effondree) |
| Monk | Meditation de Paix | +30 opinion avec un ennemi pour 5 ans (force la paix sans traite) |

**Fichiers** : `decisions/hoa_class_diplomacy_decisions.txt`, `events/hoa_class_diplomacy_events.txt`

---

### 3.10 Systeme de Reputation Internationale

**4 axes de reputation avec paliers et consequences** :

#### Axe "Conquerant"
| Palier | Seuil | Bonus | Malus |
|--------|-------|-------|-------|
| 1 | 3 guerres offensives gagnees | +5 vassal martial opinion | -5 opinion voisins |
| 2 | 5 guerres | +10% morale troupes | -15 opinion voisins |
| 3 | 8 guerres | titre "Fleau d'Azeroth" | Coalition automatique des voisins |

#### Axe "Diplomate"
| Palier | Seuil | Bonus |
|--------|-------|-------|
| 1 | 3 traites signes | -20% cout prestige actions diplo |
| 2 | 5 traites | Decision "Mediation" (resoudre une guerre entre 2 tiers) |
| 3 | 8 traites | titre "Artisan de Paix", former une Ligue de Paix |

#### Axe "Ombre"
| Palier | Seuil | Bonus |
|--------|-------|-------|
| 1 | 3 actions espionnage reussies | +20% plot power |
| 2 | 5 actions | Tribute automatique de voisins effrayes (10 gold/an) |
| 3 | 8 actions | titre "Maitre des Murmures", personne ne declare la guerre sans -20 prestige |

#### Axe "Sage"
| Palier | Seuil | Bonus |
|--------|-------|-------|
| 1 | 3 mentorats/etudes | +10% tech growth |
| 2 | 5 | Courtisans brillants viennent spontanement |
| 3 | 8 | titre "Lumiere du Savoir", fonder une universite (batiment permanent) |

**Implementation** : Hidden modifiers compteurs incrementes par les actions correspondantes. Events fires quand les seuils sont atteints.

**Fichiers** : `events/hoa_reputation_events.txt`, `common/event_modifiers/hoa_reputation_modifiers.txt`

---

## PARTIE 4 : ECOSYSTEME DES INTERACTIONS

Chaque systeme nourrit les autres. Voici la matrice d'interaction :

```
                    Specs   Items   Societes  WBoss  Arena  AH    Champions  Explore  Corrupt  Blood
Specs de classe      -       buff    bonus     +dmg   +CR    -     synergie   +check   +risk    -
Items evolutifs     equip    -       craft     loot   reward sell  equip      loot     corrupt  track
Societes            gate     craft   -         intel  -      noir  recruit    intel    source   R4=BL
World Bosses        +class   loot    intel     -      -      sell  +dmg       map      -        track
Arena PvP           +spec    +CR     -         -      -      bet   team       -        -        track
Auction House       -        trade   noir      sell   bet    -     equip      sell     -        -
Champions           class    equip   recruit   fight  team   buy   -          -        risk     -
Exploration         check    loot    intel     map    -      sell  -          -        grimoire track
Corruption          risk     curse   source    -      -      -     risk       grimoire -        track
Bloodlines          -        craft   R4=BL     track  track  -     -          track    track    -
```

**Boucle de jeu emergente** :
1. Choisis ta spec → Definit ton style de jeu
2. Explore / Raid → Obtiens des items et fragments de carte
3. Les items evoluent avec tes victoires
4. Vends les items inutiles a l'Auction House
5. Rejoins une societe → Debloque des pouvoirs caches
6. Recrute un champion → Synergie de classe
7. Affronte les World Bosses → Loot unique
8. Domine l'Arene → Titre Gladiateur
9. Gere la corruption → Pouvoir vs risque
10. Tes exploits creent une Bloodline → Metagame dynastique

---

## PARTIE 5 : FEUILLE DE ROUTE

### Phase 1 : Fondations (Priorite haute)
1. Systeme de conseil actif (Chancelier, Intendant, Maitre-espion, Marechal)
2. Diplomatie de classe (11 decisions uniques)
3. Factions internes (4 factions)
4. Commandants comme heros de guerre

### Phase 2 : Sandbox Core (Priorite haute)
5. Specialisations de classe
6. Artefacts evolutifs + gemmes
7. Systeme de corruption
8. Extension des societes existantes

### Phase 3 : Systemes Emergeants (Priorite moyenne)
9. World Bosses dynamiques
10. Arena PvP + classement
11. Champions / Compagnons
12. Exploration procedurale

### Phase 4 : Meta-systemes (Priorite moyenne)
13. Auction House
14. Bloodlines dynamiques
15. Gouvernements Warcraft uniques
16. Reputation internationale

### Phase 5 : Polish (Priorite basse)
17. Cour vivante (intrigues, audiences)
18. Localisation complete (FR/DE/ES)
19. Equilibrage global
20. Compatibilite avec les societes de base GoA

---

## PARTIE 6 : ESTIMATION TECHNIQUE

| Systeme | Fichiers estimes | Lignes estimees | Complexite |
|---------|-----------------|-----------------|-----------|
| Conseil actif | 8 fichiers | ~2000 lignes | Moyenne |
| Diplomatie de classe | 2 fichiers | ~800 lignes | Faible |
| Factions internes | 2 fichiers | ~600 lignes | Moyenne |
| Commandants | 2 fichiers | ~500 lignes | Faible |
| Specs de classe | 4 fichiers | ~1500 lignes | Moyenne |
| Items evolutifs | 4 fichiers | ~1200 lignes | Haute |
| Corruption | 4 fichiers | ~800 lignes | Moyenne |
| Societes extension | 3 fichiers | ~1000 lignes | Moyenne |
| World Bosses | 4 fichiers | ~1500 lignes | Haute |
| Arena PvP | 3 fichiers | ~800 lignes | Moyenne |
| Champions | 3 fichiers | ~1000 lignes | Moyenne |
| Exploration | 3 fichiers | ~1200 lignes | Haute |
| Auction House | 2 fichiers | ~600 lignes | Faible |
| Bloodlines | 2 fichiers | ~500 lignes | Moyenne |
| Gouvernements | 2 fichiers | ~400 lignes | Moyenne |
| Reputation | 2 fichiers | ~600 lignes | Faible |
| Cour vivante | 2 fichiers | ~800 lignes | Moyenne |
| **TOTAL** | **~52 fichiers** | **~15,800 lignes** | |

Le contenu actuel des deux submods totalise ~5,700 lignes. Ce plan ajouterait ~15,800 lignes, soit presque 3x le contenu existant. La priorite est de commencer par la Phase 1 (fondations politiques) car c'est le layer manquant le plus critique.
