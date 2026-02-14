#!/usr/bin/env python3
"""
CK2 Portrait Generator for GoA: Heroes of Azeroth
===================================================
Generates portrait layers for 5 Warcraft races using Replicate API (Flux Pro Ultra).
Outputs: individual PNGs -> sprite sheets -> DDS (with ImageMagick/nvcompress).

Usage:
    python generate_portraits.py --race human --layer male_base
    python generate_portraits.py --race all --layer all
    python generate_portraits.py --race orc --layer male_clothes --dry-run
    python generate_portraits.py --list

Requires:
    pip install replicate Pillow
    export REPLICATE_API_TOKEN=r8_...
"""

import argparse
import json
import os
import sys
import time
import subprocess
from pathlib import Path
from typing import Optional

try:
    import replicate
    HAS_REPLICATE = True
except ImportError:
    HAS_REPLICATE = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ==============================
# CONFIGURATION
# ==============================

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
MOD_DIR = PROJECT_ROOT / "GoA_Heroes_of_Azeroth"
GFX_CHARS_DIR = MOD_DIR / "gfx" / "characters"
PROMPTS_FILE = SCRIPT_DIR / "portrait_prompts.json"
OUTPUT_DIR = SCRIPT_DIR / "output"

# CK2 portrait frame dimensions
FRAME_W = 176
FRAME_H = 176

# Replicate model config
MODEL_PRIMARY = "black-forest-labs/flux-1.1-pro-ultra"
MODEL_FALLBACK = "black-forest-labs/flux-1.1-pro"

# Generation parameters per layer type
LAYER_CONFIG = {
    "base":     {"width": 1024, "height": 1024, "frames": 6, "aspect": "1:1"},
    "eyes":     {"width": 1024, "height": 512,  "frames": 6, "aspect": "2:1"},
    "hair":     {"width": 1024, "height": 1024, "frames": 8, "aspect": "1:1"},
    "beard":    {"width": 1024, "height": 1024, "frames": 6, "aspect": "1:1"},
    "clothes":  {"width": 1024, "height": 768,  "frames": 5, "aspect": "4:3"},
    "headgear": {"width": 1024, "height": 1024, "frames": 5, "aspect": "1:1"},
}

# Rate limiting
API_DELAY = 2.0  # seconds between API calls
MAX_RETRIES = 3
RETRY_DELAY = 5.0


def load_prompts() -> dict:
    """Load the prompt definitions from JSON."""
    with open(PROMPTS_FILE) as f:
        return json.load(f)


def get_layer_type(layer_name: str) -> str:
    """Extract layer type from layer name (e.g., 'male_base' -> 'base')."""
    for lt in LAYER_CONFIG:
        if layer_name.endswith(lt):
            return lt
    # Compound names
    if "clothes" in layer_name:
        return "clothes"
    if "headgear" in layer_name:
        return "headgear"
    if "base" in layer_name:
        return "base"
    if "hair" in layer_name:
        return "hair"
    if "beard" in layer_name:
        return "beard"
    return "base"


def build_prompt(prompts_data: dict, race_id: str, layer_name: str,
                 variant_idx: int) -> dict:
    """Build a complete prompt for one frame of one layer."""
    race = prompts_data["races"][race_id]
    layer_def = race["layers"][layer_name]
    style_prefix = prompts_data["style_prefix"]
    style_suffix = prompts_data["style_suffix"]
    layer_type = get_layer_type(layer_name)
    base_instructions = prompts_data["layer_instructions"].get(layer_type, "")

    prompt_template = layer_def["prompt"]

    # Substitutions
    subs = {
        "style_prefix": style_prefix,
        "style_suffix": style_suffix,
        "base_instructions": base_instructions,
    }

    # Skin tone variation
    if "vary_by" in layer_def and layer_def["vary_by"] == "skin_tones":
        tones = race.get("skin_tones", ["neutral"])
        subs["skin_tone"] = tones[variant_idx % len(tones)]

    # Eye color
    eyes = race.get("eye_colors", ["brown"])
    subs["eye_color"] = eyes[variant_idx % len(eyes)]

    # Hair color
    hair_colors = race.get("hair_colors", ["black"])
    subs["hair_color"] = hair_colors[variant_idx % len(hair_colors)]

    # Hair/beard style
    if "styles" in layer_def:
        styles = layer_def["styles"]
        subs["hair_style"] = styles[variant_idx % len(styles)]
        subs["beard_style"] = styles[variant_idx % len(styles)]

    # Rank outfit (clothes/headgear)
    rank_labels = prompts_data["_meta"]["rank_labels"]
    if "rank_outfits" in layer_def:
        rank = rank_labels[variant_idx % len(rank_labels)]
        subs["rank_outfit"] = layer_def["rank_outfits"][rank]
    if "rank_headgear" in layer_def:
        rank = rank_labels[variant_idx % len(rank_labels)]
        subs["rank_headgear"] = layer_def["rank_headgear"][rank]

    # Build final prompt
    prompt = prompt_template
    for key, val in subs.items():
        prompt = prompt.replace("{" + key + "}", str(val))

    negative = layer_def.get("negative", "")

    return {
        "prompt": prompt,
        "negative_prompt": negative,
        "race": race_id,
        "layer": layer_name,
        "variant": variant_idx,
        "layer_type": layer_type,
    }


