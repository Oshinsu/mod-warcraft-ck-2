#!/usr/bin/env python3
"""
Batch 2: Generate remaining weapon + armor icons directly.
Writes JSON prompts AND generates in one pass.
"""

import json, os, time, requests

API_TOKEN = os.environ.get("REPLICATE_API_TOKEN", "")
API_URL = "https://api.replicate.com/v1/models/google/nano-banana-pro/predictions"
REPO = "/home/user/mod-warcraft-ck-2"
INV_DIR = f"{REPO}/GoA_Heroes_of_Azeroth/gfx/interface/inventory"
PROMPTS_DIR = f"{REPO}/tools/prompts"

os.makedirs(INV_DIR, exist_ok=True)
os.makedirs(f"{PROMPTS_DIR}/inventory_weapons", exist_ok=True)
os.makedirs(f"{PROMPTS_DIR}/inventory_armor", exist_ok=True)

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "Prefer": "wait",
}

# Quality glow reference:
# common=#9d9d9d, uncommon=#1eff00, rare=#0070dd, epic=#a335ee, legendary=#ff8000

WEAPONS = [
    # (asset_id, prompt, category_file)
    ("hoa_inv_staff_epic", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background with vignette. An ornate arcane mage staff with a large pulsing purple crystal orb at the top, held by twisted silver branches growing from the shaft. Ancient rune-carved dark wooden shaft with gold bands and arcane symbols. Purple arcane energy swirling around the crystal, trailing magical particles. Purple epic quality (#a335ee) aura glow surrounding the weapon. Vertical orientation, slightly angled. Rich painterly brushwork, metallic reflections on silver, deep crystal transparency. No hands, no characters, single item only, clean dark background, readable silhouette at 80x80 pixels.", "06_staff_epic"),
    ("hoa_inv_staff_legendary", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background with vignette. Atiesh, Greatstaff of the Guardian — a tall elegant staff topped with a raven perched on a crescent moon made of pure shimmering arcane energy. The raven is detailed with iridescent black feathers, eyes glowing blue. Staff shaft is ancient polished dark wood with arcane runes spiraling along its entire length, emitting faint blue light. Intense orange legendary quality (#ff8000) glow radiating outward, stardust and magical particles swirling. Vertical orientation. Immense ancient arcane authority. No hands, single item, dark background, readable at 80x80.", "07_staff_legendary"),
    ("hoa_inv_bow_epic", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background with vignette. A magnificent ancient elven longbow carved from enchanted silverwood with intricate silver leaf and vine motifs inlaid along both limbs. Glowing blue magical bowstring of pure condensed arcane energy, taut and humming with power. Nature runes carved along the limbs emit soft green light. Small emerald gems set at the grip and limb tips. Purple epic quality (#a335ee) glow with green nature wisps. Diagonal orientation. Elegant, deadly, ancient. No hands, no arrows, single item, dark background, readable at 80x80.", "08_bow_epic"),
    ("hoa_inv_dagger_epic", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background with vignette. A sinister curved assassin's dagger with a blade forged from blackened shadow-steel, the edge dripping viscous green poison that glows faintly. Skull-shaped pommel with two tiny ruby eyes that gleam. Serrated back edge for extra brutality. The blade is slightly translucent, dark smoke wisping from its surface. Dark leather and wire wrapped grip. Purple epic quality (#a335ee) shadow glow with green poison drips. Diagonal orientation. Small, lethal, venomous. No hands, single item, dark background, readable at 80x80.", "09_dagger_epic"),
    ("hoa_inv_mace_epic", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background with vignette. A grand holy paladin warhammer with a massive golden hammer head engraved with symbols of the Holy Light — radiant suns, laurel wreaths, sacred geometry. The striking surface emanates white-golden holy radiance. Silver shaft reinforced with gold bands, blue leather grip wrapped at the handle. Alliance lion motif on the pommel in polished gold. Purple epic quality (#a335ee) border glow mixed with divine golden-white holy light rays. Diagonal orientation. Righteous, heavy, blessed. No hands, single item, dark background, readable at 80x80.", "10_mace_epic"),
    ("hoa_inv_axe_epic", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background with vignette. A brutal orcish double-headed battle axe with massive dark iron crescent blades etched with tribal Horde engravings and war glyphs. Two red gems set at the junction of blade and haft, glowing with inner fire. Bloodstained cutting edges showing recent battle. Thick wooden haft wrapped in leather strips and adorned with bone fetishes, animal teeth, and red war paint. Purple epic quality (#a335ee) glow with crimson red accents. Diagonal orientation. Savage, imposing, tribal. No hands, single item, dark background, readable at 80x80.", "11_axe_epic"),
    ("hoa_inv_mace_legendary", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background with vignette. Sulfuras, Hand of Ragnaros — a colossal flaming warhammer of mythic power. The hammer head is forged from living magma and dark iron, its surface a churning mix of solidified black volcanic rock cracking open to reveal blindingly bright molten orange-yellow magma beneath. Eternal flames wreath the striking surface, with concentric rings of fire energy orbiting the head. The haft is dark iron wrapped in fiery chains that glow red-hot. Lava drips and ember particles trail from the weapon. Intense orange legendary quality (#ff8000) fire glow radiating massively. Diagonal orientation. The weapon of a Fire God. No hands, single item, dark background, readable at 80x80.", "12_mace_legendary"),
]

ARMOR = [
    ("hoa_inv_helm_paladin_t1", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. Paladin Tier 1 Lawbringer Helm — a noble full plate helmet in polished silver and gold. Prominent golden cross symbol on the forehead, emanating faint holy light. White cloth drape hanging from the back of the helm. Narrow eye slits with soft golden-white glow within suggesting divine vision. Clean crusader aesthetic, ceremonial yet battle-ready. Blue rare quality (#0070dd) divine glow. Front-facing view centered in frame. No person wearing it, single item, dark background.", "05_helm_paladin_t1"),
    ("hoa_inv_helm_paladin_t2", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. Paladin Tier 2 Judgement Crown — THE iconic WoW paladin helmet. A magnificent golden crowned helm with sweeping crimson red feathered wings extending from the sides. Red and gold color scheme with exquisite filigree. Holy radiance beaming from within the eye slits and from the crown points. The most recognizable paladin helmet in World of Warcraft. Majestic, awe-inspiring, divine authority. Purple epic quality (#a335ee) glow mixed with brilliant holy golden-white light. Front-facing view. No person, single item, dark background.", "06_helm_paladin_t2"),
    ("hoa_inv_helm_rogue_t1", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. Rogue Tier 1 Nightslayer Hood — a dark leather cowl with an integrated face mask covering the lower face. Only shadowed eyes visible through a narrow slit, suggesting danger lurking in darkness. Dark purple and black soft leather with subtle silver buckle closures on the side. The fabric seems to absorb light. Stealthy, menacing, silent death. Blue rare quality (#0070dd) subtle shadow glow. Front-facing view. No person, single item, dark background.", "07_helm_rogue_t1"),
    ("hoa_inv_helm_rogue_t2", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. Rogue Tier 2 Bloodfang Hood — a sinister angular red and black leather mask with sharp predatory features. Two glowing red lens-like eye pieces that gleam with malicious intelligence. Bat-wing shaped ear covers extending upward. Dark red leather with black trim and tiny metal studs. The mask projects an aura of calculated lethality. Predatory, lethal, feared. Purple epic quality (#a335ee) shadow glow with red accents from eye lenses. Front-facing view. No person, single item, dark background.", "08_helm_rogue_t2"),
    ("hoa_inv_helm_hunter_t1", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. Hunter Tier 1 Giantstalker Helm — a rugged wilderness mail coif with a beast skull serving as a visor and forehead guard. Small antler-like decorations branching from the sides. Nature-themed with leaf and vine motifs worked into the chainmail. Brown and forest green color scheme with leather straps. The look of a master tracker and beast-slayer. Blue rare quality (#0070dd) natural green-tinted glow. Front-facing view. No person, single item, dark background.", "09_helm_hunter_t1"),
    ("hoa_inv_helm_hunter_t2", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. Hunter Tier 2 Dragonstalker Helm — a dramatic mail helmet shaped like a dragon's head with swept-back horns curving elegantly. Green dragon scales covering the surface with gold trim along every edge. Dragon eye gems on the brow ridge glowing with inner green fire. The helm channels the power of the Green Dragonflight. Dragonslayer, predator of legends. Purple epic quality (#a335ee) glow with green dragon fire wisps emanating from the eye gems. Front-facing view. No person, single item, dark background.", "10_helm_hunter_t2"),
    ("hoa_inv_helm_priest_t1", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. Priest Tier 1 Vestments of Prophecy circlet — a delicate golden circlet with a central brilliant white diamond that radiates pure holy light outward in soft rays. White and gold cloth head wrapping flowing from the sides. Serene, holy, prophetic. The circlet seems to glow with inner divine warmth. Blue rare quality (#0070dd) soft divine glow. Front-facing view. No person, single item, dark background.", "11_helm_priest_t1"),
    ("hoa_inv_helm_priest_t2", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. Priest Tier 2 Transcendence Crown — an ornate golden tiara with a glowing halo-like golden disc hovering behind the head, emitting divine radiance in all directions. White and gold with sacred holy symbols engraved. Divine light streams outward from the halo as visible rays. Angelic, transcendent, ultimate spiritual authority. Purple epic quality (#a335ee) glow mixed with overwhelming holy white-gold light emanating from the halo. Front-facing view. No person, single item, dark background.", "12_helm_priest_t2"),
    ("hoa_inv_helm_warlock_t1", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. Warlock Tier 1 Felheart Hood — a dark purple cloth hood with two small demonic horn-like protrusions growing from the top. Sickly green fel energy glowing from within the hood's depths, casting eerie green shadows on the fabric. Dark purple and green color scheme. Sinister demonic runes embroidered on the fabric in thread that glows faintly. Dark magic practitioner, servant of demons. Blue rare quality (#0070dd) with green fel undertone glow. Front-facing view. No person, single item, dark background.", "13_helm_warlock_t1"),
    ("hoa_inv_helm_warlock_t2", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. Warlock Tier 2 Nemesis Crown — a terrifying dark iron crown bristling with multiple curving demon horns of varying heights. Green fel fire blazing between and above the horns like a demonic bonfire. Shadow energy wreathing the base. Dark iron and shadow metal construction. Green and purple color scheme. Pure concentrated demonic power made manifest. Purple epic quality (#a335ee) glow with intense green fel energy streams rising from between the horns. Front-facing view. No person, single item, dark background.", "14_helm_warlock_t2"),
    ("hoa_inv_helm_druid_t1", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. Druid Tier 1 Cenarion Helm — a living wooden helm shaped like a wise owl's face with large round amber eye lenses that glow with nature magic. The surface is actual bark texture with small green leaves and moss growing naturally from it. Two antler-like branches extend upward from the crown, still alive with tiny buds. Earthy, ancient, natural wisdom. Blue rare quality (#0070dd) warm nature green glow from the amber eyes. Front-facing view. No person, single item, dark background.", "15_helm_druid_t1"),
    ("hoa_inv_helm_druid_t2", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. Druid Tier 2 Stormrage Cover — a majestic antlered helm of living wood and moonstone. Massive branching antlers reaching skyward, each tine tipped with a tiny glowing moonstone bead. The helm is living dark bark adorned with silver leaf filigree. Central moonstone gem on the brow radiating silver lunar energy. Inspired by Malfurion Stormrage. Commanding nature presence, ancient druidic power. Purple epic quality (#a335ee) glow with silver moonlight aura radiating from moonstones. Front-facing view. No person, single item, dark background.", "16_helm_druid_t2"),
    ("hoa_inv_helm_shaman_t1", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. Shaman Tier 1 Earthfury Helm — a rugged totem-styled helmet constructed from dark leather, bone plates, and small elemental crystals. A lightning bolt motif etched into the brow guard. Feathers (eagle, hawk) and bone beads hanging from leather cords on the sides. Earth-toned brown and storm-blue color scheme. Spiritual warrior who communes with the elements. Blue rare quality (#0070dd) elemental glow with tiny lightning sparks dancing around the brow. Front-facing view. No person, single item, dark background.", "17_helm_shaman_t1"),
    ("hoa_inv_helm_shaman_t2", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. Shaman Tier 2 Ten Storms Helm — a dramatic elemental crown embodying the fury of storms. Dark blue and silver metalwork with thundercloud and lightning motifs sculpted into the metal. Multiple crystal points on the crown with CRACKLING LIGHTNING electricity arcing between them constantly. A miniature thunderstorm swirling above the crown. Blue and silver with intense electric blue-white accents. Master of all elements, storm incarnate. Purple epic quality (#a335ee) glow with electric blue-white storm energy crackling and arcing. Front-facing view. No person, single item, dark background.", "18_helm_shaman_t2"),
    ("hoa_inv_chest_warrior_epic", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. Warrior Tier 2 Wrath chestpiece — a heavy plate warrior breastplate of blue-tinted steel with ornate gold filigree trim running along every edge and seam. A dragon motif embossed in gold relief on the center chest. Shoulder attachment rivets visible at the top. Belt buckle with a lion Alliance crest at the waist. The steel has a cold blue sheen reflecting light. Heroic, heavy, commanding. Purple epic quality (#a335ee) glow with steel-blue reflections. Front-facing flat display as if on a mannequin. No person wearing it, single item, dark background.", "19_chest_warrior_epic"),
    ("hoa_inv_chest_mage_epic", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. An ornate arcane mage robe — deep purple silk and silver thread with golden trim at collar, cuffs, and hem. Arcane runes woven directly into the fabric glow with soft blue-white light, the text of power visible in the cloth itself. High mandarin collar, flowing bell sleeves. Crystal clasps at the front in silver settings. The fabric seems to shimmer and shift with contained magical energy. Scholarly, powerful, elegant. Purple epic quality (#a335ee) magical glow with blue arcane rune light visible in the fabric. Front-facing flat display. No person wearing it, single item, dark background.", "20_chest_mage_epic"),
    ("hoa_inv_shield_epic", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. A massive Alliance tower shield of polished steel and gold. The front face bears a magnificent golden lion emblem in high relief — the Alliance crest — on a field of deep blue enamel. Silver rivets line the entire border. The lion emblem radiates faint holy light. Battle damage: scratches and dents adding character without diminishing grandeur. Heavy, defensive, the wall between order and chaos. Purple epic quality (#a335ee) glow with holy golden accents from the lion emblem. Front-facing view, slight angle to show depth and curvature. No hands, single item, dark background.", "21_shield_epic"),
    ("hoa_inv_ring_epic", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. A powerful magical ring made of intertwined gold and mithril silver bands. A large brilliant-cut deep purple amethyst gemstone set in an ornate raised bezel, emitting visible arcane light rays and small floating magical particles. Ancient microscopic runes engraved inside the band, barely visible. The gem seems to contain a swirling miniature galaxy within. Ancient, powerful, mysterious artifact. Purple epic quality (#a335ee) arcane aura radiating from the gem. Centered composition at slight angle to show the band's roundness. No fingers, single item, dark background.", "22_ring_epic"),
    ("hoa_inv_necklace_epic", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. An ornate magical amulet on a fine gold chain with small gemstone accents. The central pendant is a teardrop-shaped deep blue sapphire cradled by silver dragon claws. Arcane energy wisps emanating from the gem like ethereal smoke. The chain is delicately crafted with tiny link details. The sapphire pulses with inner blue-white light. Elegant, ancient, imbued with draconic power. Purple epic quality (#a335ee) glow around the pendant. Centered composition. No neck, single item, dark background.", "23_necklace_epic"),
    ("hoa_inv_trinket_epic", "World of Warcraft inventory icon, hand-painted game asset style, single item centered on dark gradient background. A mysterious ancient trinket — a palm-sized golden mechanical device that combines gnomish clockwork precision with raw arcane crystal power. Tiny visible rune-etched brass gears mesh perfectly around a central pulsing arcane crystal core that glows violet-blue. The device seems to be perpetually in motion, gears turning, crystal humming. Gnomish engineering meets high arcane magic. Enigmatic, complex, powerful. Purple epic quality (#a335ee) glow pulsing from the crystal core. Centered composition. Small compact object, dark background.", "24_trinket_epic"),
]

def generate(asset_id, prompt, aspect="1:1"):
    path = f"{INV_DIR}/{asset_id}.png"
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        print(f"  [SKIP] {asset_id}")
        return "skip"

    print(f"  [GEN]  {asset_id}...", end="", flush=True)
    try:
        resp = requests.post(API_URL, headers=HEADERS, json={
            "input": {"prompt": prompt, "aspect_ratio": aspect, "output_format": "png"}
        }, timeout=300)
        result = resp.json()
        output = result.get("output", "")
        if isinstance(output, list):
            output = output[0] if output else ""
        if not output:
            print(f" FAIL: {result.get('error','no output')}")
            return "fail"
        img = requests.get(output, timeout=60)
        with open(path, "wb") as f:
            f.write(img.content)
        print(f" OK ({os.path.getsize(path)/1024/1024:.1f}MB)")
        return "ok"
    except Exception as e:
        print(f" FAIL: {e}")
        return "fail"

def save_prompt(asset_id, prompt, category, filename):
    """Save a minimal but valid JSON prompt for reference."""
    data = {
        "meta": {
            "model": "google/nano-banana-pro",
            "asset_id": asset_id,
            "target_path": f"GoA_Heroes_of_Azeroth/gfx/interface/inventory/{asset_id}.png",
        },
        "parameters": {"aspect_ratio": "1:1", "output_format": "png"},
        "prompt_construction": {"positive": prompt, "negative": "text, watermark, signature, UI, modern, anime, cartoon, photorealistic face, blurry, low quality, multiple items, busy background, person wearing item, hands holding item"}
    }
    outdir = f"{PROMPTS_DIR}/{category}"
    os.makedirs(outdir, exist_ok=True)
    with open(f"{outdir}/{filename}.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    stats = {"ok": 0, "fail": 0, "skip": 0}

    print("=" * 60)
    print("  Batch 2: Remaining Weapons & Armor")
    print("=" * 60)

    print(f"\n--- Weapons ({len(WEAPONS)} items) ---")
    for asset_id, prompt, fname in WEAPONS:
        save_prompt(asset_id, prompt, "inventory_weapons", fname)
        r = generate(asset_id, prompt)
        stats[r] += 1
        if r == "ok":
            time.sleep(1)

    print(f"\n--- Armor ({len(ARMOR)} items) ---")
    for asset_id, prompt, fname in ARMOR:
        save_prompt(asset_id, prompt, "inventory_armor", fname)
        r = generate(asset_id, prompt)
        stats[r] += 1
        if r == "ok":
            time.sleep(1)

    print(f"\n{'='*60}")
    print(f"  DONE: {stats['ok']} ok / {stats['fail']} fail / {stats['skip']} skip")
    print(f"{'='*60}")
