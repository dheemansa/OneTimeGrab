@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

IF /I "%1" == "--new" (
    python new_session.py
)

SET SCRIPT_DIR=%~dp0
CD /D "%SCRIPT_DIR%"

python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.9+ first.
    pause
    exit /b 1
)

pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip is not installed. Please install pip.
    pause
    exit /b 1
)

IF NOT EXIST ".env" (
    echo The .env file does not exist. Running setup...
    python setup.py
)

pip install -r requirements.txt

python -m src.main
echo Done.
pause