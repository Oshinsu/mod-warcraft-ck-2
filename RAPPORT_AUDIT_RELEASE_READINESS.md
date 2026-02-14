# Rapport d'Audit : Les submods GoA sont-ils prets a sortir ?

## Verdict : NON - Pas en l'etat

**Score global de pret : 38/100**

Les deux submods contiennent un volume de contenu impressionnant (11,031 lignes de script, 54 assets graphiques, 599 cles de localisation) mais souffrent de **bloqueurs critiques** qui les rendraient non-fonctionnels ou gravement defaillants en conditions reelles. Ce rapport detaille chaque probleme, sa severite, et le correctif necessaire.

---

## Table des matieres

1. [Resume executif par submod](#1-resume-executif)
2. [Bloqueurs critiques (CRASH/CASSE)](#2-bloqueurs-critiques)
3. [Problemes majeurs (FONCTIONNEL DEGRADE)](#3-problemes-majeurs)
4. [Problemes mineurs (POLISH)](#4-problemes-mineurs)
5. [Conformite aux bonnes pratiques CK2](#5-conformite-bonnes-pratiques)
6. [Comparaison avec les standards de la scene](#6-comparaison-standards)
7. [Matrice des fichiers manquants](#7-fichiers-manquants)
8. [Plan de remediation prioritise](#8-plan-remediation)
9. [Ce qui est BIEN et ne doit pas changer](#9-ce-qui-est-bien)

---

## 1. Resume executif

### GoA: Heroes of Azeroth

| Critere | Score | Detail |
|---------|-------|--------|
| Structure .mod | 6/10 | Correcte mais sans thumbnail |
| PDXScript | 7/10 | Syntaxe globalement correcte, pas de bugs structurels |
| Localisation | 4/10 | 324 cles manquantes, 147 sans DE/ES |
| GFX/Assets | 2/10 | Images 20-50x trop grosses, mauvais format, 30 refs GFX cassees |
| Equilibrage | 6/10 | Grilles definies dans CLAUDE.md mais non testees in-game |
| Completude contenu | 5/10 | Raids solides mais politique quasi-absente |
| Performance | 3/10 | 302 MB d'images non-optimisees |
| **Score moyen** | **4.7/10** | |

### GoA: Improved Economy

| Critere | Score | Detail |
|---------|-------|--------|
| Structure .mod | 6/10 | Correcte mais sans thumbnail |
| PDXScript | 8/10 | Buildings bien structures, chaines valides |
| Localisation | 5/10 | Couverture EN/FR OK, DE/ES incomplets pour HoA partner |
| GFX/Assets | 1/10 | Dossiers gfx/ et interface/ VIDES - aucun icone de batiment |
| Equilibrage | 7/10 | Couts et revenues semblent raisonnables |
| Completude contenu | 6/10 | 131 batiments mais pas d'events lies |
| Performance | 9/10 | Leger (0.1 MB), pas de souci |
| **Score moyen** | **6.0/10** | |

---

## 2. Bloqueurs critiques

### CRITIQUE-1 : Images au mauvais format et surdimensionnees (HoA)

**Severite : BLOQUEUR RELEASE**

| Probleme | Constate | Standard CK2 |
|----------|---------|--------------|
| Format | PNG brut | DDS (DirectDraw Surface) |
| Event pictures | 2528x1696 px | 460x300 px |
| Inventory icons | 2048x2048 px | 80x80 px ou 60x60 px |
| Taille moyenne | 5.6 MB / image | 50-300 KB / image |
| Taille totale | **302 MB** | **~5-15 MB** |

**Consequences en jeu :**
- CK2 supporte le PNG mais le charge en RAM non-compresse. 54 images x 5.6 MB = ~300 MB de RAM additionnelle juste pour les textures du submod
- Les event pictures a 2528x1696 seront affichees dans un cadre de 460x300 : CK2 va les downscaler en temps reel a chaque affichage, causant du lag
- Les icones d'inventaire a 2048x2048 pour un slot de 60x60 representent un ratio de 1:1000 en surface - absurdement surdimensionne
- Le poids de 302 MB depasse la taille de TOUT le mod GoA de base. Sur Steam Workshop, cela rend le submod impraticable (telechargement lent, decompression lente)
- Sur certains GPU limites (integres), charger 302 MB de textures non-compressees peut causer des crashes memoire

**Correctif requis :**
1. Redimensionner les event pictures a 460x300 px
2. Redimensionner les inventory icons a 80x80 px
3. Convertir TOUT en DDS (format DXT1 pour event pictures sans alpha, DXT5 pour icons avec alpha)
4. Outil : `nvcompress` ou `texconv` (DirectXTex) ou `convert` (ImageMagick) + `nvdxt`
5. Resultat attendu : ~5-15 MB total au lieu de 302 MB

---

### CRITIQUE-2 : 30 references GFX cassees (HoA)

**Severite : BLOQUEUR VISUEL**

Les artefacts T0 et T0.5 referencent 30 sprites GFX qui n'existent NI dans les fichiers `.gfx` du submod, NI dans les images du submod :

```
GFX_inv_chest_cloth_44               GFX_inv_helm_cloth_dungeoncloth_c_01
GFX_inv_chest_cloth_raidmage_j_01    GFX_inv_helm_cloth_raidmage_j_01
GFX_inv_chest_leather_28             GFX_inv_helm_leather_dungeonleather_c_01
GFX_inv_chest_mail_15                GFX_inv_helm_mail_dungeonmail_c_01
GFX_inv_chest_mail_19                GFX_inv_helm_mail_dungeonmail_c_02
GFX_inv_chest_plate_16               GFX_inv_helm_plate_dungeonplate_c_01
GFX_inv_chest_plate_22               GFX_inv_helm_plate_dungeonplate_c_02
GFX_inv_chest_plate_24               GFX_inv_helm_plate_raidwarrior_j_01
GFX_inv_chest_plate_raidwarrior_j_01 GFX_inv_jewelry_necklace_13
GFX_inv_glove_cloth_dungeoncloth_c_01 GFX_inv_jewelry_necklace_21
GFX_inv_glove_plate_dungeonplate_c_03 GFX_inv_jewelry_ring_36
GFX_evt_battle                        GFX_inv_jewelry_ring_57
GFX_evt_council                        GFX_inv_staff_30 / _47
                                       GFX_inv_sword_27 / _39 / _48
```

**Hypothese** : Ces noms suivent la convention de nommage WoW (`inv_chest_plate_16` etc.) et sont probablement definis dans le mod GoA de base. MAIS :
- Sans acces au GoA de base, c'est **inverifiable**
- Si GoA de base ne les definit PAS exactement avec ces noms, chaque artefact T0 affichera une **icone rouge X** (le sprite d'erreur de CK2)
- Les 2 references `GFX_evt_battle` et `GFX_evt_council` sont des noms generiques qui pourraient venir de vanilla CK2 - mais GoA etant une conversion totale, vanilla est ecrase

**Correctif requis :**
1. Telecharger GoA de base et verifier que ces 30 GFX existent dans ses fichiers `.gfx`
2. Pour chaque GFX manquante : soit creer l'image + la declaration `.gfx`, soit remplacer par un sprite existant
3. En fallback : creer un fichier `hoa_fallback_icons.gfx` qui mappe les noms manquants vers des sprites generiques du submod

---

### CRITIQUE-3 : 324 cles de localisation manquantes

**Severite : BLOQUEUR VISUEL**

Sur 421 elements scriptés nécessitant une localisation, **324 n'ont aucune entree dans les CSV** (77% de couverture manquante). En jeu, ces elements afficheront leur code interne brut au lieu d'un texte lisible.

**Repartition des manques :**

| Type | Definis | Localises | Manquants | Exemples |
|------|---------|-----------|-----------|----------|
| Artefacts (noms) | 54 | ~24 | ~30 | `hoa_barons_deathcharger_reins`, `hoa_blackhand_doomsaw` |
| Artefacts (desc) | 54 | ~12 | ~42 | Toutes les `_desc` des T0 sets |
| Batiments (desc) | ~131 | ~60 | ~71 | `hoa_academie_demonologie_1_desc`, `hoa_cercle_druidique_2_desc` |
| Crafted items | ~20 | 0 | ~20 | `hoa_crafted_amulet_rare`, `hoa_crafted_plate_epic` |
| Modifiers | ~51 | ~20 | ~31 | `hoa_monument_built`, `hoa_crafting_cooldown` |
| Event modifiers | ~30 | ~15 | ~15 | Cooldowns et buffs temporaires |

**Impact en jeu :**
- Les noms d'artefacts T0 s'affichent comme `hoa_blackhand_doomsaw` au lieu de "Doomsaw de Main-noire"
- Les descriptions de batiments montrent `hoa_academie_demonologie_1_desc` au lieu du texte de flavour
- Les items craftes sont illisibles
- **Note** : Les modifiers hidden (cooldowns) n'ont pas besoin de localisation car ils ne sont jamais affiches. Les 10 modifiers "manquants" trouves dans les decisions sont en fait des cooldowns `hidden = yes` - ceci est correct et ne constitue PAS un probleme.

**Correctif requis :**
1. Generer les 324 cles manquantes pour les 4 langues
2. Priorite : EN d'abord (fallback universel), puis FR, puis DE/ES

---

### CRITIQUE-4 : Improved Economy n'a AUCUN asset graphique

**Severite : BLOQUEUR VISUEL (IE)**

Le submod Improved Economy definit 131 batiments uniques mais :
- `GoA_Improved_Economy/gfx/` - contient des dossiers vides (0 fichiers)
- `GoA_Improved_Economy/interface/` - vide (0 fichiers `.gfx`)

**Consequence :** Aucun des 131 batiments n'aura d'icone custom. CK2 affichera :
- L'icone par defaut de la categorie (chateau generique, ville generique, etc.)
- Ou un carre blanc si la reference pointe vers un GFX inexistant

**Correctif requis :**
1. Creer des icones de batiment (56x56 DDS chacune) pour au minimum les batiments uniques (mines, ateliers, capitales)
2. Creer le fichier `interface/ie_buildings.gfx` avec les declarations spriteType
3. Alternative minimale : reutiliser des icones du GoA de base en les referencant

---

## 3. Problemes majeurs

### MAJEUR-1 : Encodage UTF-8 au lieu de Windows-1252

**Severite : DEGRADATION TEXTE**

9 fichiers contiennent des caracteres non-ASCII encodes en UTF-8 au lieu de Windows-1252 :

| Fichier | Bytes non-ASCII | Caracteres concernes |
|---------|----------------|---------------------|
| `hoa_race_retinues.txt` | 8 | e avec accent (commentaires FR) |
| `hoa_raid_events.txt` | 6 | Fleche → (commentaires) |
| `hoa_t0_events.txt` | 6 | Fleche → (commentaires) |
| `hoa_buildings.csv` | 20 | Accents DE (geschäftiges, Tränke) |
| `hoa_decisions.csv` | 2 | Accent FR (imprégner) |
| `hoa_magic_economy_fr.csv` | 2 | Accent FR (dorés) |
| `hoa_retinues_fr.csv` | 2 | Accent FR (combinées) |
| `hoa_t05_events.csv` | 6 | Accent DE (Kriegshäuptling, Flüche) |
| `hoa_t0_events.csv` | 2 | Espagnol (¿Osais) |

**Consequence :** Les caracteres accentues s'afficheront comme des carres ou des symboles bizarres en jeu. `Kriegshäuptling` deviendra `KriegshÃ¤uptling`.

**Correctif requis :**
1. Convertir tous les fichiers en Windows-1252 (ANSI)
2. Remplacer les fleches → par `->` dans les commentaires
3. Verifier que les accents (e, a, u, n, etc.) sont correctement preserves apres conversion
4. Outil : `iconv -f UTF-8 -t WINDOWS-1252 input.csv > output.csv`

---

### MAJEUR-2 : Fichiers .mod sans thumbnail

**Severite : BLOCAGE WORKSHOP**

Les deux fichiers `.mod` ont `picture = ""` (champ vide). C'est un **prerequis pour la publication Steam Workshop**.

**Correctif :** Creer une image PNG 499x499 par submod et renseigner le champ `picture`.

---

### MAJEUR-3 : Dependance GoA non-verifiable

**Severite : RISQUE D'INCOMPATIBILITE**

Le mod GoA de base n'est pas present dans le repository. Cela signifie que :
- Les 30 references GFX vers le GoA de base ne sont pas verifiables
- Les traits de classe (`class_warrior_5`, `creature_human`, etc.) references dans nos scripted triggers ne sont pas verifiables
- Les noms exacts des gouvernements, cultures, religions de GoA ne sont pas verifiables
- Les buildings du submod pourraient entrer en conflit avec des buildings de GoA ayant les memes noms

**Correctif requis :**
1. Telecharger GoA de base (GitHub : `Warcraft-GoA-Development-Team/Warcraft-Guardians-of-Azeroth`)
2. Documenter la version exacte de GoA ciblée (ex: v1.10.0)
3. Executer un script de cross-validation des references
4. Ajouter un README specifiant la version GoA requise

---

### MAJEUR-4 : Les scripted triggers ne sont PAS utilises dans les events/decisions

**Severite : DESIGN DEFAILLANT**

Le fichier `hoa_triggers.txt` definit 14 scripted triggers utiles :
- `has_any_class_trigger`
- `is_warrior_class_trigger`, `is_mage_class_trigger`, etc.
- `is_magic_class_trigger`

**Mais** : Une recherche exhaustive montre que **0 de ces triggers sont utilises** dans les events et decisions du submod. Les checks de classe sont probablement faits inline (repetition de `OR = { has_trait = class_warrior_1 ... class_warrior_10 }`).

**Consequences :**
- Code duplique a travers les fichiers
- Maintenance difficile (si GoA change les noms de traits, il faut corriger partout)
- Performance degradee (les scripted triggers sont caches par le moteur, pas les blocs inline)

**Correctif :**
1. Remplacer tous les checks inline par les scripted triggers
2. Ajouter de nouveaux triggers pour les patterns communs

---

### MAJEUR-5 : Aucun fichier `on_actions` pour les events periodiques

**Severite : CONTENU MORT**

CK2 a besoin d'un fichier `common/on_actions/` pour que les events MTTH ou `is_triggered_only` soient correctement delenches. Les events economiques de IE (`ie_economy.1` a `ie_economy.6`) utilisent `is_triggered_only = yes` mais sans integration dans `on_actions`, ils ne se declencheront JAMAIS spontanement.

Les events sont appeles dans des chaines entre eux et via decisions, mais les events economiques aleatoires (gold vein discovery, trade caravan, etc.) qui devraient se produire organiquement n'ont aucun declencheur periodique.

**Correctif :**
- Creer `common/on_actions/hoa_on_actions.txt` avec des hooks sur `on_yearly_pulse`, `on_five_year_pulse`, `on_battle_won`, etc.
- Ou bien convertir les events en MTTH (moins performant mais fonctionnel)

---

## 4. Problemes mineurs

### MINEUR-1 : Localisation DE/ES incomplete (147 cles)

Les fichiers `hoa_magic_economy_fr.csv` et `hoa_retinues_fr.csv` contiennent du francais et de l'anglais mais les colonnes allemande et espagnole sont vides pour 147 cles. Le jeu affichera le texte anglais en fallback (pas de crash, mais experience degradee pour les joueurs DE/ES).

### MINEUR-2 : Nommage de fichiers localisation inconsistant

- `hoa_magic_economy_fr.csv` et `hoa_retinues_fr.csv` ont un suffixe `_fr` qui suggere qu'ils ne contiennent que du francais. En realite, ils contiennent toutes les langues. Ce nommage est trompeur.
- Les fichiers IE n'ont pas de suffixe de langue (correct).
- Recommandation : renommer en `hoa_magic_economy.csv` et `hoa_retinues.csv`.

### MINEUR-3 : Pas de loading screens pour IE

Le submod IE n'a aucun loading screen. Ce n'est pas un bug mais c'est un element de polish que la plupart des mods publies incluent.

### MINEUR-4 : Pas de `user_dir` dans les .mod

Sans `user_dir`, les sauvegardes faites avec le submod actif seront stockees dans le meme dossier que les sauvegardes vanilla/GoA. Si le joueur desactive le submod, les vieilles sauvegardes crasheront silencieusement.

**Correctif :** Ajouter `user_dir = "GoA_Heroes_of_Azeroth"` dans le .mod (optionnel mais recommande).

### MINEUR-5 : Commentaires en francais dans le code

Les fichiers `hoa_race_retinues.txt` contiennent des commentaires en francais avec accents (`# disciplinés`, `# RÉPROUVÉS`). Ce n'est pas un bug (les commentaires sont ignores par le parser) mais cela peut causer des problemes si un outil tiers tente de parser le fichier en Windows-1252.

---

## 5. Conformite aux bonnes pratiques CK2

### Structure de fichiers

| Bonne pratique | HoA | IE | Note |
|---------------|-----|-----|------|
| Fichier .mod avec name/path/dependencies | OK | OK | |
| Pas de `replace_path` (submod) | OK | OK | Correct pour un submod |
| Hierarchie de dossiers miroir CK2 | OK | OK | |
| Prefixe unique pour les noms (`hoa_`, `ie_`) | OK | OK | Excellent |
| Namespaces d'events uniques | OK | OK | 5 namespaces, 0 collision |
| Pas de duplication d'ID events | OK | OK | Verifie: 0 doublons reels |
| Chaines de buildings valides | OK | OK | 131 buildings, 0 chaine cassee |

### Encodage et format

| Bonne pratique | HoA | IE | Note |
|---------------|-----|-----|------|
| Fichiers .txt en Windows-1252 | PARTIEL | OK | 3 fichiers HoA en UTF-8 |
| Fichiers .csv en Windows-1252 | NON | OK | 7 fichiers HoA en UTF-8 |
| CSV format 15 colonnes avec `;` | OK | OK | Toutes les lignes validees |
| CSV terminant par `x` | OK | OK | |
| Images en DDS | NON | N/A | 54 PNG au lieu de DDS |
| Images aux bonnes dimensions | NON | N/A | 20-50x trop grandes |

### Performance

| Bonne pratique | HoA | IE | Note |
|---------------|-----|-----|------|
| `is_triggered_only` au lieu de MTTH | OK | OK | Tous les events sont triggered_only |
| Scripted triggers pour logique repetee | DEFINI mais NON UTILISE | N/A | Les triggers existent mais ne sont pas references |
| Pas de `any_character` dans les triggers | OK | OK | |
| Decisions avec `ai = no` pour le joueur seul | PARTIEL | PARTIEL | A verifier par decision |
| Taille totale mod < 1 GB | OK (302 MB) | OK (0.1 MB) | Mais 302 MB est tres eleve |

---

## 6. Comparaison avec les standards de la scene

### Comparaison avec les submods GoA connus

| Critere | GoA: Unlimited (ref) | HoA (nous) | IE (nous) |
|---------|---------------------|------------|-----------|
| .mod structure | Complet avec thumbnail | OK sans thumbnail | OK sans thumbnail |
| Encoding | Windows-1252 | Mix UTF-8/ASCII | ASCII pur |
| Images | DDS, dimensions correctes | PNG, surdimensionnees | Aucune image |
| Localisation | EN complete | 77% manquante | EN/FR OK |
| Taille | ~5 MB | 302 MB | 0.1 MB |
| Version GoA documentee | Oui | Non | Non |

### Comparaison avec les submods AGOT / HIP / Elder Kings

| Critere | Standard communaute | HoA | IE |
|---------|-------------------|-----|-----|
| README / Changelog | Toujours present | Absent | Absent |
| Compatibilite documentee | Version base mod specifiee | Non | Non |
| Fichier `on_actions` | Si events periodiques | Absent | Absent |
| Traits avec icones `.gfx` | Toujours | N/A (pas de traits custom) | N/A |
| Test avec error.log propre | Prerequis release | Non verifie | Non verifie |
| DDS pour toutes textures | Standard | NON (PNG) | N/A |

---

## 7. Matrice des fichiers manquants

### Fichiers qui DOIVENT exister pour une release fonctionnelle

| Fichier | Submod | Existe | Priorite |
|---------|--------|--------|----------|
| `thumbnail.png` (499x499) | HoA | NON | HAUTE |
| `thumbnail.png` (499x499) | IE | NON | HAUTE |
| `common/on_actions/hoa_on_actions.txt` | HoA | NON | HAUTE |
| `common/on_actions/ie_on_actions.txt` | IE | NON | HAUTE |
| `interface/ie_buildings.gfx` | IE | NON (vide) | HAUTE |
| `gfx/interface/buildings/*.dds` (icones) | IE | NON | HAUTE |
| 324 cles localisation manquantes | HoA | NON | HAUTE |
| `README.md` ou `README.txt` | Les deux | NON | MOYENNE |
| `CHANGELOG.txt` | Les deux | NON | MOYENNE |
| `gfx/loadingscreens/*.dds` | IE | NON | BASSE |

### Fichiers qui doivent etre CORRIGES

| Fichier | Probleme | Priorite |
|---------|----------|----------|
| 54 images PNG dans `gfx/` | Redimensionner + convertir DDS | CRITIQUE |
| 9 fichiers .txt/.csv | Reconvertir en Windows-1252 | HAUTE |
| `GoA_Heroes_of_Azeroth.mod` | Ajouter `picture = "thumbnail.png"` | HAUTE |
| `GoA_Improved_Economy.mod` | Ajouter `picture = "thumbnail.png"` | HAUTE |
| `hoa_magic_economy_fr.csv` | Renommer sans `_fr` | BASSE |
| `hoa_retinues_fr.csv` | Renommer sans `_fr` | BASSE |

---

## 8. Plan de remediation prioritise

### Sprint 1 : Bloqueurs critiques (sans cela, le mod est casse)

| Tache | Effort | Impact |
|-------|--------|--------|
| 1a. Redimensionner 18 event pictures a 460x300 | 1h (script batch) | -95% taille |
| 1b. Redimensionner 36 inventory icons a 80x80 | 1h (script batch) | -99.8% taille |
| 1c. Convertir 54 images PNG -> DDS | 1h (nvcompress batch) | Compatibilite standard |
| 1d. Mettre a jour les chemins dans `.gfx` (`.png` -> `.dds`) | 30min | References correctes |
| 2. Resoudre les 30 GFX manquantes | 3h | Plus de X rouges |
| 3. Generer les 324 cles de localisation EN | 4h | Textes lisibles |
| 4. Convertir 9 fichiers UTF-8 -> Windows-1252 | 30min (iconv batch) | Accents corrects |
| **Total Sprint 1** | **~11h** | |

### Sprint 2 : Fonctionnel complet (le mod marche correctement)

| Tache | Effort | Impact |
|-------|--------|--------|
| 5. Creer `on_actions` pour events periodiques | 2h | Events se declenchent |
| 6. Creer thumbnails .mod (2 images) | 1h | Publication Workshop possible |
| 7. Refactorer events/decisions pour utiliser scripted triggers | 3h | Maintenabilite |
| 8. Creer icones batiments IE (ou reutiliser GoA) | 4h | IE visuellement complet |
| 9. Ajouter localisation FR/DE/ES pour les 324 cles | 6h | Multilangue |
| **Total Sprint 2** | **~16h** | |

### Sprint 3 : Publication-ready (qualite Workshop)

| Tache | Effort | Impact |
|-------|--------|--------|
| 10. Creer README.md pour chaque submod | 2h | Documentation utilisateur |
| 11. Creer CHANGELOG.txt | 1h | Suivi de versions |
| 12. Tester avec GoA base (error.log propre) | 4h | Zero erreur au boot |
| 13. Tester toutes les decisions/events in-game | 8h | Validation gameplay |
| 14. Ajouter `user_dir` aux .mod | 10min | Isolation des saves |
| 15. Renommer fichiers `_fr.csv` | 10min | Nommage coherent |
| **Total Sprint 3** | **~15h** | |

### Effort total estime : ~42 heures

---

## 9. Ce qui est BIEN et ne doit pas changer

Il est important de noter que beaucoup de choses sont **correctement faites** :

### Architecture
- Le decoupage en 2 submods independants (economie vs gameplay) est une excellente decision
- Le prefixage systematique (`hoa_`, `ie_`) est impeccable
- L'absence de `replace_path` est correcte pour des submods
- La declaration `dependencies` vers GoA est correcte
- Les tags sont pertinents et bien choisis

### Script PDXScript
- La syntaxe est globalement correcte (pas d'accolades manquantes, pas de scopes invalides)
- Les 5 namespaces sont uniques et bien organises
- Zero duplication d'ID d'events (verifie par analyse complete)
- Les chaines de buildings (131 batiments, `upgrades_from`) sont toutes valides
- Le format CSV (15 colonnes, terminaison `;x`) est correct dans tous les fichiers
- L'utilisation de `is_triggered_only = yes` partout (au lieu de MTTH) est une bonne pratique de performance

### Contenu
- Les 54 artefacts (T0, T0.5, T1, T2, crafted) couvrent bien la progression WoW
- Les 14 decisions "power" offrent un gameplay sandbox riche
- Les 12 raids (4 T0, 3 T0.5, 1 raid 20-man, 4 raids 40-man) avec 3 stages chacun representent un contenu consequent
- Les ~30 retinues raciales avec 962 lignes sont une addition significative
- Les 131 batiments economiques couvrent mining, crafting, magie, culture et capitales uniques
- La grille d'equilibrage documentee (CLAUDE.md) est un atout precieux

### Qualite des assets
- Les 54 images sont visuellement de haute qualite (generees par IA avec prompts detailles)
- Elles couvrent tous les dungeons, raids, et types d'items
- Elles ont juste besoin d'etre redimensionnees et converties - pas refaites

---

## Annexe A : Inventaire complet des fichiers

### GoA: Heroes of Azeroth (8,255 lignes de script + 540 lignes loc + 335 lignes GFX)

```
common/
  artifacts/
    hoa_t0_sets.txt              291 lignes  (artefacts T0/T0.5 dungeon drops)
    hoa_tier_sets.txt            571 lignes  (tier sets T1/T2)
  buildings/
    hoa_magic_economy.txt        962 lignes  (batiments magiques)
    hoa_province_economy.txt     592 lignes  (batiments province)
    hoa_special_buildings.txt    327 lignes  (structures legendaires)
  event_modifiers/
    hoa_modifiers.txt            252 lignes  (51 modifiers)
  retinue/
    hoa_race_retinues.txt        998 lignes  (~30 retinues raciales)
  scripted_triggers/
    hoa_triggers.txt             192 lignes  (14 triggers)
decisions/
  hoa_crafting_decisions.txt     301 lignes  (forge, enchant, desenchant)
  hoa_diplomacy_decisions.txt    192 lignes  (duel, pacte, emissaire)
  hoa_dungeon_decisions.txt      578 lignes  (raids T0 a T2)
  hoa_power_decisions.txt        681 lignes  (14 decisions sandbox)
events/
  hoa_diplomacy_events.txt       406 lignes  (5 events)
  hoa_raid_events.txt            702 lignes  (12 events, 4 raids)
  hoa_t05_events.txt             537 lignes  (12 events, 3 dungeons)
  hoa_t0_events.txt              673 lignes  (15 events, 5 dungeons)
interface/
  hoa_event_pictures.gfx         106 lignes  (18 sprites)
  hoa_inventory_icons.gfx        229 lignes  (36 sprites)
gfx/interface/
  event_pictures/                18 fichiers PNG (2528x1696, ~6.3 MB chacun)
  inventory/                     36 fichiers PNG (2048x2048, ~5.3 MB chacun)
localisation/
  10 fichiers CSV                540 lignes  (599 cles)
```

### GoA: Improved Economy (2,776 lignes de script)

```
common/
  buildings/
    ie_castle_economy.txt        391 lignes  (mines 5 tiers)
    ie_culture_economy.txt      1283 lignes  (11 batiments culturels)
    ie_tribal_economy.txt        144 lignes  (batiments tribaux)
    ie_unique_capitals.txt       244 lignes  (9 capitales uniques)
  event_modifiers/
    ie_character_modifiers.txt    14 lignes
    ie_event_modifiers.txt        46 lignes
decisions/
  ie_economy_decisions.txt       212 lignes
events/
  ie_economy_events.txt          372 lignes  (6 events)
localisation/
  ie_buildings.csv                37 lignes
  ie_events.csv                   33 lignes
gfx/                              VIDE
interface/                        VIDE
```

---

## Annexe B : Checklist de validation pre-release

- [ ] Toutes les images converties en DDS aux bonnes dimensions
- [ ] Taille totale HoA < 20 MB
- [ ] 0 references GFX cassees
- [ ] 0 cles de localisation EN manquantes
- [ ] Tous les fichiers en encodage Windows-1252
- [ ] Thumbnails 499x499 crees et references dans .mod
- [ ] `on_actions` pour les events periodiques
- [ ] Icones de batiments pour IE
- [ ] Test avec GoA base : error.log propre au boot
- [ ] Test de chaque decision (apparition + execution)
- [ ] Test de chaque event chain (du debut a la fin)
- [ ] Test de chaque chaine de batiment (tier 1 a max)
- [ ] README avec version GoA requise
- [ ] CHANGELOG avec historique des modifications
