#!/usr/bin/env python3
"""
CK2 Save File Parser - MCP Server
===================================
Exposes CK2 save file data as MCP tools for Claude Agent SDK.

This server parses CK2 save files (plaintext format) and provides
structured data about the game state to AI agents.

Usage as MCP server:
    In Claude Agent SDK config:
    mcp_servers = {
        "ck2_parser": {
            "command": "python",
            "args": ["tools/mcp_servers/ck2_parser.py"]
        }
    }

Usage standalone:
    python tools/mcp_servers/ck2_parser.py parse <save_file>
    python tools/mcp_servers/ck2_parser.py analyze <save_file>
"""

import json
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict

# ---------------------------------------------------------------------------
# CK2 Save File Parser
# ---------------------------------------------------------------------------

GOA_CLASSES = [
    "warrior", "mage", "paladin", "rogue", "hunter",
    "shaman", "priest", "warlock", "druid", "death_knight", "monk",
]

GOA_RACES = [
    "human", "orc", "nightelf", "dwarf", "gnome", "troll", "tauren",
    "undead", "bloodelf", "draenei", "goblin", "worgen", "pandaren",
    "highelf", "voidelf", "nightborne", "zandalari", "maghar",
    "darkiron", "kultiran", "vulpera", "mechagnome",
]

HOA_TIER_FLAGS = [
    "t1_warrior", "t1_mage", "t1_paladin", "t1_rogue", "t1_hunter", "t1_shaman",
    "t2_warrior", "t2_mage",
]

HOA_MODIFIERS = [
    "hoa_ragnaros_slayer", "hoa_nefarian_slayer", "hoa_kelthuzad_slayer",
    "hoa_champion_of_honor", "hoa_weapon_enchanted", "hoa_defensive_pact_active",
    "hoa_wise_mentor", "hoa_trade_summit_bonus",
]


@dataclass
class CK2Character:
    char_id: int = 0
    name: str = ""
    dynasty: str = ""
    birth_date: str = ""
    age: int = 0
    is_female: bool = False
    culture: str = ""
    religion: str = ""
    traits: list = field(default_factory=list)
    # Stats
    martial: int = 0
    diplomacy: int = 0
    stewardship: int = 0
    intrigue: int = 0
    learning: int = 0
    health: float = 0.0
    wealth: float = 0.0
    prestige: float = 0.0
    piety: float = 0.0
    # GoA specific
    goa_class: str = ""
    goa_class_level: int = 0
    goa_race: str = ""
    # Artifacts
    artifacts: list = field(default_factory=list)
    tier_sets: list = field(default_factory=list)
    hoa_modifiers: list = field(default_factory=list)
    # Relations
    known_enemies: list = field(default_factory=list)
    allies: list = field(default_factory=list)
    # Title
    primary_title: str = ""
    realm_size: int = 0


@dataclass
class CK2GameState:
    date: str = ""
    player_id: int = 0
    player: CK2Character = field(default_factory=CK2Character)
    total_characters: int = 0
    independent_rulers: int = 0
    wars_active: int = 0


def parse_save_file(save_path: str) -> CK2GameState:
    """Parse a CK2 save file and extract game state.

    CK2 saves use a Clausewitz engine format:
        key=value
        key={ nested content }
    """
    path = Path(save_path)
    if not path.exists():
        raise FileNotFoundError(f"Save file not found: {save_path}")

    content = path.read_text(encoding="latin-1", errors="replace")
    state = CK2GameState()

    # Extract date
    date_match = re.search(r'^date="?(\d+\.\d+\.\d+)"?', content, re.MULTILINE)
    if date_match:
        state.date = date_match.group(1)

    # Extract player ID
    player_match = re.search(r'player=\{[^}]*id=(\d+)', content)
    if player_match:
        state.player_id = int(player_match.group(1))

    # Count characters (rough estimate)
    state.total_characters = content.count("\n\tbirth_name=")

    # Count wars
    state.wars_active = content.count("\nactive_war={")

    # Parse player character
    if state.player_id > 0:
        state.player = _parse_character(content, state.player_id)

    return state


