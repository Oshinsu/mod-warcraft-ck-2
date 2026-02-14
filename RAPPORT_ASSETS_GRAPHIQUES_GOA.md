# Rapport : Assets Graphiques GoA - Generation par IA (Replicate / Nano Banana Pro)

## 1. Architecture Graphique CK2

### 1.1 Structure des fichiers graphiques

```
mod_folder/
├── gfx/
│   ├── characters/              # Portraits de personnages
│   │   ├── portraits/           # Layers de portraits (base, clothes, hair, beard)
│   │   │   ├── portrait_properties/  # Définitions de propriétés
│   │   │   └── <culture>/       # Dossiers par culture (orc, elf, human...)
│   │   └── player_portraits/    # Portraits joueur (460x640 .tga)
│   ├── interface/
│   │   ├── event_pictures/      # Images d'événements (460x300 .dds)
│   │   ├── inventory/           # Icônes d'artefacts/équipement (80x80 .dds)
│   │   ├── icons/               # Icônes de traits, modifiers (29x29 .dds en spritesheet)
│   │   ├── buildings/           # Icônes de bâtiments (48x48 ou 80x80 .dds)
│   │   └── coat_of_arms/        # Blasons
│   ├── loadingscreens/          # Ecrans de chargement (1920x1080 .dds)
│   └── FX/                      # Shaders
├── interface/
│   └── *.gfx                    # Fichiers de définition des sprites
└── portraits/
    └── portraits.gfx            # Définitions de portraits
```

### 1.2 Formats d'image CK2

| Type | Format | Taille | Compression |
|------|--------|--------|-------------|
| Event pictures | .dds (DXT1/DXT5) | 460x300 px | DXT1 (sans alpha) |
| Inventory icons | .dds (DXT5) | 80x80 px | DXT5 (avec alpha/transparence) |
| Trait icons | .dds spritesheet | 29x29 px par icône | DXT5 |
| Building icons | .dds | 48x48 ou 80x80 px | DXT5 |
| Portraits layers | .dds (DXT5) | Variable (256x400 typ.) | DXT5 avec alpha |
| Loading screens | .dds (DXT1) | 1920x1080 px | DXT1 |
| Mod thumbnail | .jpg | 200x50 px | JPEG |

### 1.3 Comment CK2 résout les assets

```
Code PDXScript:  picture = "GFX_inv_sword_27"
        ↓
Fichier .gfx:    spriteType = { name = "GFX_inv_sword_27" texturefile = "gfx/interface/inventory/inv_sword_27.dds" }
        ↓
Fichier image:   gfx/interface/inventory/inv_sword_27.dds
```

### 1.4 Etat actuel du mod GoA HoA

**Aucun asset graphique custom.** Tout repose sur les assets du mod parent GoA et de CK2 vanilla.

- **7 images d'événements** réutilisées (GFX_evt_battle, GFX_evt_burning_house, etc.)
- **29 icônes d'inventaire** WoW standard (GFX_inv_sword_27, GFX_inv_helm_plate_*, etc.)
- **3 icônes de modificateurs** (icon = 1, 4, 14)
- **0 portraits custom**, **0 bâtiments custom**, **0 loading screens**

---

## 2. Assets à Générer

### 2.1 Inventaire complet des besoins

| Catégorie | Quantité | Taille cible | Priorité |
|-----------|----------|-------------|----------|
| **Event pictures (donjons/raids)** | ~25 | 460x300 → gen 1024x672 | HAUTE |
| **Event pictures (economie/diplo)** | ~15 | 460x300 → gen 1024x672 | MOYENNE |
| **Icônes d'artefacts (armes)** | ~20 | 80x80 → gen 512x512 | HAUTE |
| **Icônes d'artefacts (armures)** | ~30 | 80x80 → gen 512x512 | HAUTE |
| **Icônes d'artefacts (bijoux)** | ~15 | 80x80 → gen 512x512 | MOYENNE |
| **Icônes de bâtiments (race)** | ~45 | 48x48 → gen 512x512 | MOYENNE |
| **Icônes de bâtiments (magie)** | ~35 | 48x48 → gen 512x512 | MOYENNE |
| **Icônes de bâtiments (speciaux)** | ~12 | 48x48 → gen 512x512 | BASSE |
| **Portraits de race (layers)** | ~30+ sets | 256x400 → gen 1024x1600 | TRES HAUTE |
| **Icônes de traits** | ~20 | 29x29 → gen 256x256 | BASSE |
| **Icônes de retinues** | ~36 | 80x80 → gen 512x512 | MOYENNE |
| **Loading screens** | ~5 | 1920x1080 → gen 4096x2304 | BASSE |
| **Mod thumbnail** | 2 | 200x50 → gen 800x200 | BASSE |

**Total estimé : ~290 assets**

---

## 3. Pipeline de Génération IA

### 3.1 Architecture du pipeline