def generate_image(prompt_data: dict, model: str = MODEL_PRIMARY,
                   dry_run: bool = False) -> Optional[str]:
    """Generate a single image via Replicate API. Returns output URL or path."""
    layer_type = prompt_data["layer_type"]
    config = LAYER_CONFIG.get(layer_type, LAYER_CONFIG["base"])

    if dry_run:
        print(f"  [DRY RUN] Would generate: {prompt_data['race']}/{prompt_data['layer']} "
              f"variant {prompt_data['variant']}")
        print(f"    Prompt ({len(prompt_data['prompt'])} chars): "
              f"{prompt_data['prompt'][:120]}...")
        return None

    if not HAS_REPLICATE:
        print("ERROR: 'replicate' package not installed. Run: pip install replicate")
        return None

    for attempt in range(MAX_RETRIES):
        try:
            print(f"  Generating {prompt_data['race']}/{prompt_data['layer']} "
                  f"v{prompt_data['variant']} (attempt {attempt + 1})...")

            input_params = {
                "prompt": prompt_data["prompt"],
                "aspect_ratio": config["aspect"],
                "output_format": "png",
                "safety_tolerance": 5,
            }

            # Flux Pro Ultra supports aspect_ratio, not width/height directly
            if "ultra" in model:
                input_params["aspect_ratio"] = config["aspect"]
            else:
                input_params["width"] = config["width"]
                input_params["height"] = config["height"]

            output = replicate.run(model, input=input_params)

            # Handle different output formats
            if isinstance(output, list):
                url = str(output[0])
            elif hasattr(output, 'url'):
                url = output.url
            else:
                url = str(output)

            time.sleep(API_DELAY)
            return url

        except Exception as e:
            print(f"    Error: {e}")
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_DELAY * (2 ** attempt)
                print(f"    Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"    FAILED after {MAX_RETRIES} attempts")
                return None


def download_image(url: str, output_path: Path) -> bool:
    """Download an image from URL to local path."""
    try:
        import urllib.request
        output_path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, str(output_path))
        return True
    except Exception as e:
        print(f"    Download error: {e}")
        return False


def create_sprite_sheet(frame_paths: list[Path], output_path: Path,
                        frame_w: int = FRAME_W, frame_h: int = FRAME_H) -> bool:
    """Combine individual frame PNGs into a horizontal sprite sheet."""
    if not HAS_PIL:
        print("ERROR: Pillow not installed. Run: pip install Pillow")
        return False

    frames = []
    for fp in frame_paths:
        if fp.exists():
            img = Image.open(fp).convert("RGBA")
            # Resize to CK2 frame size
            img = img.resize((frame_w, frame_h), Image.Resampling.LANCZOS)
            frames.append(img)
        else:
            # Create empty transparent frame
            frames.append(Image.new("RGBA", (frame_w, frame_h), (0, 0, 0, 0)))

    if not frames:
        return False

    # Create horizontal strip
    sheet_w = frame_w * len(frames)
    sheet_h = frame_h
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))

    for i, frame in enumerate(frames):
        sheet.paste(frame, (i * frame_w, 0))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(str(output_path), "PNG")
    print(f"  Sprite sheet: {output_path} ({sheet_w}x{sheet_h}, {len(frames)} frames)")
    return True