def _parse_character(content: str, char_id: int) -> CK2Character:
    """Parse a single character block from save content"""
    char = CK2Character(char_id=char_id)

    # Find character block: \n<id>={
    pattern = rf'\n{char_id}=\{{'
    match = re.search(pattern, content)
    if not match:
        return char

    # Extract block (simplified - finds matching brace)
    start = match.start()
    block = _extract_block(content, start + len(str(char_id)) + 2)

    # Name
    name_match = re.search(r'birth_name="([^"]+)"', block)
    if name_match:
        char.name = name_match.group(1)

    # Dynasty
    dyn_match = re.search(r'dynasty=(\d+)', block)
    if dyn_match:
        char.dynasty = dyn_match.group(1)

    # Culture
    culture_match = re.search(r'culture="?(\w+)"?', block)
    if culture_match:
        char.culture = culture_match.group(1)

    # Religion
    religion_match = re.search(r'religion="?(\w+)"?', block)
    if religion_match:
        char.religion = religion_match.group(1)

    # Stats (base + modifiers)
    for stat in ["martial", "diplomacy", "stewardship", "intrigue", "learning"]:
        stat_match = re.search(rf'{stat}=(\d+)', block)
        if stat_match:
            setattr(char, stat, int(stat_match.group(1)))

    # Health
    health_match = re.search(r'health=([\d.]+)', block)
    if health_match:
        char.health = float(health_match.group(1))

    # Wealth
    wealth_match = re.search(r'wealth=([\d.-]+)', block)
    if wealth_match:
        char.wealth = float(wealth_match.group(1))

    # Prestige
    prestige_match = re.search(r'prestige=([\d.-]+)', block)
    if prestige_match:
        char.prestige = float(prestige_match.group(1))

    # Piety
    piety_match = re.search(r'piety=([\d.-]+)', block)
    if piety_match:
        char.piety = float(piety_match.group(1))

    # Traits
    traits_match = re.search(r'traits=\{([^}]+)\}', block)
    if traits_match:
        trait_ids = traits_match.group(1).strip().split()
        char.traits = trait_ids

    # GoA class detection from trait names in the block
    for cls in GOA_CLASSES:
        for level in range(10, 0, -1):
            trait_name = f"class_{cls}_{level}"
            if trait_name in block:
                char.goa_class = cls
                char.goa_class_level = level
                break
        if char.goa_class:
            break

    # GoA race detection
    for race in GOA_RACES:
        if f"creature_{race}" in block:
            char.goa_race = race
            break

    # HoA modifiers
    for mod in HOA_MODIFIERS:
        if mod in block:
            char.hoa_modifiers.append(mod)

    # HoA tier sets
    for tier_flag in HOA_TIER_FLAGS:
        if f"hoa_{tier_flag}_earned" in block:
            char.tier_sets.append(tier_flag)

    # Primary title
    title_match = re.search(r'primary=\{[^}]*title="([^"]+)"', block)
    if title_match:
        char.primary_title = title_match.group(1)

    return char


def _extract_block(content: str, start: int, max_depth: int = 50000) -> str:
    """Extract a balanced brace block from content"""
    depth = 1
    i = start
    while i < len(content) and i < start + max_depth and depth > 0:
        if content[i] == "{":
            depth += 1
        elif content[i] == "}":
            depth -= 1
        i += 1
    return content[start:i]


# ---------------------------------------------------------------------------
# Strategic Analyzer
# ---------------------------------------------------------------------------

def analyze_strategic_situation(state: CK2GameState) -> dict:
    """Analyze the player's strategic situation for AI Game Master"""
    player = state.player
    analysis = {
        "ruler": {
            "name": player.name,
            "class": f"{player.goa_class} (Level {player.goa_class_level})" if player.goa_class else "None",
            "race": player.goa_race or "Unknown",
            "power_level": _calculate_power_level(player),
        },
        "stats": {
            "martial": player.martial,
            "diplomacy": player.diplomacy,
            "stewardship": player.stewardship,
            "intrigue": player.intrigue,
            "learning": player.learning,
            "health": player.health,
            "wealth": player.wealth,
            "prestige": player.prestige,
        },
        "equipment": {
            "tier_sets_owned": player.tier_sets,
            "active_modifiers": player.hoa_modifiers,
            "boss_kills": [m for m in player.hoa_modifiers if "slayer" in m],
        },
        "recommendations": _generate_recommendations(player),
        "raid_readiness": _check_raid_readiness(player),
    }
    return analysis