```
[1. Prompt JSON]  →  [2. API Replicate/Nano Banana Pro]  →  [3. PNG haute-res]
        ↓                                                          ↓
[4. Post-traitement Python]                                   [Downscale]
        ↓                                                          ↓
[5. Conversion DDS]  →  [6. Fichier .gfx]  →  [7. Intégration mod]
```

### 3.2 Outils nécessaires

```bash
# Conversion PNG → DDS
pip install Pillow
# ou utiliser ImageMagick :
convert input.png -define dds:compression=dxt5 output.dds

# Batch processing
pip install replicate  # API Replicate
```

### 3.3 Script de pipeline (concept)

```python
import replicate
import json
from PIL import Image

def generate_asset(prompt_json, output_path):
    """Genere un asset via Replicate API et convertit en DDS"""
    output = replicate.run(
        "nano-banana-2-pro",
        input={
            "prompt": prompt_json["scene_graph"]["environment"]["space"],
            "negative_prompt": " ".join(prompt_json["constraints"]["must_not_include"]),
            "width": prompt_json["parameters"]["render_resolution"].split("x")[0],
            "height": prompt_json["parameters"]["render_resolution"].split("x")[1],
            "num_inference_steps": prompt_json["parameters"]["steps"],
            "guidance_scale": prompt_json["parameters"]["guidance_strength"],
            "seed": prompt_json["parameters"]["seed"],
        }
    )
    # Post-traitement et conversion DDS ici
    return output
```

---

## 4. Prompts JSON Optimisés par Catégorie

### 4.1 EVENT PICTURES - Donjons & Raids

#### Template de base : Donjon

```json
{
  "meta": {
    "model_version": "nano-banana-2-pro",
    "task_type": "event_picture_dungeon",
    "project": "GOA_HEROES_OF_AZEROTH",
    "asset_id": "EVT_SHADOWFANG_KEEP_ENTRANCE",
    "scene_intent": "Vue dramatique de l'entrée d'un donjon gothique dans un monde dark fantasy Warcraft. Ambiance CK2 medievale heroique."
  },
  "scene_graph": {
    "style_bible": {
      "usp_core": [
        "World of Warcraft classic dungeon aesthetic",
        "CK2 event picture framing: wide establishing shot, painterly",
        "Medieval fantasy heroic tone, not grimdark"
      ],
      "look": "digital painting, oil paint texture, World of Warcraft concept art style, CK2 event illustration, matte painting quality",
      "palette": ["#1a1a2e", "#4a0e4e", "#c3a343", "#8b4513", "#2d5016"]
    },
    "environment": {
      "space": "Massive gothic castle perched on misty cliffs at twilight, Shadowfang Keep. Crumbling stone towers with green-glowing windows, spectral mist curling around battlements. A dark forest of dead trees surrounds the base. Worgen silhouettes visible in the fog. Iron portcullis with wolf-head motifs.",
      "atmosphere": "dread, gothic horror, haunted, moonlit",
      "scale_cues": [
        "tiny armored figures approaching the main gate for scale",
        "ravens circling the tallest tower",
        "lightning illuminating cloud banks behind the keep"
      ]
    },
    "camera": {
      "shot_type": "wide establishing shot, slight low angle",
      "lens": "35mm",
      "composition": "castle centered, framed by dead trees, path leading eye to gate",
      "aspect_ratio_note": "CK2 event pictures are wide format (460x300 = ~3:2)"
    },
    "lighting": {
      "key": "cold moonlight from upper left",
      "accent": "sickly green glow from keep windows, warm torchlight at gate",
      "fx": "volumetric fog, spectral wisps, subtle god rays through clouds"
    }
  },
  "parameters": {
    "aspect_ratio": "3:2",
    "render_resolution": "1024x672",
    "output_count": 3,
    "seed": -1,
    "steps": 50,
    "guidance_strength": 7.5,
    "sharpness": 0.4,
    "film_grain": 0.08
  },
  "constraints": {
    "must_include": [
      "gothic castle architecture",
      "spectral green glow",
      "misty atmosphere",
      "dark fantasy tone matching CK2 aesthetic"
    ],
    "must_not_include": [
      "modern elements",
      "text or UI elements",
      "anime style",
      "photorealistic humans close-up",
      "bright cheerful colors"
    ]
  }
}
```

#### Raid : Molten Core / Ragnaros

