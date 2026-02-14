# RAPPORT UI/UX - Organisation de l'Interface des Submods GoA

**Date :** 14 fevrier 2026
**Sujet :** Audit complet de l'interface, diagnostic du probleme de decisions, et plan de refonte

---

## 1. DIAGNOSTIC : L'ETAT ACTUEL

### 1.1 Le probleme

**102 decisions** sont actuellement empilees dans l'onglet Intrigue de CK2.
Un joueur qui ouvre sa liste de decisions voit un mur de texte :

```
[ ] Forge Equipment (Uncommon)
[ ] Forge Equipment (Rare)
[ ] Forge Masterwork Weapon
[ ] Enchant Weapon
[ ] Disenchant Artifact
[ ] Enter Shadowfang Keep
[ ] Enter Scarlet Monastery
[ ] Enter Gnomeregan
[ ] Enter Maraudon
[ ] Enter Dire Maul
[ ] Enter Stratholme
[ ] Enter Scholomance
[ ] Enter Upper Blackrock Spire
[ ] Enter Zul'Gurub
[ ] Enter Molten Core
[ ] Enter Blackwing Lair
[ ] Enter Ahn'Qiraj
[ ] Enter Naxxramas
[ ] Challenge to Single Combat
[ ] Form Defensive Pact
[ ] Send Emissary
[ ] Walk the Streets
[ ] Visit the Tavern
[ ] Host a Grand Feast
[ ] Diplomatic Tour
[ ] Commission Monument
... (77 decisions de plus)
```

C'est **injouable**. Meme avec les `potential` qui filtrent certaines decisions, un personnage qui a acces a tout peut voir 60+ decisions d'un coup.

### 1.2 Repartition actuelle par type de bloc

| Type de bloc | Nombre | Emplacement UI |
|---|---|---|
| `decisions = { }` | ~85 | Onglet Intrigue (decisions panel) |
| `targetted_decisions = { }` | ~17 | Clic-droit sur personnage |
| `settlement_decisions = { }` | 0 | Clic-droit sur holding |
| `title_decisions = { }` | 0 | Clic-droit sur titre |

**Probleme principal :** 85 decisions dans un seul panneau scroll.

### 1.3 Inventaire par categorie

| Categorie | Nb decisions | Fichier source |
|---|---|---|
| Crafting | 5 | hoa_crafting_decisions.txt |
| Dungeons/Raids | 13 | hoa_dungeon_decisions.txt |
| Diplomatie basique | 3 | hoa_diplomacy_decisions.txt |
| Diplomatie de classe | 11 | hoa_class_diplomacy_decisions.txt |
| Conseil (Chancellor) | 3 | hoa_chancellor_decisions.txt |
| Conseil (Steward) | 3 | hoa_steward_decisions.txt |
| Conseil (Spymaster) | 3 | hoa_spymaster_decisions.txt |
| Conseil (Marshal) | 3 | hoa_marshal_decisions.txt |
| Pouvoir/Flavour | 14 | hoa_power_decisions.txt |
| Personnel | 8 | hoa_personal_decisions.txt |
| Combat/Bataille | 5 | hoa_battle_decisions.txt |
| Commerce | 5 | hoa_trade_decisions.txt |
| Societe secrete | 5 | hoa_society_decisions.txt |
| Factions | 4 | hoa_faction_decisions.txt |
| Economie (IE) | 4 | ie_economy_decisions.txt |
| **Targeted:** Schemes | 10 | hoa_scheme_decisions.txt |
| **Targeted:** Gifts | 5 | hoa_gift_decisions.txt |
| **Targeted:** Advisors | 6 | hoa_advisor_decisions.txt |
| **Targeted:** Faction ultimatum | 1 | hoa_faction_decisions.txt |

---

## 2. CE QUE FONT LES GROS MODS CK2

### 2.1 La technique standard : "Master Decision → Event Menu"

**Tous** les gros mods CK2 (AGOT, Elder Kings, CK2Plus) utilisent la meme approche :

1. **UNE seule decision** dans l'onglet Intrigue ("Ouvrir le menu Heroes of Azeroth")
2. Cette decision ouvre un **character_event** qui sert de **menu principal**
3. Chaque option du menu ouvre un **sous-menu** (autre event)
4. Les sous-menus contiennent les actions reelles
5. Un bouton "Retour" ramene au menu principal

