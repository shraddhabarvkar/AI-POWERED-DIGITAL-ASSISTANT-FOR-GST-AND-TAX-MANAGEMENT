@echo off
echo.
echo =============================================
echo    InvoiScope - GST SmartScan Backend
echo =============================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo [1/3] Installing backend dependencies...
pip install -r backend\requirements.txt

echo.
echo [2/3] Creating data directories...
if not exist "data\uploads" mkdir "data\uploads"
if not exist "data\results" mkdir "data\results"
if not exist "data\temp" mkdir "data\temp"

echo.
echo [3/3] Starting FastAPI server on http://localhost:8000 ...
echo       API Docs available at: http://localhost:8000/docs
echo.
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

pause
