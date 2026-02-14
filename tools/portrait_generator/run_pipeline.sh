#!/bin/bash
# =====================================================
# CK2 Portrait Generation Pipeline
# GoA: Heroes of Azeroth
# =====================================================
#
# Full pipeline: Generate -> Post-process -> Sprite Sheet -> DDS
#
# Prerequisites:
#   pip install replicate Pillow
#   export REPLICATE_API_TOKEN=r8_your_token_here
#
# Usage:
#   ./run_pipeline.sh                    # Generate everything
#   ./run_pipeline.sh human              # Generate one race
#   ./run_pipeline.sh human male_base    # Generate one layer
#   ./run_pipeline.sh --check            # Check dependencies
#   ./run_pipeline.sh --dry-run          # Preview prompts only
#   ./run_pipeline.sh --plan             # Show cost estimate
# =====================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATOR="$SCRIPT_DIR/generate_portraits.py"
POSTPROCESSOR="$SCRIPT_DIR/postprocess.py"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  GoA: Heroes of Azeroth - Portrait Pipeline     ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════╝${NC}"

# Check dependencies
if [[ "${1:-}" == "--check" ]]; then
    python3 "$POSTPROCESSOR" --check
    exit 0
fi

# Plan mode
if [[ "${1:-}" == "--plan" ]]; then
    python3 "$GENERATOR" --plan
    exit 0
fi

# Dry run
if [[ "${1:-}" == "--dry-run" ]]; then
    RACE="${2:-all}"
    LAYER="${3:-all}"
    echo -e "${YELLOW}DRY RUN: Writing prompts to files...${NC}"
    python3 "$GENERATOR" --race "$RACE" --layer "$LAYER" --dry-run
    echo -e "${GREEN}Prompts written to: $SCRIPT_DIR/output/${NC}"
    echo -e "${YELLOW}Review the prompts, then run without --dry-run${NC}"
    exit 0
fi

# Check API token
if [[ -z "${REPLICATE_API_TOKEN:-}" ]]; then
    echo -e "${RED}ERROR: REPLICATE_API_TOKEN not set${NC}"
    echo "  export REPLICATE_API_TOKEN=r8_your_token_here"
    exit 1
fi

# Determine race and layer
RACE="${1:-all}"
LAYER="${2:-all}"

echo ""
echo -e "${GREEN}Race:  ${RACE}${NC}"
echo -e "${GREEN}Layer: ${LAYER}${NC}"
echo ""

# Step 1: Generate raw images
echo -e "${BLUE}[1/4] Generating portraits via Replicate API...${NC}"
python3 "$GENERATOR" --race "$RACE" --layer "$LAYER" --skip-existing

# Step 2: Post-process
echo -e "${BLUE}[2/4] Post-processing (crop, style, alpha)...${NC}"
if [[ "$RACE" == "all" ]]; then
    python3 "$POSTPROCESSOR" --race all
else
    if [[ "$LAYER" != "all" ]]; then
        python3 "$POSTPROCESSOR" --race "$RACE" --layer "$LAYER"
    else
        python3 "$POSTPROCESSOR" --race "$RACE"
    fi
fi

# Step 3: Generate GFX definitions
echo -e "${BLUE}[3/4] Generating CK2 GFX definitions...${NC}"
python3 "$GENERATOR" --gfx-only

# Step 4: Summary
echo ""
echo -e "${BLUE}[4/4] Summary${NC}"
echo -e "${GREEN}╔══════════════════════════════════════════════════╗${NC}"

# Count generated files
RAW_COUNT=$(find "$SCRIPT_DIR/output" -name "*.png" -not -name "*_prompt*" 2>/dev/null | wc -l)
SHEET_COUNT=$(find "$SCRIPT_DIR/../../GoA_Heroes_of_Azeroth/gfx/characters" -name "*.png" 2>/dev/null | wc -l)
DDS_COUNT=$(find "$SCRIPT_DIR/../../GoA_Heroes_of_Azeroth/gfx/characters" -name "*.dds" 2>/dev/null | wc -l)

echo -e "${GREEN}║  Raw frames generated: ${RAW_COUNT}${NC}"
echo -e "${GREEN}║  Sprite sheets:        ${SHEET_COUNT} PNG${NC}"
echo -e "${GREEN}║  DDS converted:        ${DDS_COUNT}${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Review sprite sheets in gfx/characters/<race>/<gender>/"
echo "  2. If DDS conversion failed, install ImageMagick:"
echo "     sudo apt install imagemagick"
echo "  3. Test in CK2 with GoA base mod loaded"
