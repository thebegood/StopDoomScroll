@echo off
echo ========================================
echo    StopDoomScroll - Installation
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH!
    echo Telechargez Python 3.11 ou 3.12 depuis: https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Cochez "Add Python to PATH" lors de l'installation!
    pause
    exit /b 1
)

echo [OK] Python detecte
python --version
echo.

REM Vérifier la version de Python
for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Version detectee: %PYTHON_VERSION%

REM Avertir si Python 3.13
echo %PYTHON_VERSION% | findstr /C:"3.13" >nul
if not errorlevel 1 (
    echo.
    echo [AVERTISSEMENT] Python 3.13 detecte!
    echo Cette version peut avoir des problemes de compatibilite.
    echo Python 3.11 ou 3.12 est recommande.
    echo.
    echo Voulez-vous continuer quand meme? ^(O/N^)
    set /p CONTINUE="> "
    if /i not "%CONTINUE%"=="O" (
        echo Installation annulee.
        pause
        exit /b 0
    )
)

echo.
echo [INFO] Mise a jour de pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [ERREUR] Echec de la mise a jour de pip!
    pause
    exit /b 1
)

echo.
echo [INFO] Installation des dependances...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERREUR] Echec de l'installation!
    echo.
    echo Solutions possibles:
    echo 1. Si vous avez Python 3.13, installez Python 3.11 ou 3.12
    echo 2. Essayez: pip install --upgrade pip setuptools wheel
    echo 3. Essayez: pip install -r requirements-py313.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Installation terminee avec succes!
echo ========================================
echo.
echo Pour lancer l'application:
echo - Double-cliquez sur start.bat
echo - Ou tapez: python main.py
echo.
pause

