#!/usr/bin/env python3
"""
GoA Agent Mod Generator
========================
Uses Claude Agent SDK to generate complete CK2 mod content for
Warcraft: Guardians of Azeroth.

Requires: pip install claude-agent-sdk anthropic

Usage:
    python tools/goa_agent_generator.py raid "Karazhan" "Prince Malchezaar" 8
    python tools/goa_agent_generator.py tier-set "T3" "Naxxramas" warrior mage paladin rogue
    python tools/goa_agent_generator.py decision "recruit_champion" "Recruit a legendary champion"
    python tools/goa_agent_generator.py balance-check
    python tools/goa_agent_generator.py localize events/hoa_dungeon_events.txt
"""

import asyncio
import argparse
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MOD_DIR = PROJECT_ROOT / "GoA_Heroes_of_Azeroth"
SKILLS_DIR = PROJECT_ROOT / ".claude" / "skills"

CLAUDE_MODEL = os.environ.get("GOA_MODEL", "claude-sonnet-4-5-20250929")

# ---------------------------------------------------------------------------
# Skill Loader
# ---------------------------------------------------------------------------

def load_skill(skill_name: str) -> str:
    """Load a skill file from .claude/skills/"""
    skill_path = SKILLS_DIR / f"{skill_name}.md"
    if skill_path.exists():
        return skill_path.read_text()
    return ""


def load_claude_md() -> str:
    """Load project CLAUDE.md context"""
    claude_md = PROJECT_ROOT / "CLAUDE.md"
    if claude_md.exists():
        return claude_md.read_text()
    return ""


def build_system_prompt(*skill_names: str) -> str:
    """Build system prompt from CLAUDE.md + skills"""
    parts = [load_claude_md()]
    for name in skill_names:
        skill = load_skill(name)
        if skill:
            parts.append(f"\n---\n{skill}")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Raid Generator
# ---------------------------------------------------------------------------

RAID_PROMPT_TEMPLATE = """Generate a COMPLETE CK2 GoA dungeon raid for:

**Raid Name**: {raid_name}
**Final Boss**: {boss_name}
**Difficulty**: {difficulty}/10
**Lore**: {lore}
**Tier Set Level**: {tier}
**Classes with tier sets**: {classes}

Generate ALL of the following files. Output each file with a clear header
showing the exact file path.

### Required Files:

1. **events/hoa_{raid_id}_events.txt**
   - Namespace: hoa_{raid_id}
   - Event launcher (hoa_{raid_id}.1) with entry requirements
   - Boss outcome event (hoa_{raid_id}.10) with 4 tiers
   - Class-specific T{tier_num} loot drops on great success
   - Scale costs/rewards with difficulty level

2. **common/artifacts/hoa_{raid_id}_tier_sets.txt**
   - T{tier_num} set pieces for: {classes}
   - Each class gets crown + torso (minimum)
   - Quality based on tier level
   - Class-appropriate stats (see artifact designer skill)
   - Proper activation conditions with class triggers

3. **common/event_modifiers/hoa_{raid_id}_modifiers.txt**
   - Boss kill title modifier (permanent, scales with difficulty)
   - Raid cooldown modifier (hidden)
   - Any unique buff modifiers

4. **localisation/hoa_{raid_id}.csv**
   - All event descriptions, option texts, tooltips
   - 4 languages: EN, FR, DE, ES
   - Full EN/FR, abbreviated DE/ES

Follow the balance guidelines exactly. Harder raids = higher costs, lower
success rates, better loot. Reference existing raids (MC difficulty 5,
BWL difficulty 7, Naxx difficulty 9) for calibration.
"""

RAID_LORE = {
    "aq40": {
        "name": "Temple of Ahn'Qiraj",
        "boss": "C'Thun, the Old God",
        "difficulty": 8,
        "tier": "T2.5",
        "tier_num": 2,
        "lore": (
            "The ancient temple of Ahn'Qiraj in the deserts of Silithus houses "
            "the Old God C'Thun, a being of unfathomable evil. The Qiraji armies "
            "swarm beneath the sands, preparing for war against all mortal races. "
            "Only the combined might of Horde and Alliance opened the Gates of "
            "Ahn'Qiraj. Within, C'Thun's eye watches all who dare enter."
        ),
    },
    "karazhan": {
        "name": "Karazhan",
        "boss": "Prince Malchezaar, the Eredar Lord",
        "difficulty": 7,
        "tier": "T4",
        "tier_num": 4,
        "lore": (
            "Karazhan, the ivory tower of Medivh, last Guardian of Tirisfal, "
            "stands in the haunted region of Deadwind Pass. Since Medivh's death, "
            "the tower has become a nexus of dark magical energies. Ghosts of past "
            "guests haunt its halls. At the top, Prince Malchezaar, an eredar lord "
            "of the Burning Legion, has claimed the tower as his own. The Curator, "
            "Shade of Aran, and Nightbane all guard the path to the summit."
        ),
    },
    "ulduar": {
        "name": "Ulduar",
        "boss": "Yogg-Saron, the God of Death",
        "difficulty": 9,
        "tier": "T8",
        "tier_num": 8,
        "lore": (
            "Ulduar is a titan-forged city in the Storm Peaks of Northrend, built "
            "to serve as the prison of the Old God Yogg-Saron. The Keepers of "
            "Ulduar - Hodir, Thorim, Freya, and Mimiron - have been corrupted. "
            "Algalon the Observer watches from the Celestial Planetarium, ready "
            "to signal the titans to re-originate Azeroth if the corruption "
            "cannot be contained."
        ),
    },
    "icc": {
        "name": "Icecrown Citadel",
        "boss": "The Lich King, Arthas Menethil",
        "difficulty": 10,
        "tier": "T10",
        "tier_num": 10,
        "lore": (
            "The Icecrown Citadel towers above the frozen wastes of Northrend, "
            "the seat of the Lich King's power. Within its halls, the Scourge's "
            "greatest champions guard the Frozen Throne: Lord Marrowgar, Lady "
            "Deathwhisper, the Blood Princes, Professor Putricide, Sindragosa "
            "the frost wyrm, and finally the Lich King himself - Arthas Menethil, "
            "the fallen prince of Lordaeron. This is the final battle against "
            "the Scourge. There must always be a Lich King."
        ),
    },
}