```
[Onglet Intrigue]
    |
    +-- "Heroes of Azeroth" (1 seule decision visible)
            |
            +-- [Event Menu Principal]
                |-- "Donjons & Raids"        --> Sous-menu donjons
                |-- "Forge & Artisanat"      --> Sous-menu crafting
                |-- "Commerce & Economie"    --> Sous-menu trade
                |-- "Actions personnelles"   --> Sous-menu perso
                |-- "Fermer"
```

**Avantages :**
- Zero conflit de fichiers GUI
- Compatible avec tous les autres mods
- Remplace 85 decisions par 1 seule
- Menus dynamiques (options masquees via `trigger`)
- Pagination possible ("Page suivante...")

### 2.2 Exemple concret : AGOT

Le mod A Game of Thrones utilise exactement ce pattern pour :
- Le menu R'hllor (religion)
- Le menu de gestion d'esclaves
- Le menu "More Decisions" (submod communautaire)

### 2.3 Les `targetted_decisions` restent en clic-droit

Les decisions ciblees sur un personnage (schemes, gifts, advisor consult) sont **deja bien placees** en clic-droit. On ne les touche pas.

---

## 3. PLAN DE REFONTE PROPOSE

### 3.1 Architecture cible

```
ONGLET INTRIGUE (decisions panel)
    |
    +-- "Heroes of Azeroth"     (1 decision - menu HoA)
    +-- "Economie de Royaume"   (1 decision - menu IE)
    |
    (Total : 2 decisions au lieu de 85)


CLIC-DROIT SUR PERSONNAGE (inchange)
    |
    +-- Schemes (10 targeted decisions)
    +-- Gifts (5 targeted decisions)
    +-- Advisor Consult (6 targeted decisions)
    +-- Faction Ultimatum (1 targeted decision)


CLIC-DROIT SUR HOLDING (nouveau)
    |
    +-- settlement_decisions pour batiments speciaux IE
```

### 3.2 Structure detaillee du menu "Heroes of Azeroth"