```json
{
  "meta": {
    "model_version": "nano-banana-2-pro",
    "task_type": "event_picture_raid",
    "project": "GOA_HEROES_OF_AZEROTH",
    "asset_id": "EVT_MOLTEN_CORE_RAGNAROS",
    "scene_intent": "Ragnaros le Seigneur du Feu émerge de son bassin de magma. Climax épique du raid Molten Core."
  },
  "scene_graph": {
    "style_bible": {
      "usp_core": [
        "Warcraft raid boss encounter at maximum epic scale",
        "CK2 event picture composition: painterly, dramatic",
        "BY FIRE BE PURGED energy"
      ],
      "look": "epic digital matte painting, Warcraft concept art, oil paint strokes, dramatic chiaroscuro",
      "palette": ["#ff4500", "#ff8c00", "#8b0000", "#1a0a00", "#ffd700"]
    },
    "environment": {
      "space": "Enormous cavern deep beneath Blackrock Mountain. A colossal fire elemental lord rises from a pool of molten lava, wielding a massive flaming hammer (Sulfuras). Rivers of magma flow between obsidian platforms. Tiny raid party silhouettes on a stone bridge for scale. Stalactites glow red-hot. Fire elementals float in the background.",
      "atmosphere": "apocalyptic, infernal, awe-inspiring, volcanic",
      "scale_cues": [
        "Ragnaros towers 50x the height of the raiders",
        "magma rivers wide as highways",
        "cavern ceiling barely visible in smoke and heat haze"
      ]
    },
    "camera": {
      "shot_type": "dramatic low angle looking up at Ragnaros",
      "lens": "24mm wide angle",
      "composition": "Ragnaros upper-center, hammer raised, raiders bottom-left for scale, lava pool reflection"
    },
    "lighting": {
      "key": "intense orange-red from magma and Ragnaros body",
      "accent": "white-hot core of Sulfuras hammer, blue-white spell effects from raiders",
      "fx": "heat distortion, ember particles, volcanic smoke, lava splashes"
    }
  },
  "parameters": {
    "aspect_ratio": "3:2",
    "render_resolution": "1024x672",
    "output_count": 3,
    "seed": -1,
    "steps": 60,
    "guidance_strength": 8.0,
    "sharpness": 0.35,
    "film_grain": 0.05
  },
  "constraints": {
    "must_include": [
      "colossal fire elemental emerging from lava",
      "massive flaming hammer",
      "underground volcanic cavern",
      "tiny raiders for scale"
    ],
    "must_not_include": [
      "text", "UI elements", "modern elements",
      "cute or cartoonish style", "anime"
    ]
  }
}
```

#### Template pour chaque donjon (liste des 13)

```json
{
  "meta": { "asset_id": "EVT_<DUNGEON_ID>" },
  "dungeon_prompts": {
    "shadowfang_keep": "Gothic haunted castle, spectral worgen, moonlit cliffs, green ghostly glow",
    "scarlet_monastery": "Red-bannered cathedral fortress, fanatical crusaders, crimson and gold, religious fervor",
    "gnomeregan": "Underground gnomish city, irradiated green glow, broken machinery, toxic pools, steampunk",
    "maraudon": "Sacred corrupted caverns, crystal formations, twisted nature elementals, purple corruption",
    "dire_maul": "Ancient elven ruins overgrown with jungle, massive broken columns, moonlit courtyard, ogres",
    "stratholme": "Burning plagued city streets, undead hordes, fire and plague, ruined human architecture",
    "scholomance": "Dark necromancy school, skeletal students, green necromantic energy, gothic lecture halls",
    "ubrs": "Volcanic fortress interior, black dragons, lava flows, orcish dark horde banners",
    "zulgurub": "Jungle troll temple, blood rituals, serpent god statues, primal voodoo energy, tribal",
    "molten_core": "Underground volcanic cavern, fire elementals, magma rivers, obsidian pillars",
    "bwl": "Dragon lair atop volcano, black dragon eggs, chromatic experiments, Nefarian's throne",
    "aq40": "Insectoid temple underground, qiraji swarm, Old God whispers, alien architecture, C'Thun eye",
    "naxxramas": "Floating necropolis, ice and death, Four Horsemen, skeletal architecture, Scourge banners"
  }
}
```

---

### 4.2 ICÔNES D'INVENTAIRE - Armes & Armures

#### Template : Arme (épée)

```json
{
  "meta": {
    "model_version": "nano-banana-2-pro",
    "task_type": "inventory_icon_weapon",
    "project": "GOA_HEROES_OF_AZEROTH",
    "asset_id": "INV_SWORD_ASHKANDI_EPIC",
    "scene_intent": "Icône d'inventaire WoW d'une épée à deux mains épique. Style icon carré, fond neutre."
  },
  "scene_graph": {
    "style_bible": {
      "usp_core": [
        "World of Warcraft inventory icon aesthetic exactly",
        "Single item centered on dark gradient background",
        "Painterly game icon style, slight 3D depth, clean silhouette"
      ],
      "look": "WoW item icon, hand-painted game asset, centered weapon on dark background, slight vignette, clean edges",
      "palette": ["#1a1a2e", "#a335ee", "#c0c0c0", "#ffd700", "#4169e1"]
    },
    "subject": {
      "item": "A massive two-handed greatsword with a dark blade etched with glowing purple runes. Cross-guard shaped like dragon wings. Pommel is a dark gemstone. The blade emanates a faint purple epic-quality glow.",
      "quality_glow": "purple epic border glow (quality = 4 epic)",
      "orientation": "diagonal from bottom-left to upper-right, blade pointing up-right"
    },
    "camera": {
      "shot_type": "flat icon view, slight 3/4 angle on blade",
      "composition": "weapon centered, fills 80% of frame, dark gradient background"
    },
    "lighting": {
      "key": "soft top-left key light on metal",
      "accent": "purple magical glow from runes, metallic specular highlights",
      "fx": "subtle purple particle trail, epic quality aura"
    }
  },
  "parameters": {
    "aspect_ratio": "1:1",
    "render_resolution": "512x512",
    "output_count": 3,
    "seed": -1,
    "steps": 40,
    "guidance_strength": 8.5,
    "sharpness": 0.5,
    "film_grain": 0.0
  },
  "constraints": {
    "must_include": [
      "single weapon only",
      "dark gradient background",
      "clear silhouette readable at 80x80",
      "WoW item icon composition"
    ],
    "must_not_include": [
      "hands or characters holding weapon",
      "text or labels",
      "busy background",
      "multiple items",
      "photorealistic style"
    ]
  }
}
```