async def generate_raid(raid_id: str, classes: list[str] | None = None):
    """Generate a complete raid using Claude Agent SDK or direct API"""
    if raid_id not in RAID_LORE:
        print(f"Unknown raid: {raid_id}")
        print(f"Available: {', '.join(RAID_LORE.keys())}")
        return

    raid = RAID_LORE[raid_id]
    if classes is None:
        classes = ["warrior", "mage", "paladin", "rogue", "hunter", "shaman"]

    system = build_system_prompt(
        "goa_event_writer", "goa_artifact_designer", "goa_localizer"
    )

    prompt = RAID_PROMPT_TEMPLATE.format(
        raid_name=raid["name"],
        boss_name=raid["boss"],
        difficulty=raid["difficulty"],
        lore=raid["lore"],
        tier=raid["tier"],
        tier_num=raid["tier_num"],
        classes=", ".join(classes),
        raid_id=raid_id,
    )

    # Try Agent SDK first, fall back to direct API
    try:
        from claude_agent_sdk import query, ClaudeAgentOptions

        print(f"[Agent SDK] Generating {raid['name']}...")
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                model=CLAUDE_MODEL,
                system_prompt=system,
                allowed_tools=["Read", "Write", "Edit", "Glob", "Grep"],
                permission_mode="acceptEdits",
                max_turns=20,
            ),
        ):
            if hasattr(message, "result"):
                print(message.result)
            elif hasattr(message, "content"):
                print(message.content)

    except ImportError:
        print("[Fallback] Agent SDK not installed, using Anthropic API directly...")
        await _generate_raid_api(raid_id, raid, classes, system, prompt)


async def _generate_raid_api(
    raid_id: str, raid: dict, classes: list, system: str, prompt: str
):
    """Fallback: generate via Anthropic Messages API and write files manually"""
    try:
        from anthropic import AsyncAnthropic
    except ImportError:
        print("ERROR: Install anthropic SDK: pip install anthropic")
        return

    client = AsyncAnthropic()

    print(f"[API] Generating {raid['name']} with {CLAUDE_MODEL}...")
    response = await client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=16000,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.content[0].text
    print(f"[API] Generated {len(content)} characters")

    # Parse file blocks from response
    files = _parse_file_blocks(content)

    for file_path, file_content in files.items():
        full_path = MOD_DIR / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(file_content)
        print(f"  [WRITE] {full_path}")

    if not files:
        # If parsing failed, dump raw output
        output_path = MOD_DIR / f"_generated_{raid_id}.txt"
        output_path.write_text(content)
        print(f"  [RAW] Output saved to {output_path}")
        print("  Note: Could not parse file blocks. Manual extraction needed.")


def _parse_file_blocks(content: str) -> dict[str, str]:
    """Parse file blocks from LLM output.

    Looks for patterns like:
        ### events/hoa_aq40_events.txt
        ```
        <content>
        ```
    Or:
        **File: events/hoa_aq40_events.txt**
        ```
        <content>
        ```
    """
    import re

    files = {}

    # Pattern 1: ### path or **path** followed by code block
    pattern = re.compile(
        r"(?:#{1,4}\s*|(?:\*\*)?(?:File:\s*)?)"
        r"((?:events|common|localisation|decisions)/[^\s*#\n]+)"
        r"[*\s]*\n"
        r"```[^\n]*\n"
        r"(.*?)"
        r"\n```",
        re.DOTALL,
    )

    for match in pattern.finditer(content):
        path = match.group(1).strip()
        body = match.group(2).strip()
        if body:
            files[path] = body + "\n"

    return files


