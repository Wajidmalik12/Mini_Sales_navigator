@echo off
echo ========================================================
echo   Launching Mini Sales Navigator Web UI...
echo ========================================================
echo.
cd /d "%~dp0"
call venv\Scripts\activate.bat 2>nul || (
    echo [INFO] Virtual environment not activated, using system python.
)
start "" http://127.0.0.1:8000
python -m uvicorn server:app --host 127.0.0.1 --port 8000 --reload
pause