#### Template : Armure (plastron)

```json
{
  "meta": {
    "model_version": "nano-banana-2-pro",
    "task_type": "inventory_icon_armor",
    "project": "GOA_HEROES_OF_AZEROTH",
    "asset_id": "INV_CHEST_T2_WARRIOR_PLATE",
    "scene_intent": "Icône d'inventaire WoW d'un plastron de plaque T2 guerrier (Wrath set). Bleu et or."
  },
  "scene_graph": {
    "style_bible": {
      "usp_core": [
        "WoW inventory icon style, chestpiece displayed flat",
        "T2 Warrior Wrath set visual identity: blue steel + gold trim"
      ],
      "look": "WoW item icon, hand-painted game asset, armor on dark background",
      "palette": ["#1a1a2e", "#0053a0", "#ffd700", "#c0c0c0", "#a335ee"]
    },
    "subject": {
      "item": "Heavy plate chestpiece, T2 warrior Wrath set style. Blue-tinted steel plates with gold filigree trim. Shoulder attachment points visible. Dragon motif embossed on chest. Belt buckle with lion/alliance crest. Purple epic quality glow.",
      "quality_glow": "purple epic glow",
      "orientation": "front-facing, shoulders slightly angled"
    },
    "camera": {
      "shot_type": "flat frontal icon view",
      "composition": "chestpiece centered, fills frame, dark gradient"
    },
    "lighting": {
      "key": "soft directional light from upper-left",
      "accent": "blue steel reflections, gold specular on trim",
      "fx": "subtle purple epic aura"
    }
  },
  "parameters": {
    "aspect_ratio": "1:1",
    "render_resolution": "512x512",
    "output_count": 3,
    "seed": -1,
    "steps": 40,
    "guidance_strength": 8.5,
    "sharpness": 0.5,
    "film_grain": 0.0
  },
  "constraints": {
    "must_include": [
      "single armor piece only",
      "dark background",
      "readable at 80x80",
      "WoW icon style"
    ],
    "must_not_include": [
      "person wearing armor",
      "text",
      "multiple items",
      "photorealistic"
    ]
  }
}
```

#### Système de qualité par couleur (bordure/glow)

```json
{
  "quality_system": {
    "1_common": { "glow": "none", "border": "#9d9d9d", "palette_note": "grey, dull" },
    "2_uncommon": { "glow": "faint green", "border": "#1eff00", "palette_note": "green tint" },
    "3_rare": { "glow": "blue", "border": "#0070dd", "palette_note": "blue glow" },
    "4_epic": { "glow": "purple", "border": "#a335ee", "palette_note": "purple aura" },
    "5_legendary": { "glow": "intense orange", "border": "#ff8000", "palette_note": "golden-orange fire glow" }
  }
}
```

---

### 4.3 ICÔNES DE BÂTIMENTS

#### Template : Bâtiment culturel

```json
{
  "meta": {
    "model_version": "nano-banana-2-pro",
    "task_type": "building_icon",
    "project": "GOA_HEROES_OF_AZEROTH",
    "asset_id": "BLDG_GUILDE_ENCHANTEURS",
    "scene_intent": "Icône de bâtiment CK2 : tour d'enchantement magique avec des runes brillantes."
  },
  "scene_graph": {
    "style_bible": {
      "usp_core": [
        "CK2 building icon aesthetic: small readable structure",
        "Warcraft architecture style for the given race",
        "Must read clearly at 48x48 pixels"
      ],
      "look": "CK2 building icon, miniature architectural illustration, painterly, clean readable shapes, slight isometric",
      "palette": ["#1a1a2e", "#7b68ee", "#ffd700", "#4a0e4e", "#c0c0c0"]
    },
    "subject": {
      "building": "A mystical tower with glowing arcane runes carved into its stone walls. Purple crystal at the top emanating magical energy. Enchanting table visible through an arched window. Floating magical particles around the structure. Warcraft high-elf architecture style.",
      "culture": "universal_magic",
      "size": "single building, compact composition"
    },
    "camera": {
      "shot_type": "slight isometric 3/4 view from above",
      "composition": "building centered, minimal ground plane, sky gradient background"
    },
    "lighting": {
      "key": "warm ambient from upper-left",
      "accent": "purple/blue magical glow from runes and crystal",
      "fx": "magical sparkles, subtle light beams"
    }
  },
  "parameters": {
    "aspect_ratio": "1:1",
    "render_resolution": "512x512",
    "output_count": 2,
    "seed": -1,
    "steps": 35,
    "guidance_strength": 8.0,
    "sharpness": 0.6,
    "film_grain": 0.0
  },
  "constraints": {
    "must_include": [
      "single building structure",
      "readable silhouette at small size",
      "magical/fantasy architectural elements",
      "clean background"
    ],
    "must_not_include": [
      "people or characters",
      "text",
      "modern architecture",
      "busy cluttered scene"
    ]
  }
}
```