def _calculate_power_level(char: CK2Character) -> str:
    """Calculate overall power level rating"""
    score = char.martial * 2 + char.goa_class_level * 5 + len(char.tier_sets) * 10
    score += len([m for m in char.hoa_modifiers if "slayer" in m]) * 15

    if score >= 80:
        return "Legendary"
    elif score >= 60:
        return "Epic"
    elif score >= 40:
        return "Rare"
    elif score >= 20:
        return "Uncommon"
    return "Common"


def _check_raid_readiness(char: CK2Character) -> dict:
    """Check which raids the character can attempt"""
    readiness = {}

    # Molten Core: martial >= 10
    mc_ready = char.martial >= 10 and char.goa_class != ""
    readiness["molten_core"] = {
        "ready": mc_ready,
        "requirements": "martial >= 10, any class",
        "missing": [] if mc_ready else [
            f"martial {char.martial}/10" if char.martial < 10 else None,
            "no class" if not char.goa_class else None,
        ],
    }
    readiness["molten_core"]["missing"] = [
        m for m in readiness["molten_core"]["missing"] if m
    ]

    # Blackwing Lair: martial >= 14, has T1
    has_t1 = any("t1_" in t for t in char.tier_sets)
    bwl_ready = char.martial >= 14 and has_t1
    readiness["blackwing_lair"] = {
        "ready": bwl_ready,
        "requirements": "martial >= 14, T1 tier set",
        "missing": [] if bwl_ready else [
            f"martial {char.martial}/14" if char.martial < 14 else None,
            "no T1 set" if not has_t1 else None,
        ],
    }
    readiness["blackwing_lair"]["missing"] = [
        m for m in readiness["blackwing_lair"]["missing"] if m
    ]

    # Naxxramas: martial >= 16, learning >= 12, has T2
    has_t2 = any("t2_" in t for t in char.tier_sets)
    naxx_ready = char.martial >= 16 and char.learning >= 12 and has_t2
    readiness["naxxramas"] = {
        "ready": naxx_ready,
        "requirements": "martial >= 16, learning >= 12, T2 tier set",
        "missing": [] if naxx_ready else [
            f"martial {char.martial}/16" if char.martial < 16 else None,
            f"learning {char.learning}/12" if char.learning < 12 else None,
            "no T2 set" if not has_t2 else None,
        ],
    }
    readiness["naxxramas"]["missing"] = [
        m for m in readiness["naxxramas"]["missing"] if m
    ]

    return readiness


def _generate_recommendations(char: CK2Character) -> list:
    """Generate strategic recommendations"""
    recs = []

    # Crafting recommendation
    if char.wealth >= 100 and not char.tier_sets:
        recs.append({
            "type": "crafting",
            "priority": "HIGH",
            "action": "Forge uncommon equipment (100g) to prepare for raids",
        })

    if char.wealth >= 300 and char.martial >= 12:
        recs.append({
            "type": "crafting",
            "priority": "MEDIUM",
            "action": "Forge rare equipment (300g) for significant power boost",
        })

    # Raid recommendation
    if char.martial >= 10 and char.goa_class and not any("t1_" in t for t in char.tier_sets):
        recs.append({
            "type": "raid",
            "priority": "HIGH",
            "action": "Attempt Molten Core for T1 tier set pieces",
        })

    if any("t1_" in t for t in char.tier_sets) and char.martial >= 14:
        recs.append({
            "type": "raid",
            "priority": "HIGH",
            "action": "Attempt Blackwing Lair for T2 tier set upgrade",
        })

    # Diplomacy recommendation
    if char.diplomacy >= 10 and char.prestige >= 200:
        recs.append({
            "type": "diplomacy",
            "priority": "MEDIUM",
            "action": "Form defensive pact with neighbors (+30 opinion, +10% garrison)",
        })

    if char.wealth >= 50 and char.diplomacy >= 8:
        recs.append({
            "type": "diplomacy",
            "priority": "LOW",
            "action": "Send emissary to improve relations (+15 opinion with neighbors)",
        })

    # Enchanting recommendation
    if char.goa_class in ["mage", "warlock", "priest", "druid", "shaman"]:
        if char.learning >= 10 and char.wealth >= 200:
            if "hoa_weapon_enchanted" not in char.hoa_modifiers:
                recs.append({
                    "type": "enchanting",
                    "priority": "HIGH",
                    "action": "Enchant weapon (+5 CR, +1 martial for 10 years)",
                })

    if not recs:
        recs.append({
            "type": "general",
            "priority": "LOW",
            "action": "Build up martial and wealth before attempting content",
        })

    return recs


