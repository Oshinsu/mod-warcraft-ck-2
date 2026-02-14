#!/bin/bash
# =============================================================================
# GoA Heroes of Azeroth — Asset Generation from SOTA JSON Prompts
# Reads structured JSON prompt files and calls Replicate API
# Downloads results directly to repo (Replicate deletes after 1h)
# =============================================================================

set -euo pipefail

API_TOKEN="${REPLICATE_API_TOKEN:?Set REPLICATE_API_TOKEN env var}"
API_URL="https://api.replicate.com/v1/models/google/nano-banana-pro/predictions"
REPO_DIR="/home/user/mod-warcraft-ck-2"
PROMPTS_DIR="$REPO_DIR/tools/prompts"

# Counters
TOTAL=0
SUCCESS=0
FAIL=0
SKIP=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
log_fail() { echo -e "${RED}[FAIL]${NC} $1"; }
log_skip() { echo -e "${YELLOW}[SKIP]${NC} $1"; }
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }

# =============================================================================
# Extract prompt text and parameters from JSON, call API, download result
# =============================================================================
generate_from_json() {
    local json_file="$1"
    local asset_id target_path aspect_ratio positive negative

    # Parse JSON fields
    asset_id=$(python3 -c "import json,sys; d=json.load(open('$json_file')); print(d['meta']['asset_id'])")
    target_path=$(python3 -c "import json,sys; d=json.load(open('$json_file')); print(d['meta']['target_path'])")
    aspect_ratio=$(python3 -c "import json,sys; d=json.load(open('$json_file')); print(d['parameters']['aspect_ratio'])")

    local output_file="$REPO_DIR/$target_path"

    # Skip if already generated
    if [ -f "$output_file" ] && [ -s "$output_file" ]; then
        log_skip "$asset_id — already exists ($(du -h "$output_file" | cut -f1))"
        SKIP=$((SKIP + 1))
        TOTAL=$((TOTAL + 1))
        return 0
    fi

    # Ensure target directory exists
    mkdir -p "$(dirname "$output_file")"

    # Extract positive and negative prompts
    positive=$(python3 -c "
import json, sys
d = json.load(open('$json_file'))
print(d['prompt_construction']['positive'])
")
    negative=$(python3 -c "
import json, sys
d = json.load(open('$json_file'))
print(d['prompt_construction']['negative'])
")

    log_info "Generating: $asset_id ($aspect_ratio)..."

    # Build API request payload
    local payload
    payload=$(python3 -c "
import json, sys
positive = sys.stdin.read()
d = {
    'input': {
        'prompt': positive.strip(),
        'aspect_ratio': '$aspect_ratio',
        'output_format': 'png',
        'safety_filter_level': 'block_none'
    }
}
print(json.dumps(d))
" <<< "$positive")

    # Call Replicate API with Prefer: wait (synchronous)
    local response
    response=$(curl --silent --show-error --max-time 300 \
        "$API_URL" \
        -X POST \
        -H "Authorization: Bearer $API_TOKEN" \
        -H "Content-Type: application/json" \
        -H "Prefer: wait" \
        -d "$payload" 2>&1) || {
        log_fail "$asset_id — curl failed"
        FAIL=$((FAIL + 1))
        TOTAL=$((TOTAL + 1))
        return 1
    }

    # Extract image URL from response
    local image_url status error
    image_url=$(python3 -c "
import json, sys
d = json.loads(sys.stdin.read())
out = d.get('output', '')
if isinstance(out, list):
    print(out[0] if out else '')
else:
    print(out or '')
" <<< "$response" 2>/dev/null) || image_url=""

    status=$(python3 -c "import json,sys; print(json.loads(sys.stdin.read()).get('status',''))" <<< "$response" 2>/dev/null) || status=""

    if [ -z "$image_url" ] || [ "$image_url" = "None" ] || [ "$image_url" = "" ]; then
        error=$(python3 -c "import json,sys; print(json.loads(sys.stdin.read()).get('error','unknown'))" <<< "$response" 2>/dev/null) || error="unknown"
        log_fail "$asset_id — API error: $error (status: $status)"
        FAIL=$((FAIL + 1))
        TOTAL=$((TOTAL + 1))
        return 1
    fi

    # Download image directly to repo
    curl --silent --max-time 60 -o "$output_file" "$image_url" || {
        log_fail "$asset_id — download failed"
        FAIL=$((FAIL + 1))
        TOTAL=$((TOTAL + 1))
        return 1
    }

    if [ -f "$output_file" ] && [ -s "$output_file" ]; then
        local size
        size=$(du -h "$output_file" | cut -f1)
        log_ok "$asset_id — $size → $output_file"
        SUCCESS=$((SUCCESS + 1))
    else
        log_fail "$asset_id — empty file"
        rm -f "$output_file"
        FAIL=$((FAIL + 1))
    fi
    TOTAL=$((TOTAL + 1))
}

# =============================================================================
# Main
# =============================================================================
echo "============================================================"
echo "  GoA Heroes of Azeroth — SOTA Asset Generation Pipeline"
echo "============================================================"
echo ""

# Process each category
for category_dir in "$PROMPTS_DIR"/*/; do
    category=$(basename "$category_dir")
    json_count=$(ls "$category_dir"/*.json 2>/dev/null | wc -l)

    if [ "$json_count" -eq 0 ]; then
        continue
    fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Category: $category ($json_count prompts)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    for json_file in "$category_dir"/*.json; do
        generate_from_json "$json_file"
    done
done

echo ""
echo "============================================================"
echo "  GENERATION COMPLETE"
echo "  Total: $TOTAL | Success: $SUCCESS | Failed: $FAIL | Skipped: $SKIP"
echo "============================================================"

# List generated files
echo ""
echo "Generated files:"
find "$REPO_DIR/GoA_Heroes_of_Azeroth/gfx" -name "*.png" -exec ls -lh {} \; 2>/dev/null
