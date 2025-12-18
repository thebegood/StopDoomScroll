@echo off
echo ========================================
echo    StopDoomScroll - Lancement
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou pas dans le PATH!
    echo Téléchargez Python depuis: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python détecté
echo.

REM Vérifier si les dépendances sont installées
echo Vérification des dépendances...
pip show customtkinter >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation des dépendances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERREUR] Échec de l'installation des dépendances!
        pause
        exit /b 1
    )
) else (
    echo [OK] Dépendances déjà installées
)

echo.
echo ========================================
echo    Lancement de l'application...
echo ========================================
echo.

REM Lancer l'application
python main.py

if errorlevel 1 (
    echo.
    echo [ERREUR] L'application a rencontré une erreur!
    pause
)

