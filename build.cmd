@echo off
title CoreOptimizer Build Script
echo ======================================================
echo           CoreOptimizer Build Automation
echo ======================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Error: Python is not installed or not in PATH.
    pause
    exit /b %errorlevel%
)

echo [*] Cleaning previous builds...
if exist build rd /s /q build
if exist dist rd /s /q dist

echo [*] Installing/Updating required tools...
python -m pip install --upgrade pip pyinstaller >nul

echo [*] Starting PyInstaller build process...
echo     - Mode: One File
echo     - GUI: Windowed (No Console)
echo     - Elevation: UAC Admin
echo.

python -m PyInstaller --noconfirm --onefile --windowed --noconsole --uac-admin --name "CoreOptimizer" --collect-all "customtkinter" main.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================
    echo [OK] Build Completed Successfully!
    echo [OK] Executable: dist\CoreOptimizer.exe
    echo ======================================================
) else (
    echo.
    echo [!] Build Failed! Please check the error messages above.
)
echo.
pause