#### Architecture par race (style keywords)

```json
{
  "race_architecture_keywords": {
    "human": "Stormwind stone cathedral gothic, blue and gold banners, lion motifs, cobblestone, medieval european",
    "orc": "Orgrimmar spiked iron and red steel, Horde banners, animal skulls, crude but imposing, war drums",
    "night_elf": "Darnassus ancient tree-integrated, moonstone, silver leaf motifs, nature-grown, bioluminescent purple",
    "dwarf": "Ironforge carved mountain stone, bronze and iron, gears, forge fires, sturdy geometric, underground",
    "gnome": "Gnomeregan copper pipes, gears, spinning cogs, glass tubes, chaotic invention lab, steam vents",
    "troll": "Zul'Gurub jungle stone, voodoo masks, bone totems, tiki torches, overgrown with vines",
    "tauren": "Thunder Bluff hide tents, wooden totems, feathers, natural materials, mesa architecture, leather and bone",
    "forsaken": "Undercity green slime, gothic decay, iron cages, plague barrels, dark purple banners, stitched flesh",
    "blood_elf": "Silvermoon ornate gold and crimson, arcane crystals, elegant spires, mana-infused, flowing curves",
    "draenei": "Exodar crystalline purple-blue, naaru light, dimensional tech, alien geometry, holy radiance",
    "goblin": "Gadgetzan corrugated metal, neon signs, explosive barrels, gold coins, ramshackle but profitable",
    "worgen": "Gilneas Victorian gothic, dark stone, iron fences, gas lamps, wolf motifs, perpetual fog"
  }
}
```

---

### 4.4 PORTRAITS DE PERSONNAGES

Les portraits CK2 sont composés de **layers** superposés :

```
Layer 0: Base (visage nu, teint de peau)
Layer 1: Yeux
Layer 2: Nez
Layer 3: Bouche
Layer 4: Oreilles
Layer 5: Cheveux
Layer 6: Barbe (optionnel)
Layer 7: Vêtements
Layer 8: Casque/couronne (optionnel)
Layer 9: Cadre/bordure
```

#### Template : Portrait base de race

```json
{
  "meta": {
    "model_version": "nano-banana-2-pro",
    "task_type": "portrait_layer_base",
    "project": "GOA_HEROES_OF_AZEROTH",
    "asset_id": "PORTRAIT_ORC_MALE_BASE_01",
    "scene_intent": "Layer de base pour portrait CK2 d'un orc mâle. Fond transparent (alpha). Visage frontal."
  },
  "scene_graph": {
    "style_bible": {
      "usp_core": [
        "CK2 portrait layer: MUST be front-facing, centered, neutral expression",
        "Warcraft orc racial features: green skin, tusks, broad jaw, heavy brow",
        "Portrait painting style matching CK2 aesthetic"
      ],
      "look": "CK2 character portrait, oil painting style, front-facing bust, Warcraft orc, detailed face",
      "palette": ["#2d5a27", "#4a7a3f", "#1a3a15", "#8b4513", "#ffd700"]
    },
    "subject": {
      "race": "orc",
      "gender": "male",
      "features": "Green skin, prominent lower jaw tusks, heavy brow ridge, broad flat nose, small deep-set eyes with amber/red iris, muscular neck, scarred. Stoic warrior expression.",
      "framing": "head and shoulders bust, front-facing, eyes looking at viewer",
      "background": "solid color or transparent (will be composited)"
    },
    "camera": {
      "shot_type": "passport-style front bust",
      "composition": "head centered upper third, shoulders visible, face fills most of frame"
    },
    "lighting": {
      "key": "soft three-point lighting for clear facial features",
      "accent": "warm side light to show skin texture and scars",
      "fx": "none - clean portrait lighting"
    }
  },
  "parameters": {
    "aspect_ratio": "2:3",
    "render_resolution": "1024x1536",
    "output_count": 5,
    "seed": -1,
    "steps": 50,
    "guidance_strength": 7.5,
    "sharpness": 0.45,
    "film_grain": 0.03
  },
  "constraints": {
    "must_include": [
      "front-facing portrait",
      "clearly visible racial features",
      "neutral to stoic expression",
      "head and shoulders framing"
    ],
    "must_not_include": [
      "profile or 3/4 angle",
      "action pose",
      "weapons in frame",
      "text",
      "anime style"
    ]
  }
}
```

