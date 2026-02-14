@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

echo ============================================
echo  GoA Submods Installer - CK2
echo  Heroes of Azeroth + Improved Economy
echo ============================================
echo.

REM --- Detect CK2 mod folder ---
set "CK2_MOD="

REM Standard Documents path
if exist "%USERPROFILE%\Documents\Paradox Interactive\Crusader Kings II\mod" (
    set "CK2_MOD=%USERPROFILE%\Documents\Paradox Interactive\Crusader Kings II\mod"
)

REM OneDrive Documents path
if not defined CK2_MOD (
    if exist "%USERPROFILE%\OneDrive\Documents\Paradox Interactive\Crusader Kings II\mod" (
        set "CK2_MOD=%USERPROFILE%\OneDrive\Documents\Paradox Interactive\Crusader Kings II\mod"
    )
)

REM Custom Documents folder via registry
if not defined CK2_MOD (
    for /f "tokens=2*" %%A in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Personal 2^>nul') do (
        set "DOCS=%%B"
    )
    if defined DOCS (
        call set "DOCS=!DOCS:%%USERPROFILE%%=%USERPROFILE%!"
        if exist "!DOCS!\Paradox Interactive\Crusader Kings II\mod" (
            set "CK2_MOD=!DOCS!\Paradox Interactive\Crusader Kings II\mod"
        )
    )
)

if not defined CK2_MOD (
    echo [ERREUR] Dossier CK2 introuvable automatiquement.
    echo.
    echo Entrez le chemin complet vers votre dossier "mod" de CK2:
    echo Exemple: C:\Users\VotreNom\Documents\Paradox Interactive\Crusader Kings II\mod
    echo.
    set /p "CK2_MOD=Chemin: "
)

if not exist "!CK2_MOD!" (
    echo [ERREUR] Le dossier "!CK2_MOD!" n'existe pas.
    echo Verifiez que CK2 et Guardians of Azeroth sont bien installes.
    pause
    exit /b 1
)

echo [OK] Dossier CK2 detecte:
echo     !CK2_MOD!
echo.

REM --- Check GoA base mod ---
set "GOA_FOUND=0"
if exist "!CK2_MOD!\guardians_of_azeroth.mod" set "GOA_FOUND=1"
if exist "!CK2_MOD!\Guardians_of_Azeroth.mod" set "GOA_FOUND=1"
if exist "!CK2_MOD!\warcraft.mod" set "GOA_FOUND=1"
for /f %%F in ('dir /b "!CK2_MOD!\*azeroth*" 2^>nul') do set "GOA_FOUND=1"
for /f %%F in ('dir /b "!CK2_MOD!\*warcraft*" 2^>nul') do set "GOA_FOUND=1"
for /f %%F in ('dir /b "!CK2_MOD!\*Warcraft*" 2^>nul') do set "GOA_FOUND=1"

if "!GOA_FOUND!"=="0" (
    echo [ATTENTION] Le mod de base "Warcraft: Guardians of Azeroth" n'a pas ete detecte.
    echo Ces submods en dependent. Assurez-vous qu'il est installe.
    echo.
    choice /M "Continuer quand meme"
    if errorlevel 2 exit /b 0
    echo.
)

REM --- Get script directory ---
set "SCRIPT_DIR=%~dp0"

REM --- Install Heroes of Azeroth ---
echo [1/2] Installation de GoA: Heroes of Azeroth...

if exist "!SCRIPT_DIR!GoA_Heroes_of_Azeroth.mod" (
    copy /Y "!SCRIPT_DIR!GoA_Heroes_of_Azeroth.mod" "!CK2_MOD!\GoA_Heroes_of_Azeroth.mod" >nul
) else (
    echo [ERREUR] GoA_Heroes_of_Azeroth.mod introuvable dans !SCRIPT_DIR!
    goto :skip_hoa
)

if exist "!SCRIPT_DIR!GoA_Heroes_of_Azeroth\" (
    robocopy "!SCRIPT_DIR!GoA_Heroes_of_Azeroth" "!CK2_MOD!\GoA_Heroes_of_Azeroth" /MIR /NFL /NDL /NJH /NJS /nc /ns /np >nul
    echo     [OK] Heroes of Azeroth installe.
) else (
    echo     [ERREUR] Dossier GoA_Heroes_of_Azeroth introuvable.
)
:skip_hoa

REM --- Install Improved Economy ---
echo [2/2] Installation de GoA: Improved Economy...

if exist "!SCRIPT_DIR!GoA_Improved_Economy.mod" (
    copy /Y "!SCRIPT_DIR!GoA_Improved_Economy.mod" "!CK2_MOD!\GoA_Improved_Economy.mod" >nul
) else (
    echo [ERREUR] GoA_Improved_Economy.mod introuvable dans !SCRIPT_DIR!
    goto :skip_ie
)

if exist "!SCRIPT_DIR!GoA_Improved_Economy\" (
    robocopy "!SCRIPT_DIR!GoA_Improved_Economy" "!CK2_MOD!\GoA_Improved_Economy" /MIR /NFL /NDL /NJH /NJS /nc /ns /np >nul
    echo     [OK] Improved Economy installe.
) else (
    echo     [ERREUR] Dossier GoA_Improved_Economy introuvable.
)
:skip_ie

echo.
echo ============================================
echo  Installation terminee!
echo ============================================
echo.
echo Lancez CK2 et activez dans le launcher:
echo   [x] Warcraft: Guardians of Azeroth
echo   [x] GoA: Heroes of Azeroth
echo   [x] GoA: Improved Economy
echo.
echo Ordre de chargement recommande:
echo   1. Guardians of Azeroth (base)
echo   2. Improved Economy
echo   3. Heroes of Azeroth
echo.
pause
