
@echo off
setlocal
title YORU TERMINAL // TACTICAL LAUNCHER
color 0B

cd /d "%~dp0"

cls
echo.
echo  ============================================================
echo.
echo     Y   Y   OOO   RRRR   U   U
echo     Y   Y  O   O  R   R  U   U
echo      Y Y   O   O  RRRR   U   U
echo       Y    O   O  R  R   U   U
echo       Y     OOO   R   R   UUU
echo.
echo              YORU TERMINAL
echo          TACTICAL TRAINING SYSTEM
echo.
echo  ============================================================
echo.
echo  [BOOT] Initializing launcher...
timeout /t 1 /nobreak >nul

echo  [CHECK] Looking for the Python environment...

if exist ".venv\Scripts\python.exe" (
    set "YORU_PYTHON=%~dp0.venv\Scripts\python.exe"
) else (
    where python >nul 2>&1
    if errorlevel 1 (
        echo.
        echo  [ERROR] Python was not found.
        echo  Install Python or recreate the .venv environment.
        goto error
    )
    set "YORU_PYTHON=python"
)

echo  [OK] Python interpreter located.
echo  [CHECK] Verifying game entry point...

if not exist "main.py" (
    echo.
    echo  [ERROR] main.py was not found.
    echo  Make sure this launcher is inside the YoruTerminal folder.
    goto error
)

echo  [OK] Game entry point located.
echo.
echo  ============================================================
echo.
echo  1. INITIALIZE TRAINING SESSION
echo  2. RUN SYSTEM DIAGNOSTICS
echo  3. EXIT
echo.
echo  ============================================================
echo.

choice /c 123 /n /m "SELECT OPERATION > "

if errorlevel 3 goto end
if errorlevel 2 goto diagnostics
if errorlevel 1 goto launch

:launch
cls
echo.
echo  [BOOT] Launching YoruTerminal...
echo.
"%YORU_PYTHON%" main.py
echo.
echo  [INFO] Training session ended.
goto finish

:diagnostics
cls
echo.
echo  YORU TERMINAL // SYSTEM DIAGNOSTICS
echo  -----------------------------------
echo.
"%YORU_PYTHON%" --version
if errorlevel 1 (
    echo  [FAIL] Python could not run.
    goto error
)
echo.
"%YORU_PYTHON%" -c "import rich, argon2; print('[OK] Required Python packages are available.')"
if errorlevel 1 (
    echo  [FAIL] A required package is missing.
    echo  Activate .venv and install requirements.txt.
    goto error
)
echo.
"%YORU_PYTHON%" -c "from pathlib import Path; print('[OK] Project directory:', Path.cwd()); print('[OK] Main entry point:', Path('main.py').exists())"
echo.
echo  [INFO] Diagnostics complete.
goto finish

:error
echo.
echo  [ERROR] Launcher could not complete this operation.

:finish
echo.
pause
goto end

:end
endlocal