def convert_to_dds(png_path: Path, dds_path: Path) -> bool:
    """Convert PNG sprite sheet to DDS DXT5 format for CK2."""
    # Try ImageMagick first
    try:
        result = subprocess.run(
            ["convert", str(png_path), "-define", "dds:compression=dxt5",
             str(dds_path)],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print(f"  DDS (ImageMagick): {dds_path}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Try nvcompress
    try:
        result = subprocess.run(
            ["nvcompress", "-bc3", str(png_path), str(dds_path)],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print(f"  DDS (nvcompress): {dds_path}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    print(f"  WARNING: No DDS converter found. Keeping PNG: {png_path}")
    print(f"           Install ImageMagick or nvcompress for DDS output.")
    return False


def get_all_layers(prompts_data: dict, race_id: str) -> list[str]:
    """Get all layer names for a race."""
    return list(prompts_data["races"][race_id]["layers"].keys())


def get_all_races(prompts_data: dict) -> list[str]:
    """Get all race IDs."""
    return list(prompts_data["races"].keys())


def process_layer(prompts_data: dict, race_id: str, layer_name: str,
                  dry_run: bool = False, model: str = MODEL_PRIMARY,
                  skip_existing: bool = True) -> dict:
    """Generate all frames for one layer, build sprite sheet, convert to DDS."""
    race = prompts_data["races"][race_id]
    layer_def = race["layers"][layer_name]
    layer_type = get_layer_type(layer_name)
    config = LAYER_CONFIG.get(layer_type, LAYER_CONFIG["base"])
    num_frames = layer_def.get("variants", config["frames"])

    # Determine gender from layer name
    if layer_name.startswith("female"):
        gender = "female"
    else:
        gender = "male"

    # Output directories
    race_output = OUTPUT_DIR / race_id / gender
    race_output.mkdir(parents=True, exist_ok=True)

    # Final CK2 output path
    ck2_output = GFX_CHARS_DIR / race_id / gender

    print(f"\n{'='*60}")
    print(f"Processing: {race_id} / {layer_name} ({num_frames} frames)")
    print(f"{'='*60}")

    frame_paths = []
    generated = 0
    skipped = 0

    for i in range(num_frames):
        frame_path = race_output / f"{layer_name}_v{i:02d}.png"

        if skip_existing and frame_path.exists():
            print(f"  Frame {i}: exists, skipping")
            frame_paths.append(frame_path)
            skipped += 1
            continue

        prompt_data = build_prompt(prompts_data, race_id, layer_name, i)

        if dry_run:
            # Write prompt to file for review
            prompt_file = race_output / f"{layer_name}_v{i:02d}_prompt.txt"
            prompt_file.parent.mkdir(parents=True, exist_ok=True)
            with open(prompt_file, "w") as f:
                f.write(f"PROMPT:\n{prompt_data['prompt']}\n\n")
                f.write(f"NEGATIVE:\n{prompt_data['negative_prompt']}\n")
            frame_paths.append(frame_path)
            generated += 1
            continue

        url = generate_image(prompt_data, model=model, dry_run=False)
        if url:
            if download_image(url, frame_path):
                frame_paths.append(frame_path)
                generated += 1
            else:
                frame_paths.append(frame_path)  # placeholder
        else:
            frame_paths.append(frame_path)

    # Build sprite sheet
    sheet_name = f"hoa_{race_id}_{layer_name}.png"
    sheet_path = race_output / sheet_name
    ck2_sheet = ck2_output / sheet_name

    if not dry_run and any(p.exists() for p in frame_paths):
        create_sprite_sheet(frame_paths, sheet_path)
        # Copy to CK2 mod directory
        ck2_output.mkdir(parents=True, exist_ok=True)
        if sheet_path.exists():
            import shutil
            shutil.copy2(sheet_path, ck2_sheet)
            print(f"  Copied to mod: {ck2_sheet}")

        # Try DDS conversion
        dds_path = ck2_sheet.with_suffix(".dds")
        convert_to_dds(ck2_sheet, dds_path)

    return {
        "race": race_id,
        "layer": layer_name,
        "frames_generated": generated,
        "frames_skipped": skipped,
        "frames_total": num_frames,
        "sheet_path": str(sheet_path),
    }


def generate_gfx_file(prompts_data: dict, races: list[str]) -> str:
    """Generate the CK2 .gfx portrait definition file content."""
    lines = ['spriteTypes = {', '']

    for race_id in races:
        race = prompts_data["races"][race_id]
        gfx_culture = race["gfx_culture"]
        lines.append(f'\t# === {race_id.upper()} ({gfx_culture}) ===')

        for layer_name in race["layers"]:
            layer_type = get_layer_type(layer_name)
            config = LAYER_CONFIG.get(layer_type, LAYER_CONFIG["base"])
            gender = "male" if "male" in layer_name else "female"
            layer_def = race["layers"][layer_name]
            num_frames = layer_def.get("variants", config["frames"])

            gfx_name = f"GFX_hoa_{race_id}_{layer_name}"
            # Use PNG as primary (DDS if converted)
            tex_path = f"gfx/characters/{race_id}/{gender}/hoa_{race_id}_{layer_name}.png"

            lines.append(f'\tspriteType = {{')
            lines.append(f'\t\tname = "{gfx_name}"')
            lines.append(f'\t\ttexturefile = "{tex_path}"')
            lines.append(f'\t\tnoOfFrames = {num_frames}')
            lines.append(f'\t}}')

        lines.append('')

    lines.append('}')
    return '\n'.join(lines)


def generate_portrait_types(prompts_data: dict, races: list[str]) -> str:
    """Generate portraitType definitions for CK2."""
    lines = ['# =====================================================',
             '# GoA: Heroes of Azeroth - Portrait Type Definitions',
             '# =====================================================',
             '# Generated by portrait_generator. Do not edit manually.',
             '# =====================================================',
             '', 'spriteTypes = {', '']

    for race_id in races:
        race = prompts_data["races"][race_id]
        gfx = race["gfx_culture"]
        prefix = f"hoa_{race_id}"

        for gender in ["male", "female"]:
            pt_name = f"PORTRAIT_{gfx}_{gender}"
            lines.append(f'\tportraitType = {{')
            lines.append(f'\t\tname = "{pt_name}"')
            lines.append(f'\t\teffectFile = "gfx/FX/portrait.lua"')
            lines.append(f'')

            # Layer stack (bottom to top)
            layers = [
                f'"GFX_{prefix}_{gender}_clothes:p3:c0"',       # clothes behind
                f'"GFX_{prefix}_{gender}_base:p2"',              # face base
            ]

            # Hair and beard
            layers.append(f'"GFX_{prefix}_{gender}_hair:d5:h"')
            if gender == "male":
                layers.append(f'"GFX_{prefix}_{gender}_beard:d6"')

            # Clothes and headgear on top
            layers.append(f'"GFX_{prefix}_{gender}_clothes:p3:c1"')
            layers.append(f'"GFX_{prefix}_{gender}_headgear:p3"')

            lines.append(f'\t\tlayer = {{')
            for layer in layers:
                lines.append(f'\t\t\t{layer}')
            lines.append(f'\t\t}}')
            lines.append(f'')
            lines.append(f'\t\thair_color_index = 8')
            lines.append(f'\t\teye_color_index = 9')
            lines.append(f'\t}}')
            lines.append(f'')

    lines.append('}')
    return '\n'.join(lines)


def print_generation_plan(prompts_data: dict, races: list[str],
                          layers: Optional[list[str]] = None):
    """Print what would be generated without doing it."""
    total_images = 0
    total_cost_estimate = 0.0
    cost_per_image = 0.04  # Flux Pro Ultra estimate

    print("\n" + "=" * 70)
    print("GENERATION PLAN")
    print("=" * 70)

    for race_id in races:
        race = prompts_data["races"][race_id]
        race_layers = layers or list(race["layers"].keys())

        print(f"\n  Race: {race_id} ({race['description'][:60]}...)")
        race_images = 0

        for layer_name in race_layers:
            if layer_name not in race["layers"]:
                continue
            layer_def = race["layers"][layer_name]
            layer_type = get_layer_type(layer_name)
            config = LAYER_CONFIG.get(layer_type, LAYER_CONFIG["base"])
            num = layer_def.get("variants", config["frames"])
            race_images += num
            print(f"    {layer_name:30s} {num:3d} frames  "
                  f"({config['width']}x{config['height']})")

        total_images += race_images
        print(f"    {'':30s} --- ")
        print(f"    {'Subtotal':30s} {race_images:3d} images")

    total_cost_estimate = total_images * cost_per_image
    print(f"\n{'=' * 70}")
    print(f"  TOTAL: {total_images} images")
    print(f"  Estimated API cost: ${total_cost_estimate:.2f}")
    print(f"  Estimated time: {total_images * 8}s "
          f"(~{total_images * 8 / 60:.0f} min)")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"{'=' * 70}")


def main():
    parser = argparse.ArgumentParser(
        description="CK2 Portrait Generator for GoA: Heroes of Azeroth",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list                         Show all races and layers
  %(prog)s --plan                         Show generation plan with cost estimate
  %(prog)s --race human --layer male_base Generate human male base portraits
  %(prog)s --race orc --layer all         Generate all orc layers
  %(prog)s --race all --layer all         Generate EVERYTHING
  %(prog)s --race human --dry-run         Write prompts to files without API calls
  %(prog)s --gfx-only                     Generate GFX/portraitType files only
        """
    )

    parser.add_argument("--race", type=str, default=None,
                        help="Race to generate (human/orc/nightelf/bloodelf/troll/all)")
    parser.add_argument("--layer", type=str, default=None,
                        help="Layer to generate (male_base/female_hair/etc/all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Write prompts to files without calling API")
    parser.add_argument("--list", action="store_true",
                        help="List all races and layers")
    parser.add_argument("--plan", action="store_true",
                        help="Show generation plan with cost estimate")
    parser.add_argument("--model", type=str, default=MODEL_PRIMARY,
                        help=f"Replicate model (default: {MODEL_PRIMARY})")
    parser.add_argument("--skip-existing", action="store_true", default=True,
                        help="Skip frames that already exist")
    parser.add_argument("--gfx-only", action="store_true",
                        help="Only generate GFX definition files")
    parser.add_argument("--output-dir", type=str, default=None,
                        help="Override output directory")

    args = parser.parse_args()

    # Load prompts
    prompts_data = load_prompts()

    if args.output_dir:
        global OUTPUT_DIR
        OUTPUT_DIR = Path(args.output_dir)

    # List mode
    if args.list:
        print("\nAvailable races and layers:")
        for race_id, race in prompts_data["races"].items():
            print(f"\n  {race_id} ({race['gfx_culture']}):")
            for layer_name, layer_def in race["layers"].items():
                lt = get_layer_type(layer_name)
                n = layer_def.get("variants", LAYER_CONFIG.get(lt, {}).get("frames", 6))
                print(f"    {layer_name:30s} {n:3d} frames")
        return

    # Plan mode
    if args.plan:
        races = get_all_races(prompts_data) if args.race in (None, "all") \
            else [args.race]
        print_generation_plan(prompts_data, races)
        return

    # GFX-only mode
    if args.gfx_only:
        races = get_all_races(prompts_data)
        # Sprite GFX
        gfx_content = generate_gfx_file(prompts_data, races)
        gfx_path = MOD_DIR / "interface" / "portraits" / "hoa_portrait_sprites.gfx"
        gfx_path.parent.mkdir(parents=True, exist_ok=True)
        with open(gfx_path, "w") as f:
            f.write(gfx_content)
        print(f"Written: {gfx_path}")

        # Portrait types
        pt_content = generate_portrait_types(prompts_data, races)
        pt_path = MOD_DIR / "interface" / "portraits" / "hoa_portrait_types.gfx"
        with open(pt_path, "w") as f:
            f.write(pt_content)
        print(f"Written: {pt_path}")
        return

    # Generation mode
    if not args.race:
        parser.print_help()
        return

    races = get_all_races(prompts_data) if args.race == "all" else [args.race]

    if args.race != "all" and args.race not in prompts_data["races"]:
        print(f"ERROR: Unknown race '{args.race}'. "
              f"Available: {', '.join(get_all_races(prompts_data))}")
        return

    results = []
    for race_id in races:
        if args.layer and args.layer != "all":
            layer_list = [args.layer]
        else:
            layer_list = get_all_layers(prompts_data, race_id)

        for layer_name in layer_list:
            if layer_name not in prompts_data["races"][race_id]["layers"]:
                print(f"WARNING: Layer '{layer_name}' not found for race '{race_id}'")
                continue

            result = process_layer(
                prompts_data, race_id, layer_name,
                dry_run=args.dry_run,
                model=args.model,
                skip_existing=args.skip_existing,
            )
            results.append(result)

    # Generate GFX files after generation
    if not args.dry_run:
        print("\n\nGenerating GFX definition files...")
        gfx_content = generate_gfx_file(prompts_data, races)
        gfx_path = MOD_DIR / "interface" / "portraits" / "hoa_portrait_sprites.gfx"
        gfx_path.parent.mkdir(parents=True, exist_ok=True)
        with open(gfx_path, "w") as f:
            f.write(gfx_content)
        print(f"Written: {gfx_path}")

    # Summary
    print("\n" + "=" * 60)
    print("GENERATION SUMMARY")
    print("=" * 60)
    total_gen = sum(r["frames_generated"] for r in results)
    total_skip = sum(r["frames_skipped"] for r in results)
    total_all = sum(r["frames_total"] for r in results)
    print(f"  Generated: {total_gen}")
    print(f"  Skipped:   {total_skip}")
    print(f"  Total:     {total_all}")
    if args.dry_run:
        print(f"\n  Prompts written to: {OUTPUT_DIR}")
        print(f"  Review prompts, then run without --dry-run to generate.")


if __name__ == "__main__":
    main()