#### Traits raciaux par race (pour le prompt subject.features)

```json
{
  "race_portrait_features": {
    "human": "Caucasian to varied skin tones, normal human proportions, medieval hairstyles, clean-shaven or bearded, noble bearing",
    "orc": "Green skin (Thrall-green to dark olive), tusks from lower jaw, heavy brow, broad nose, muscular, amber/red eyes, tribal scars",
    "night_elf": "Purple/blue skin, long pointed ears (very long), silver/white/green hair, glowing silver eyes (no pupils), tall angular features, ancient and serene",
    "dwarf": "Short and stocky, ruddy complexion, enormous beards (braided), broad nose, small eyes, weather-beaten, miners tan",
    "gnome": "Very small, large heads relative to body, big eyes, big ears, wild hair (pink/green/white), jovial expression, goggles optional",
    "troll": "Blue/teal skin, long pointed ears, two large tusks (upper jaw), long nose, wild hair often in mohawk, lanky, tribal piercings, three-fingered hands",
    "tauren": "Bovine humanoid, large bull-like head, horns, fur-covered, large nose ring, mane, massive build, gentle wise eyes despite size",
    "forsaken": "Undead human, visible bones/jaw, glowing yellow eyes, grey/green decayed skin, patchy hair, gaunt, torn flesh showing ribs",
    "blood_elf": "Pale golden skin, long pointed ears (shorter than night elf), glowing green/golden eyes, angular beautiful features, ornate hairstyles",
    "draenei": "Blue/purple skin, face tentacles (male: chin tendrils), horns curving back, hooves (not visible in bust), glowing blue eyes, otherworldly",
    "goblin": "Small green-skinned, very large pointed ears, long nose, beady clever eyes, sharp teeth, gold earrings, scheming expression",
    "worgen": "Wolf-human hybrid: lupine snout, fangs, fur, pointed ears, glowing amber eyes. OR human form: pale, Victorian, haunted"
  }
}
```

---

### 4.5 ICÔNES DE RETINUES (Unités spéciales)

```json
{
  "meta": {
    "model_version": "nano-banana-2-pro",
    "task_type": "retinue_icon",
    "project": "GOA_HEROES_OF_AZEROTH",
    "asset_id": "RET_GARDE_KORKRON",
    "scene_intent": "Icône de retinue CK2 : silhouette d'un guerrier Kor'kron orc d'élite en armure noire."
  },
  "scene_graph": {
    "style_bible": {
      "usp_core": [
        "CK2 retinue icon: single soldier emblem style",
        "Warcraft unit aesthetic for the given race",
        "Readable at small size, iconic silhouette"
      ],
      "look": "CK2 military unit icon, heraldic emblem style, single warrior figure, painterly, dark background",
      "palette": ["#1a1a1a", "#8b0000", "#2f2f2f", "#c0c0c0", "#ff4500"]
    },
    "subject": {
      "unit": "Single Kor'kron Elite Guard orc warrior in full black plate armor. Massive spiked shoulders, dark steel faceplate, dual war axes. Horde insignia on chest. Red eyes glowing through helmet visor. Intimidating frontal stance.",
      "race": "orc",
      "type": "heavy_infantry_elite"
    },
    "camera": {
      "shot_type": "frontal full body, slight heroic low angle",
      "composition": "figure centered, fills 80% of frame vertically"
    },
    "lighting": {
      "key": "dramatic rim light from behind",
      "accent": "red glow from eyes and Horde insignia",
      "fx": "dark atmospheric smoke at feet"
    }
  },
  "parameters": {
    "aspect_ratio": "1:1",
    "render_resolution": "512x512",
    "output_count": 2,
    "seed": -1,
    "steps": 40,
    "guidance_strength": 8.0,
    "sharpness": 0.5,
    "film_grain": 0.0
  },
  "constraints": {
    "must_include": [
      "single warrior figure",
      "race-appropriate armor and weapons",
      "iconic readable silhouette",
      "dark background"
    ],
    "must_not_include": [
      "multiple figures",
      "text",
      "busy background",
      "modern elements"
    ]
  }
}
```

---

### 4.6 LOADING SCREENS

