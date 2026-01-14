@echo off
echo Starting Smart Meeting Notes Generator...
echo.

REM Check if virtual environment exists
if not exist "env\" (
    echo Creating virtual environment...
    python -m venv env
    call env\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    call env\Scripts\activate.bat
)

echo.
echo Starting Backend Server...
start "Backend - FastAPI" cmd /k "cd backend && uvicorn app.main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo Starting Frontend...
start "Frontend - Streamlit" cmd /k "cd frontend && streamlit run streamlit_app.py"

echo.
echo ========================================
echo   Smart Meeting Notes Generator
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:8501
echo.
echo Press Ctrl+C in each window to stop
echo ========================================
pause