```
==============================================
 HEROES OF AZEROTH - Menu Principal
==============================================
    |
    |-- [1] DONJONS & RAIDS
    |       |
    |       |-- Page 1 : Donjons (5-man)
    |       |   |-- Shadowfang Keep      (si controle province)
    |       |   |-- Scarlet Monastery    (si controle province)
    |       |   |-- Gnomeregan           (si controle province)
    |       |   |-- Maraudon             (si controle province)
    |       |   |-- Dire Maul            (si controle province)
    |       |   +-- "Donjons avances..." (page 2)
    |       |   +-- "Retour"
    |       |
    |       |-- Page 2 : Donjons avances (10-man)
    |       |   |-- Stratholme
    |       |   |-- Scholomance
    |       |   |-- Upper Blackrock Spire
    |       |   +-- "Raids..." (page 3)
    |       |   +-- "Retour"
    |       |
    |       +-- Page 3 : Raids (20/40-man)
    |           |-- Zul'Gurub (20)
    |           |-- Molten Core (40)
    |           |-- Blackwing Lair (40)    (si MC complete)
    |           |-- Ahn'Qiraj (40)         (si BWL complete)
    |           |-- Naxxramas (40)         (si AQ complete)
    |           +-- "Retour"
    |
    |-- [2] FORGE & ARTISANAT
    |       |-- Forger equipement (Uncommon)
    |       |-- Forger equipement (Rare)
    |       |-- Forger chef-d'oeuvre (Epic)
    |       |-- Enchanter une arme
    |       |-- Desenchanter un artefact
    |       +-- "Retour"
    |
    |-- [3] POUVOIR DE CLASSE
    |       |-- (Affiche seulement la capacite de la classe du perso)
    |       |-- Warrior: Ultimatum de guerre
    |       |-- Mage: Portail arcanique
    |       |-- Paladin: Jugement divin
    |       |-- Rogue: Reseau de contrebande
    |       |-- etc. (1 option visible par classe)
    |       +-- "Retour"
    |
    |-- [4] COMMERCE & ROUTES
    |       |-- Etablir route commerciale
    |       |-- Envoyer caravane
    |       |-- Organiser foire commerciale
    |       |-- Engager escorte mercenaire
    |       |-- Embargo commercial
    |       +-- "Retour"
    |
    |-- [5] CONSEIL & MISSIONS
    |       |-- Missions du Chancelier (sous-menu)
    |       |-- Missions du Senechal (sous-menu)
    |       |-- Missions du Maitre-espion (sous-menu)
    |       |-- Missions du Marechal (sous-menu)
    |       +-- "Retour"
    |
    |-- [6] ACTIONS PERSONNELLES
    |       |
    |       |-- Page 1 : Vie quotidienne
    |       |   |-- Marcher dans les rues
    |       |   |-- Visiter la taverne
    |       |   |-- Mediter / Prier
    |       |   |-- Tenir cour privee
    |       |   |-- Patrouille nocturne
    |       |   +-- "Plus d'actions..." (page 2)
    |       |   +-- "Retour"
    |       |
    |       +-- Page 2 : Actions majeures
    |           |-- Organiser grand festin
    |           |-- Tournoi d'arene
    |           |-- Ecrire ses memoires
    |           |-- Chercher guerison
    |           |-- Explorer les terres sauvages
    |           |-- S'entrainer avec les champions
    |           |-- Etudier les textes anciens
    |           |-- Visiter la bibliotheque
    |           +-- "Retour"
    |
    |-- [7] GUERRE & BATAILLE (visible seulement en guerre)
    |       |-- Mener la charge
    |       |-- Fortifier position
    |       |-- Inspirer les troupes
    |       |-- Defier le commandant ennemi
    |       |-- Capacite de combat de classe
    |       +-- "Retour"
    |
    |-- [8] SOCIETE SECRETE
    |       |-- Fonder une societe
    |       |-- Recruter un membre
    |       |-- Operation clandestine
    |       |-- Dissoudre la societe
    |       +-- "Retour"
    |
    |-- [9] GESTION DES FACTIONS
    |       |-- Apaiser les vassaux
    |       |-- Espionner les factions
    |       |-- Rallier les loyalistes
    |       +-- "Retour"
    |
    |-- [10] INVESTISSEMENTS
    |       |-- Etablir compagnie commerciale
    |       |-- Entreprise magique
    |       |-- Investir dans les infrastructures
    |       |-- Patronner les arts
    |       |-- Engager un garde du corps
    |       |-- Commander un monument
    |       |-- Tour diplomatique
    |       +-- "Retour"
    |
    +-- "Fermer"
```

### 3.3 Structure du menu "Economie de Royaume" (Improved Economy)

```
==============================================
 ECONOMIE DE ROYAUME - Menu IE
==============================================
    |
    |-- Etablir accord commercial
    |-- Commander grande construction
    |-- Developper les mines
    |-- Engager conseiller gobelin
    +-- "Fermer"
```

(4 decisions seulement, un menu simple suffit)

---

## 4. DETAILS TECHNIQUES D'IMPLEMENTATION

### 4.1 Fichiers a creer

| Fichier | Contenu |
|---|---|
| `decisions/hoa_master_menu.txt` | 1 decision gateway "Heroes of Azeroth" |
| `decisions/ie_master_menu.txt` | 1 decision gateway "Economie de Royaume" |
| `events/hoa_menu_events.txt` | Tous les events de navigation (menus/sous-menus) |
| `events/ie_menu_events.txt` | Menu events IE |
| `localisation/hoa_menu.csv` | Texte des menus FR/EN/DE/ES |
| `localisation/ie_menu.csv` | Texte des menus IE |

### 4.2 Fichiers a modifier

| Fichier | Modification |
|---|---|
| Tous les 14 fichiers `decisions/hoa_*.txt` | Retirer les `decisions = { }` (garder les `targetted_decisions`) |
| `decisions/ie_economy_decisions.txt` | Retirer les `decisions = { }` |

**Important :** Les `targetted_decisions` (schemes, gifts, advisors, faction ultimatum) restent dans leurs fichiers actuels. On ne touche PAS au clic-droit.

### 4.3 Pattern de code pour le menu principal

