#!/bin/bash
# ============================================
# GoA Submods - Installation Script (Mac/Linux)
# ============================================
# Usage: ./INSTALL.sh
#
# Pre-requis: "Warcraft: Guardians of Azeroth" installe via Steam Workshop
# ============================================

set -e

# Detect CK2 mod directory
if [[ "$OSTYPE" == "darwin"* ]]; then
    CK2_MOD_DIR="$HOME/Documents/Paradox Interactive/Crusader Kings II/mod"
elif [[ "$OSTYPE" == "linux"* ]]; then
    CK2_MOD_DIR="$HOME/.local/share/Paradox Interactive/Crusader Kings II/mod"
else
    echo "OS non supporte. Copie manuellement dans le dossier mod de CK2."
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== GoA Submods Installer ==="
echo ""
echo "Dossier CK2 detecte: $CK2_MOD_DIR"
echo ""

# Check CK2 mod dir exists
if [ ! -d "$CK2_MOD_DIR" ]; then
    echo "ERREUR: Dossier CK2 introuvable: $CK2_MOD_DIR"
    echo "Verifie que CK2 a ete lance au moins une fois."
    exit 1
fi

# Install Heroes of Azeroth
echo "[1/2] Installation de GoA: Heroes of Azeroth..."
cp "$SCRIPT_DIR/GoA_Heroes_of_Azeroth.mod" "$CK2_MOD_DIR/"
rm -rf "$CK2_MOD_DIR/GoA_Heroes_of_Azeroth"
cp -r "$SCRIPT_DIR/GoA_Heroes_of_Azeroth" "$CK2_MOD_DIR/"
echo "      OK"

# Install Improved Economy
echo "[2/2] Installation de GoA: Improved Economy..."
cp "$SCRIPT_DIR/GoA_Improved_Economy.mod" "$CK2_MOD_DIR/"
rm -rf "$CK2_MOD_DIR/GoA_Improved_Economy"
cp -r "$SCRIPT_DIR/GoA_Improved_Economy" "$CK2_MOD_DIR/"
echo "      OK"

echo ""
echo "=== Installation terminee! ==="
echo ""
echo "Prochaines etapes:"
echo "  1. Lance CK2 via Steam"
echo "  2. Dans le Launcher, coche les mods:"
echo "     - Warcraft: Guardians of Azeroth (mod principal)"
echo "     - GoA: Heroes of Azeroth"
echo "     - GoA: Improved Economy & Buildings"
echo "  3. Joue!"
echo ""