```json
{
  "meta": {
    "model_version": "nano-banana-2-pro",
    "task_type": "loading_screen",
    "project": "GOA_HEROES_OF_AZEROTH",
    "asset_id": "LOAD_ORGRIMMAR_PANORAMA",
    "scene_intent": "Ecran de chargement : vue panoramique d'Orgrimmar au coucher du soleil."
  },
  "scene_graph": {
    "style_bible": {
      "usp_core": [
        "Warcraft cinematic concept art quality",
        "CK2 loading screen composition: wide panoramic, dramatic",
        "Must look stunning at 1920x1080"
      ],
      "look": "ultra detailed digital matte painting, Warcraft cinematic concept art, dramatic panoramic vista, 4K quality",
      "palette": ["#ff4500", "#ff8c00", "#8b4513", "#2f1810", "#ffd700"]
    },
    "environment": {
      "space": "Panoramic view of Orgrimmar at golden hour sunset. The massive orcish capital city built into red desert canyon walls. Spiked metal towers and wooden bridges span the chasm. The Valley of Strength bustling below. Grommash Hold visible on the highest point. Horde banners everywhere. Dust and heat haze. Durotar desert stretching to the horizon.",
      "atmosphere": "epic, proud, warm, vast",
      "scale_cues": [
        "tiny figures on bridges for massive scale",
        "wyvern riders in the sky",
        "dust storms on the distant horizon"
      ]
    },
    "camera": {
      "shot_type": "wide panoramic establishing shot",
      "lens": "16mm ultra-wide",
      "composition": "rule of thirds, city fills middle band, dramatic sky upper third, canyon floor lower third"
    },
    "lighting": {
      "key": "golden hour sunset from right",
      "accent": "forge fires and torch lights within the city",
      "fx": "volumetric dust, heat shimmer, lens flare from sun, god rays through canyon gaps"
    }
  },
  "parameters": {
    "aspect_ratio": "16:9",
    "render_resolution": "4096x2304",
    "output_count": 2,
    "seed": -1,
    "steps": 70,
    "guidance_strength": 8.5,
    "sharpness": 0.4,
    "film_grain": 0.06
  },
  "constraints": {
    "must_include": [
      "panoramic city view",
      "Warcraft orcish architecture",
      "dramatic sky",
      "sense of massive scale"
    ],
    "must_not_include": [
      "text or watermarks",
      "modern buildings",
      "UI elements",
      "close-up characters"
    ]
  }
}
```

---

## 5. Fichier .gfx d'intégration

Chaque asset généré doit être déclaré dans un fichier `.gfx` :

```
# interface/hoa_event_pictures.gfx
spriteTypes = {
    # Event Pictures (460x300)
    spriteType = {
        name = "GFX_evt_hoa_shadowfang_keep"
        texturefile = "gfx/interface/event_pictures/hoa_shadowfang_keep.dds"
        noOfFrames = 1
    }
    spriteType = {
        name = "GFX_evt_hoa_molten_core"
        texturefile = "gfx/interface/event_pictures/hoa_molten_core.dds"
        noOfFrames = 1
    }
    spriteType = {
        name = "GFX_evt_hoa_ragnaros"
        texturefile = "gfx/interface/event_pictures/hoa_ragnaros.dds"
        noOfFrames = 1
    }
    # ... etc pour chaque image
}
```

```
# interface/hoa_inventory_icons.gfx
spriteTypes = {
    # Inventory Icons (80x80)
    spriteType = {
        name = "GFX_hoa_inv_sword_ashkandi"
        texturefile = "gfx/interface/inventory/hoa_inv_sword_ashkandi.dds"
        noOfFrames = 1
    }
    # ... etc
}
```

```
# interface/hoa_building_icons.gfx
spriteTypes = {
    # Building Icons (48x48)
    spriteType = {
        name = "GFX_hoa_bldg_guilde_enchanteurs"
        texturefile = "gfx/interface/buildings/hoa_bldg_guilde_enchanteurs.dds"
        noOfFrames = 1
    }
    # ... etc
}
```

---

## 6. Post-traitement et Conversion

### 6.1 Pipeline de conversion PNG → DDS

```python
#!/usr/bin/env python3
"""Pipeline de conversion des assets générés par IA vers format CK2 DDS"""

import os
import subprocess
from PIL import Image

# Tailles cibles par type d'asset
ASSET_SIZES = {
    "event_picture": (460, 300),
    "inventory_icon": (80, 80),
    "building_icon": (48, 48),
    "trait_icon": (29, 29),
    "retinue_icon": (80, 80),
    "loading_screen": (1920, 1080),
    "portrait_base": (256, 400),
    "mod_thumbnail": (200, 50),
}

# Compression DDS par type
DDS_COMPRESSION = {
    "event_picture": "dxt1",      # Pas besoin d'alpha
    "inventory_icon": "dxt5",     # Alpha pour transparence
    "building_icon": "dxt5",      # Alpha
    "trait_icon": "dxt5",         # Alpha
    "retinue_icon": "dxt5",       # Alpha
    "loading_screen": "dxt1",     # Pas d'alpha
    "portrait_base": "dxt5",      # Alpha crucial pour layers
    "mod_thumbnail": "dxt1",      # Pas d'alpha
}

def process_asset(input_png, asset_type, output_dir):
    """Redimensionne et convertit un PNG en DDS pour CK2"""
    target_size = ASSET_SIZES[asset_type]
    compression = DDS_COMPRESSION[asset_type]

    # 1. Ouvrir et redimensionner
    img = Image.open(input_png)
    img = img.resize(target_size, Image.LANCZOS)

    # 2. Sauvegarder en TGA temporaire (meilleure compatibilité DDS)
    temp_tga = input_png.replace(".png", ".tga")
    img.save(temp_tga)

    # 3. Convertir en DDS via ImageMagick ou nvcompress
    output_dds = os.path.join(output_dir,
        os.path.basename(input_png).replace(".png", ".dds"))

    # Option A: ImageMagick
    subprocess.run([
        "convert", temp_tga,
        "-define", f"dds:compression={compression}",
        output_dds
    ])

    # Option B: nvcompress (NVIDIA, meilleure qualité)
    # subprocess.run(["nvcompress", "-bc3" if compression == "dxt5" else "-bc1", temp_tga, output_dds])

    os.remove(temp_tga)
    return output_dds
```