```pdx
# decisions/hoa_master_menu.txt
decisions = {
    hoa_master_menu = {
        only_playable = yes

        potential = {
            ai = no
            is_ruler = yes
            has_any_class_trigger = yes
        }

        allow = {
            is_adult = yes
            prisoner = no
            NOT = { trait = incapable }
        }

        effect = {
            character_event = { id = hoa_menu.1 }
        }

        ai_will_do = { factor = 0 }
    }
}
```

### 4.4 Pattern de code pour un sous-menu avec filtrage dynamique

```pdx
# events/hoa_menu_events.txt
namespace = hoa_menu

# Menu principal
character_event = {
    id = hoa_menu.1
    is_triggered_only = yes
    title = "HOA_MENU_TITLE"
    desc = "HOA_MENU_DESC"
    picture = GFX_evt_throne_room

    # Donjons - visible seulement si le joueur a acces a un donjon
    option = {
        name = "HOA_MENU_DUNGEONS"
        trigger = { has_any_class_trigger = yes }
        character_event = { id = hoa_menu.10 }
    }

    # Forge - visible seulement si martial > 0 ou classe appropriee
    option = {
        name = "HOA_MENU_CRAFTING"
        character_event = { id = hoa_menu.20 }
    }

    # Pouvoir de classe
    option = {
        name = "HOA_MENU_CLASS_POWER"
        trigger = { has_any_class_trigger = yes }
        character_event = { id = hoa_menu.30 }
    }

    # Commerce
    option = {
        name = "HOA_MENU_TRADE"
        character_event = { id = hoa_menu.40 }
    }

    # Conseil
    option = {
        name = "HOA_MENU_COUNCIL"
        character_event = { id = hoa_menu.50 }
    }

    # Actions perso
    option = {
        name = "HOA_MENU_PERSONAL"
        character_event = { id = hoa_menu.60 }
    }

    # Guerre (seulement visible en guerre)
    option = {
        name = "HOA_MENU_BATTLE"
        trigger = { war = yes }
        character_event = { id = hoa_menu.70 }
    }

    # Societe secrete
    option = {
        name = "HOA_MENU_SOCIETY"
        character_event = { id = hoa_menu.80 }
    }

    # Gestion factions
    option = {
        name = "HOA_MENU_FACTIONS"
        trigger = {
            is_ruler = yes
            any_vassal = { always = yes }
        }
        character_event = { id = hoa_menu.90 }
    }

    # Investissements
    option = {
        name = "HOA_MENU_INVESTMENTS"
        character_event = { id = hoa_menu.100 }
    }

    # Fermer
    option = {
        name = "HOA_MENU_CLOSE"
    }
}
```

### 4.5 Gestion de l'IA

**Probleme :** Si on retire les decisions individuelles, l'IA ne peut plus les utiliser.

**Solution :** Garder les anciennes decisions dans les fichiers mais les rendre **invisibles au joueur** :

```pdx
hoa_forge_weapon_uncommon = {
    potential = {
        ai = yes          # SEULEMENT visible par l'IA
        has_any_class_trigger = yes
        # ... autres conditions
    }
    # ... le reste identique
    ai_will_do = {
        factor = 1
        # ... poids IA
    }
}
```

Le joueur ne voit que le menu, l'IA continue d'utiliser les decisions individuelles avec ses poids `ai_will_do`. **Meilleur des deux mondes.**

### 4.6 Namespace des events de menu

| ID Range | Contenu |
|---|---|
| hoa_menu.1 | Menu principal |
| hoa_menu.10-19 | Sous-menus Donjons (pages 1-3) |
| hoa_menu.20-29 | Sous-menus Crafting |
| hoa_menu.30-39 | Sous-menus Pouvoir de classe |
| hoa_menu.40-49 | Sous-menus Commerce |
| hoa_menu.50-59 | Sous-menus Conseil |
| hoa_menu.60-69 | Sous-menus Actions perso (pages 1-2) |
| hoa_menu.70-79 | Sous-menus Guerre |
| hoa_menu.80-89 | Sous-menus Societe secrete |
| hoa_menu.90-99 | Sous-menus Factions |
| hoa_menu.100-109 | Sous-menus Investissements |

---