# ---------------------------------------------------------------------------
# MCP Server Protocol
# ---------------------------------------------------------------------------

class MCPServer:
    """Minimal MCP server implementation for stdio transport"""

    def __init__(self):
        self.tools = {
            "parse_save": {
                "description": "Parse a CK2 save file and return game state",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "save_path": {
                            "type": "string",
                            "description": "Path to the CK2 save file",
                        }
                    },
                    "required": ["save_path"],
                },
            },
            "analyze_strategy": {
                "description": "Analyze player's strategic situation from a CK2 save",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "save_path": {
                            "type": "string",
                            "description": "Path to the CK2 save file",
                        }
                    },
                    "required": ["save_path"],
                },
            },
            "check_raid_readiness": {
                "description": "Check which raids the player can attempt",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "save_path": {
                            "type": "string",
                            "description": "Path to the CK2 save file",
                        }
                    },
                    "required": ["save_path"],
                },
            },
            "get_recommendations": {
                "description": "Get AI-powered strategic recommendations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "save_path": {
                            "type": "string",
                            "description": "Path to the CK2 save file",
                        }
                    },
                    "required": ["save_path"],
                },
            },
        }

    def handle_request(self, request: dict) -> dict:
        """Handle a JSON-RPC request"""
        method = request.get("method", "")
        params = request.get("params", {})
        req_id = request.get("id")

        if method == "initialize":
            return self._response(req_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {
                    "name": "ck2-goa-parser",
                    "version": "1.0.0",
                },
            })

        elif method == "tools/list":
            tools_list = [
                {"name": name, **info} for name, info in self.tools.items()
            ]
            return self._response(req_id, {"tools": tools_list})

        elif method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            return self._handle_tool_call(req_id, tool_name, arguments)

        elif method == "notifications/initialized":
            return None  # No response needed for notifications

        return self._error(req_id, -32601, f"Unknown method: {method}")

    def _handle_tool_call(self, req_id, tool_name: str, arguments: dict) -> dict:
        """Execute a tool and return results"""
        save_path = arguments.get("save_path", "")

        try:
            if tool_name == "parse_save":
                state = parse_save_file(save_path)
                result = asdict(state)

            elif tool_name == "analyze_strategy":
                state = parse_save_file(save_path)
                result = analyze_strategic_situation(state)

            elif tool_name == "check_raid_readiness":
                state = parse_save_file(save_path)
                analysis = analyze_strategic_situation(state)
                result = analysis["raid_readiness"]

            elif tool_name == "get_recommendations":
                state = parse_save_file(save_path)
                analysis = analyze_strategic_situation(state)
                result = {
                    "recommendations": analysis["recommendations"],
                    "power_level": analysis["ruler"]["power_level"],
                }

            else:
                return self._error(req_id, -32602, f"Unknown tool: {tool_name}")

            return self._response(req_id, {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
            })

        except FileNotFoundError as e:
            return self._error(req_id, -32602, str(e))
        except Exception as e:
            return self._error(req_id, -32603, f"Parse error: {e}")

    def _response(self, req_id, result: dict) -> dict:
        return {"jsonrpc": "2.0", "id": req_id, "result": result}

    def _error(self, req_id, code: int, message: str) -> dict:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}

    def run_stdio(self):
        """Run as MCP server over stdio"""
        import select

        sys.stderr.write("CK2 GoA Parser MCP Server started\n")

        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
                response = self.handle_request(request)
                if response is not None:
                    sys.stdout.write(json.dumps(response) + "\n")
                    sys.stdout.flush()
            except json.JSONDecodeError:
                error = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error"},
                }
                sys.stdout.write(json.dumps(error) + "\n")
                sys.stdout.flush()


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ck2_parser.py serve          - Run as MCP server")
        print("  python ck2_parser.py parse <save>    - Parse save file")
        print("  python ck2_parser.py analyze <save>  - Strategic analysis")
        return

    command = sys.argv[1]

    if command == "serve":
        server = MCPServer()
        server.run_stdio()

    elif command == "parse" and len(sys.argv) >= 3:
        state = parse_save_file(sys.argv[2])
        print(json.dumps(asdict(state), indent=2))

    elif command == "analyze" and len(sys.argv) >= 3:
        state = parse_save_file(sys.argv[2])
        analysis = analyze_strategic_situation(state)
        print(json.dumps(analysis, indent=2))

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
