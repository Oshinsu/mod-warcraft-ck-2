#!/bin/bash
# GoA Submods Installer - CK2
# Heroes of Azeroth + Improved Economy

set -e

echo "============================================"
echo " GoA Submods Installer - CK2"
echo " Heroes of Azeroth + Improved Economy"
echo "============================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# --- Detect CK2 mod folder ---
CK2_MOD=""

# Linux (Steam)
if [ -d "$HOME/.local/share/Paradox Interactive/Crusader Kings II/mod" ]; then
    CK2_MOD="$HOME/.local/share/Paradox Interactive/Crusader Kings II/mod"
# Linux (alternate)
elif [ -d "$HOME/.paradoxinteractive/Crusader Kings II/mod" ]; then
    CK2_MOD="$HOME/.paradoxinteractive/Crusader Kings II/mod"
# macOS
elif [ -d "$HOME/Documents/Paradox Interactive/Crusader Kings II/mod" ]; then
    CK2_MOD="$HOME/Documents/Paradox Interactive/Crusader Kings II/mod"
# macOS (Library)
elif [ -d "$HOME/Library/Application Support/Paradox Interactive/Crusader Kings II/mod" ]; then
    CK2_MOD="$HOME/Library/Application Support/Paradox Interactive/Crusader Kings II/mod"
# WSL -> Windows Documents
elif [ -d "/mnt/c/Users" ]; then
    for WINUSER in /mnt/c/Users/*/; do
        if [ -d "${WINUSER}Documents/Paradox Interactive/Crusader Kings II/mod" ]; then
            CK2_MOD="${WINUSER}Documents/Paradox Interactive/Crusader Kings II/mod"
            break
        fi
        if [ -d "${WINUSER}OneDrive/Documents/Paradox Interactive/Crusader Kings II/mod" ]; then
            CK2_MOD="${WINUSER}OneDrive/Documents/Paradox Interactive/Crusader Kings II/mod"
            break
        fi
    done
fi

if [ -z "$CK2_MOD" ]; then
    echo "[ERREUR] Dossier CK2 introuvable automatiquement."
    echo ""
    echo "Entrez le chemin complet vers votre dossier 'mod' de CK2:"
    read -r -p "Chemin: " CK2_MOD
fi

if [ ! -d "$CK2_MOD" ]; then
    echo "[ERREUR] Le dossier '$CK2_MOD' n'existe pas."
    echo "Verifiez que CK2 et Guardians of Azeroth sont bien installes."
    exit 1
fi

echo "[OK] Dossier CK2 detecte:"
echo "    $CK2_MOD"
echo ""

# --- Install Heroes of Azeroth ---
echo "[1/2] Installation de GoA: Heroes of Azeroth..."

if [ -f "$SCRIPT_DIR/GoA_Heroes_of_Azeroth.mod" ]; then
    cp -f "$SCRIPT_DIR/GoA_Heroes_of_Azeroth.mod" "$CK2_MOD/GoA_Heroes_of_Azeroth.mod"
else
    echo "    [ERREUR] GoA_Heroes_of_Azeroth.mod introuvable."
fi

if [ -d "$SCRIPT_DIR/GoA_Heroes_of_Azeroth" ]; then
    rsync -a --delete "$SCRIPT_DIR/GoA_Heroes_of_Azeroth/" "$CK2_MOD/GoA_Heroes_of_Azeroth/"
    echo "    [OK] Heroes of Azeroth installe."
else
    echo "    [ERREUR] Dossier GoA_Heroes_of_Azeroth introuvable."
fi

# --- Install Improved Economy ---
echo "[2/2] Installation de GoA: Improved Economy..."

if [ -f "$SCRIPT_DIR/GoA_Improved_Economy.mod" ]; then
    cp -f "$SCRIPT_DIR/GoA_Improved_Economy.mod" "$CK2_MOD/GoA_Improved_Economy.mod"
else
    echo "    [ERREUR] GoA_Improved_Economy.mod introuvable."
fi

if [ -d "$SCRIPT_DIR/GoA_Improved_Economy" ]; then
    rsync -a --delete "$SCRIPT_DIR/GoA_Improved_Economy/" "$CK2_MOD/GoA_Improved_Economy/"
    echo "    [OK] Improved Economy installe."
else
    echo "    [ERREUR] Dossier GoA_Improved_Economy introuvable."
fi

echo ""
echo "============================================"
echo " Installation terminee!"
echo "============================================"
echo ""
echo "Lancez CK2 et activez dans le launcher:"
echo "  [x] Warcraft: Guardians of Azeroth"
echo "  [x] GoA: Heroes of Azeroth"
echo "  [x] GoA: Improved Economy"
echo ""
echo "Ordre de chargement recommande:"
echo "  1. Guardians of Azeroth (base)"
echo "  2. Improved Economy"
echo "  3. Heroes of Azeroth"