## 5. IMPACT SUR L'UX JOUEUR

### Avant (actuel)

```
Onglet Intrigue:
  [60-85 decisions en vrac, scroll interminable]
  - Pas de categorie
  - Pas d'ordre logique
  - Le joueur ne sait pas par ou commencer
```

### Apres (refonte)

```
Onglet Intrigue:
  [ ] Heroes of Azeroth          <-- 1 clic = menu organise
  [ ] Economie de Royaume         <-- 1 clic = 4 options eco
  (+ eventuelles decisions vanilla CK2/GoA de base)
```

**Gain :**
- De 85 decisions → 2 decisions dans le panneau
- Navigation arborescente intuitive
- Menus contextuels (guerre visible seulement en guerre, classe visible seulement si classe)
- Boutons "Retour" pour naviguer sans se perdre
- L'IA continue de fonctionner exactement comme avant

---

## 6. LIMITATIONS CONNUES DE CK2

### 6.1 Ce qu'on ne peut PAS faire

| Limitation | Detail |
|---|---|
| Vrais onglets UI | CK2 ne supporte pas l'ajout de tabs natifs au panneau de decisions |
| Boutons custom dans .gui | Les boutons ne peuvent pas declencher d'events directement |
| Plus de 20 options/event | Limite technique du moteur (~20 options max par event) |
| Arbre de talents visuel | Pas de widget tree/graph dans le moteur GUI |
| Icones custom dans menus | Les options d'events n'ont pas d'icones individuelles |

### 6.2 Contournements possibles

| Besoin | Solution |
|---|---|
| "Onglets" | Decision-to-Event menu (la technique qu'on applique) |
| Arbre de talents | Chaine de decisions avec prerequis, affiches dans le desc de l'event |
| Inventaire etendu | Event qui liste les artefacts equipes dans le texte de description |
| Ressources custom | Province modifiers + affichage dans les descriptions d'events |

---

## 7. PLAN D'IMPLEMENTATION PAR PHASES

### Phase 1 : Menu principal + migration decisions (PRIORITE HAUTE)
- Creer `hoa_master_menu.txt` (1 decision gateway)
- Creer `hoa_menu_events.txt` (menu principal + 10 sous-menus)
- Modifier toutes les `decisions = { }` en `ai = yes` only
- Creer `hoa_menu.csv` localisation
- **Impact :** 85 decisions → 2 dans le panel

### Phase 2 : Menu IE + settlement decisions
- Creer `ie_master_menu.txt`
- Deplacer les decisions de batiment IE en `settlement_decisions`
- **Impact :** Decisions eco accessibles via clic-droit sur holding

### Phase 3 : Enrichissement des sous-menus
- Ajouter descriptions detaillees dans les descs d'events
- Afficher les cooldowns restants dans le texte
- Afficher les stats/ressources dans le texte du menu
- Pagination propre pour les donjons

### Phase 4 : Nouvelles features via le menu
- Systeme de potions (nouveau sous-menu)
- Entrainement (nouveau sous-menu dans Actions perso)
- Boutiques (nouveau sous-menu dans Commerce)
- Chaque feature = juste un nouveau sous-menu, pas de nouvelles decisions dans le panel

---

## 8. RESUME EXECUTIF

| Metrique | Avant | Apres |
|---|---|---|
| Decisions dans l'onglet Intrigue | ~85 | 2 |
| Decisions en clic-droit | ~17 | ~17 (inchange) |
| Profondeur max de navigation | 1 (flat) | 3 (menu → sous-menu → action) |
| Nombre de clics pour une action | 1 | 2-3 |
| Capacite d'ajout de features | Ajouter 1 decision = +1 ligne dans le panel | Ajouter 1 option dans un sous-menu = 0 impact panel |
| Compatibilite autres mods | Bonne | Excellente (zero fichier .gui modifie) |
| IA | Fonctionne | Fonctionne identiquement (decisions ai=yes conservees) |

**Conclusion :** La refonte en menus events est LA solution standard CK2. Tous les mods majeurs l'utilisent. C'est propre, scalable, et ca permet d'ajouter des dizaines de features futures (potions, entrainement, boutiques) sans jamais polluer l'onglet Intrigue.
