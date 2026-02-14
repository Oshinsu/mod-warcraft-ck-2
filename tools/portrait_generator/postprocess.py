#!/usr/bin/env python3
"""
Post-Processing Pipeline for CK2 Portrait Sprites
===================================================
Takes raw AI-generated images and processes them into CK2-compatible
sprite sheets:

1. Background removal (alpha mask generation)
2. Center crop to portrait frame (176x176)
3. Color correction / consistency pass
4. Horizontal sprite sheet assembly
5. DDS DXT5 conversion (if tools available)

Usage:
    python postprocess.py --race human --layer male_base
    python postprocess.py --race all
    python postprocess.py --install-deps  # Install required packages
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path

try:
    from PIL import Image, ImageFilter, ImageEnhance, ImageOps
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
MOD_DIR = PROJECT_ROOT / "GoA_Heroes_of_Azeroth"
GFX_CHARS_DIR = MOD_DIR / "gfx" / "characters"
RAW_DIR = SCRIPT_DIR / "output"
PROCESSED_DIR = SCRIPT_DIR / "processed"

FRAME_W = 176
FRAME_H = 176

# CK2 portrait color palette - slightly desaturated, painterly
CK2_STYLE = {
    "saturation": 0.85,     # Slightly desaturated
    "contrast": 1.10,       # Slight contrast boost
    "brightness": 0.95,     # Slightly dark (CK2 portraits are dim)
    "sharpness": 1.3,       # Crisp details
    "warmth": 1.02,         # Very slight warm tint
}


def remove_background(img: Image.Image, threshold: int = 30) -> Image.Image:
    """Simple background removal: darken near-black pixels to transparent."""
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    for pixel in data:
        r, g, b, a = pixel
        # If pixel is very dark (background), make transparent
        if r < threshold and g < threshold and b < threshold:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(pixel)
    img.putdata(new_data)
    return img


def apply_ck2_style(img: Image.Image) -> Image.Image:
    """Apply CK2 portrait art style adjustments."""
    # Saturation
    enhancer = ImageEnhance.Color(img.convert("RGB"))
    rgb = enhancer.enhance(CK2_STYLE["saturation"])

    # Contrast
    enhancer = ImageEnhance.Contrast(rgb)
    rgb = enhancer.enhance(CK2_STYLE["contrast"])

    # Brightness
    enhancer = ImageEnhance.Brightness(rgb)
    rgb = enhancer.enhance(CK2_STYLE["brightness"])

    # Sharpness
    enhancer = ImageEnhance.Sharpness(rgb)
    rgb = enhancer.enhance(CK2_STYLE["sharpness"])

    # Recombine with original alpha
    if img.mode == "RGBA":
        rgb = rgb.convert("RGBA")
        r, g, b, _ = rgb.split()
        _, _, _, a = img.split()
        return Image.merge("RGBA", (r, g, b, a))
    return rgb


def center_crop_portrait(img: Image.Image, target_w: int = FRAME_W,
                         target_h: int = FRAME_H) -> Image.Image:
    """Smart center crop for portrait: focus on upper-center (face area)."""
    w, h = img.size

    # For portrait: crop to square first, biased toward top (face)
    if w != h:
        crop_size = min(w, h)
        left = (w - crop_size) // 2
        # Bias top by 10% for face-centric crop
        top_bias = int(h * 0.05)
        top = max(0, (h - crop_size) // 2 - top_bias)
        img = img.crop((left, top, left + crop_size, top + crop_size))

    # Resize to target
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    return img


def process_frame(input_path: Path, output_path: Path,
                  layer_type: str = "base") -> bool:
    """Process a single frame: bg removal, crop, style, save."""
    if not input_path.exists():
        return False

    img = Image.open(input_path).convert("RGBA")

    # Background removal (for non-base layers)
    if layer_type in ("hair", "beard", "clothes", "headgear"):
        img = remove_background(img, threshold=25)

    # Center crop to CK2 frame size
    img = center_crop_portrait(img)

    # Apply CK2 art style
    img = apply_ck2_style(img)

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), "PNG")
    return True


def assemble_sprite_sheet(frame_dir: Path, layer_name: str,
                          num_frames: int, output_path: Path) -> bool:
    """Assemble processed frames into a horizontal sprite sheet."""
    frames = []
    for i in range(num_frames):
        frame_path = frame_dir / f"{layer_name}_v{i:02d}.png"
        if frame_path.exists():
            frames.append(Image.open(frame_path).convert("RGBA"))
        else:
            # Transparent placeholder
            frames.append(Image.new("RGBA", (FRAME_W, FRAME_H), (0, 0, 0, 0)))

    sheet = Image.new("RGBA", (FRAME_W * len(frames), FRAME_H), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        sheet.paste(frame, (i * FRAME_W, 0))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(str(output_path), "PNG")
    print(f"  Sheet: {output_path.name} ({FRAME_W * len(frames)}x{FRAME_H})")
    return True


def convert_png_to_dds(png_path: Path) -> bool:
    """Convert PNG to DDS DXT5."""
    dds_path = png_path.with_suffix(".dds")

    # Try ImageMagick
    try:
        r = subprocess.run(
            ["convert", str(png_path), "-define", "dds:compression=dxt5",
             str(dds_path)],
            capture_output=True, timeout=30
        )
        if r.returncode == 0:
            print(f"  DDS: {dds_path.name}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Try nvcompress
    try:
        r = subprocess.run(
            ["nvcompress", "-bc3", str(png_path), str(dds_path)],
            capture_output=True, timeout=30
        )
        if r.returncode == 0:
            print(f"  DDS: {dds_path.name}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    print(f"  No DDS converter. PNG kept: {png_path.name}")
    return False


def process_race(race_id: str, layers: list = None):
    """Process all layers for a race."""
    import json

    with open(SCRIPT_DIR / "portrait_prompts.json") as f:
        prompts = json.load(f)

    if race_id not in prompts["races"]:
        print(f"ERROR: Unknown race '{race_id}'")
        return

    race = prompts["races"][race_id]
    if layers is None:
        layers = list(race["layers"].keys())

    print(f"\n{'='*60}")
    print(f"Post-processing: {race_id}")
    print(f"{'='*60}")

    for layer_name in layers:
        if layer_name not in race["layers"]:
            continue

        layer_def = race["layers"][layer_name]
        gender = "female" if layer_name.startswith("female") else "male"

        # Detect layer type
        layer_type = "base"
        for lt in ("hair", "beard", "clothes", "headgear", "base"):
            if lt in layer_name:
                layer_type = lt
                break

        num_frames = layer_def.get("variants", 6)
        raw_dir = RAW_DIR / race_id / gender
        proc_dir = PROCESSED_DIR / race_id / gender
        ck2_dir = GFX_CHARS_DIR / race_id / gender

        print(f"\n  Layer: {layer_name} ({num_frames} frames, type={layer_type})")

        # Process each frame
        processed = 0
        for i in range(num_frames):
            raw_frame = raw_dir / f"{layer_name}_v{i:02d}.png"
            proc_frame = proc_dir / f"{layer_name}_v{i:02d}.png"

            if raw_frame.exists():
                if process_frame(raw_frame, proc_frame, layer_type):
                    processed += 1

        print(f"    Processed: {processed}/{num_frames} frames")

        if processed > 0:
            # Assemble sprite sheet
            sheet_name = f"hoa_{race_id}_{layer_name}.png"
            sheet_path = ck2_dir / sheet_name
            assemble_sprite_sheet(proc_dir, layer_name, num_frames, sheet_path)

            # Convert to DDS
            convert_png_to_dds(sheet_path)


def check_dependencies():
    """Check and report on available tools."""
    print("Dependency Check:")
    print(f"  Python PIL/Pillow: {'OK' if HAS_PIL else 'MISSING (pip install Pillow)'}")

    # ImageMagick
    try:
        r = subprocess.run(["convert", "--version"], capture_output=True, timeout=5)
        print(f"  ImageMagick:       OK ({r.stdout.decode().split(chr(10))[0][:50]})")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print(f"  ImageMagick:       MISSING (apt install imagemagick)")

    # nvcompress
    try:
        r = subprocess.run(["nvcompress", "--help"], capture_output=True, timeout=5)
        print(f"  nvcompress:        OK")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print(f"  nvcompress:        MISSING (optional, ImageMagick is sufficient)")

    # Replicate
    try:
        import replicate
        print(f"  replicate:         OK")
    except ImportError:
        print(f"  replicate:         MISSING (pip install replicate)")

    # Check REPLICATE_API_TOKEN
    token = os.environ.get("REPLICATE_API_TOKEN", "")
    if token:
        print(f"  API Token:         SET ({token[:8]}...)")
    else:
        print(f"  API Token:         NOT SET (export REPLICATE_API_TOKEN=r8_...)")


def main():
    parser = argparse.ArgumentParser(description="CK2 Portrait Post-Processor")
    parser.add_argument("--race", type=str, help="Race to process (or 'all')")
    parser.add_argument("--layer", type=str, nargs="*", help="Layers to process")
    parser.add_argument("--check", action="store_true", help="Check dependencies")
    parser.add_argument("--install-deps", action="store_true",
                        help="Install Python dependencies")

    args = parser.parse_args()

    if args.check:
        check_dependencies()
        return

    if args.install_deps:
        subprocess.run([sys.executable, "-m", "pip", "install",
                        "Pillow", "replicate"])
        return

    if not HAS_PIL:
        print("ERROR: Pillow required. Run: pip install Pillow")
        return

    if not args.race:
        parser.print_help()
        return

    import json
    with open(SCRIPT_DIR / "portrait_prompts.json") as f:
        prompts = json.load(f)

    if args.race == "all":
        races = list(prompts["races"].keys())
    else:
        races = [args.race]

    for race_id in races:
        process_race(race_id, args.layer)


if __name__ == "__main__":
    main()