# ---------------------------------------------------------------------------
# Balance Checker
# ---------------------------------------------------------------------------

async def check_balance():
    """Analyze all mod files for balance issues"""
    system = build_system_prompt("goa_balance_analyzer")

    # Gather all mod files
    mod_files = {}
    for ext in ("*.txt", "*.csv"):
        for f in MOD_DIR.rglob(ext):
            rel = f.relative_to(MOD_DIR)
            mod_files[str(rel)] = f.read_text()

    files_summary = "\n\n".join(
        f"=== {path} ===\n{content}" for path, content in mod_files.items()
    )

    prompt = f"""Analyze ALL of the following mod files for balance issues.

Check for:
1. Gold economy (costs vs rewards, ROI)
2. Stat inflation (per-item and total loadout)
3. Combat rating scaling
4. Cooldown exploits
5. Difficulty progression gaps
6. AI behavior issues
7. Comparison with vanilla GoA power levels

Produce a detailed balance report with a table of findings.

{files_summary}"""

    try:
        from claude_agent_sdk import query, ClaudeAgentOptions

        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                model=CLAUDE_MODEL,
                system_prompt=system,
                allowed_tools=["Read", "Glob", "Grep"],
                max_turns=10,
            ),
        ):
            if hasattr(message, "result"):
                print(message.result)
    except ImportError:
        from anthropic import AsyncAnthropic

        client = AsyncAnthropic()
        response = await client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=8000,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        print(response.content[0].text)


# ---------------------------------------------------------------------------
# Localizer
# ---------------------------------------------------------------------------

async def localize_file(file_path: str):
    """Generate or complete localization for a mod file"""
    system = build_system_prompt("goa_localizer", "goa_event_writer")

    source = Path(file_path).read_text()

    prompt = f"""Analyze this CK2 mod file and generate COMPLETE localization CSV.

Extract every localizable string key (event descs, option names, tooltips,
modifier names) and provide translations in EN, FR, DE, ES.

Source file:
```
{source}
```

Output a complete CSV file ready to save to localisation/"""

    try:
        from anthropic import AsyncAnthropic
    except ImportError:
        print("ERROR: pip install anthropic")
        return

    client = AsyncAnthropic()
    response = await client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=8000,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    print(response.content[0].text)


# ---------------------------------------------------------------------------
# Interactive Generator
# ---------------------------------------------------------------------------

async def interactive_mode():
    """Interactive prompt for generating mod content"""
    print("=" * 60)
    print("  GoA Mod Generator - Interactive Mode")
    print("  Powered by Claude Agent SDK + Opus 4.6")
    print("=" * 60)
    print()
    print("Available raids to generate:")
    for rid, rdata in RAID_LORE.items():
        print(f"  {rid:12s} - {rdata['name']} (Boss: {rdata['boss']}, Diff: {rdata['difficulty']}/10)")
    print()
    print("Commands:")
    print("  raid <id>           - Generate a full raid")
    print("  balance             - Run balance analysis")
    print("  localize <file>     - Generate localization")
    print("  quit                - Exit")
    print()

    while True:
        try:
            cmd = input("goa> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not cmd or cmd == "quit":
            break

        parts = cmd.split()

        if parts[0] == "raid" and len(parts) >= 2:
            classes = parts[2:] if len(parts) > 2 else None
            await generate_raid(parts[1], classes)
        elif parts[0] == "balance":
            await check_balance()
        elif parts[0] == "localize" and len(parts) >= 2:
            await localize_file(parts[1])
        else:
            print(f"Unknown command: {cmd}")


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="GoA Agent Mod Generator - AI-powered CK2 mod content creation"
    )
    subparsers = parser.add_subparsers(dest="command")

    # raid command
    raid_parser = subparsers.add_parser("raid", help="Generate a complete raid")
    raid_parser.add_argument("raid_id", choices=list(RAID_LORE.keys()),
                             help="Raid identifier")
    raid_parser.add_argument("--classes", nargs="+",
                             default=["warrior", "mage", "paladin", "rogue", "hunter", "shaman"],
                             help="Classes to generate tier sets for")

    # balance command
    subparsers.add_parser("balance", help="Run balance analysis on all mod files")

    # localize command
    loc_parser = subparsers.add_parser("localize", help="Generate localization for a file")
    loc_parser.add_argument("file", help="Path to the mod file to localize")

    # interactive command
    subparsers.add_parser("interactive", help="Interactive generation mode")

    # list command
    subparsers.add_parser("list", help="List available raids")

    args = parser.parse_args()

    if args.command == "raid":
        asyncio.run(generate_raid(args.raid_id, args.classes))
    elif args.command == "balance":
        asyncio.run(check_balance())
    elif args.command == "localize":
        asyncio.run(localize_file(args.file))
    elif args.command == "interactive":
        asyncio.run(interactive_mode())
    elif args.command == "list":
        for rid, rdata in RAID_LORE.items():
            print(f"  {rid:12s} - {rdata['name']} (Diff: {rdata['difficulty']}/10)")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