### 6.2 Script de batch generation via Replicate

```python
#!/usr/bin/env python3
"""Batch generation d'assets via Replicate API"""

import replicate
import json
import os
import requests

def generate_from_json_prompt(prompt_json, output_dir):
    """Genere un asset depuis un prompt JSON structuré"""

    # Extraire les parametres
    params = prompt_json["parameters"]
    scene = prompt_json["scene_graph"]

    # Construire le prompt texte depuis le JSON structuré
    text_prompt = build_text_prompt(scene)
    negative = " ".join(prompt_json["constraints"]["must_not_include"])

    # Appel API
    output = replicate.run(
        "nano-banana-2-pro",  # ou le modele exact sur Replicate
        input={
            "prompt": text_prompt,
            "negative_prompt": negative,
            "width": int(params["render_resolution"].split("x")[0]),
            "height": int(params["render_resolution"].split("x")[1]),
            "num_inference_steps": params["steps"],
            "guidance_scale": params["guidance_strength"],
            "seed": params.get("seed", -1),
            "num_outputs": params.get("output_count", 1),
        }
    )

    # Telecharger les resultats
    asset_id = prompt_json["meta"]["asset_id"]
    for i, url in enumerate(output):
        img_data = requests.get(url).content
        path = os.path.join(output_dir, f"{asset_id}_{i}.png")
        with open(path, "wb") as f:
            f.write(img_data)
        print(f"Saved: {path}")

def build_text_prompt(scene):
    """Convertit le scene_graph JSON en prompt texte optimisé"""
    parts = []

    # Style
    parts.append(scene["style_bible"]["look"])

    # Scene/Sujet
    if "environment" in scene:
        parts.append(scene["environment"]["space"])
        if "atmosphere" in scene["environment"]:
            parts.append(f"atmosphere: {scene['environment']['atmosphere']}")
    if "subject" in scene:
        for key in ["item", "building", "unit"]:
            if key in scene["subject"]:
                parts.append(scene["subject"][key])

    # Eclairage
    if "lighting" in scene:
        parts.append(f"lighting: {scene['lighting']['key']}")
        if "fx" in scene["lighting"]:
            parts.append(scene["lighting"]["fx"])

    # Camera
    if "camera" in scene:
        parts.append(f"composition: {scene['camera']['composition']}")

    # Palette
    if "palette" in scene["style_bible"]:
        colors = ", ".join(scene["style_bible"]["palette"])
        parts.append(f"color palette: {colors}")

    return ". ".join(parts)
```

---

## 7. Estimation des coûts

### Replicate API (prix approximatifs)

| Modèle | Prix/image | Images nécessaires | Coût estimé |
|--------|-----------|-------------------|-------------|
| Nano Banana Pro | ~$0.01-0.05 | ~290 x 3 variantes = 870 | $8.70 - $43.50 |
| SDXL (alternative) | ~$0.005-0.02 | ~870 | $4.35 - $17.40 |
| Flux Pro (haut de gamme) | ~$0.05-0.10 | ~870 | $43.50 - $87.00 |

**Budget recommandé : $20-50 pour une génération complète avec variantes.**

### Temps estimé

| Phase | Durée |
|-------|-------|
| Préparation des prompts JSON | 2-3h |
| Génération IA (batch) | 1-2h |
| Sélection des meilleurs résultats | 1-2h |
| Post-traitement et conversion DDS | 30min (automatisé) |
| Intégration .gfx et test in-game | 2-3h |
| **Total** | **~8-12h** |

---

## 8. Résumé des Priorités

```
PRIORITÉ 1 (Impact visuel maximum) :
├── 25 event pictures (donjons + raids) - Le joueur les voit constamment
├── 30 icônes d'armures T0/T0.5/T1/T2 - Loot principal
└── 20 icônes d'armes - Loot principal

PRIORITÉ 2 (Amélioration notable) :
├── 45 icônes bâtiments raciaux - Visible dans la gestion
├── 35 icônes bâtiments magiques - Visible dans la gestion
├── 36 icônes retinues - Visible dans l'armée
└── 15 icônes bijoux - Loot secondaire

PRIORITÉ 3 (Polish) :
├── Portraits layers par race - Très complexe, beaucoup de layers
├── 5 loading screens - Beau mais optionnel
├── 20 icônes de traits - Petits, peu visibles
└── 2 mod thumbnails - Cosmétique
```
