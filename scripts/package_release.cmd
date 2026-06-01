@echo off
pushd "%~dp0.."
set VERSION=v2.2.4
set RELEASE_DIR=releases\Release_%VERSION%

echo [*] Starting Build and Packaging Process for %VERSION%...

:: 1. Build the EXE
echo [*] Step 1: Building Executable...
python -m PyInstaller --noconfirm --onefile --windowed --noconsole --uac-admin --name "CoreOptimizer" --collect-all "customtkinter" main.py

if %ERRORLEVEL% NEQ 0 (
    echo [!] Build failed!
    popd
    pause
    exit /b %ERRORLEVEL%
)

:: 2. Create Release Folder
echo [*] Step 2: Creating Release Folder: %RELEASE_DIR%
if exist %RELEASE_DIR% rd /s /q %RELEASE_DIR%
mkdir %RELEASE_DIR%

:: 3. Copy Files
echo [*] Step 3: Collecting files...
copy dist\CoreOptimizer.exe %RELEASE_DIR%\
if exist README.md copy README.md %RELEASE_DIR%\
if exist RELEASE_NOTES.md copy RELEASE_NOTES.md %RELEASE_DIR%\
if exist docs\clean_junk_logic.txt copy docs\clean_junk_logic.txt %RELEASE_DIR%\
if exist LICENSE copy LICENSE %RELEASE_DIR%\

:: 4. Cleanup temporary build files
echo [*] Step 4: Cleaning up temporary files...
if exist build rd /s /q build
if exist CoreOptimizer.spec del /q CoreOptimizer.spec

echo.
echo ======================================================
echo [OK] Release Packaged Successfully!
echo [OK] Folder: %RELEASE_DIR%
echo [OK] You can now zip this folder and send it to users.
echo ======================================================
popd
pause
