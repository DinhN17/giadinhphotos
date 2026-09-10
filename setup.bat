@echo off
echo ============================================================
echo           FAMILY PHOTO CATEGORIZER - SETUP
echo ============================================================
echo.
echo This will install everything needed to run the program.
echo It will install Python dependencies and download the AI model.
echo.
echo Estimated time: 5-10 minutes (depends on internet speed)
echo.
pause

echo.
echo Step 1: Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python is not installed.
  echo.
  echo Please install Python 3.10 or newer from:
  echo   https://www.python.org/downloads/
  echo.
  echo IMPORTANT: During installation, CHECK the box that says
  echo "Add Python to PATH" before clicking Install Now.
  echo.
  pause
  exit /b 1
)
echo Python found.

echo.
echo Step 2: Installing Python libraries...
pip install torch transformers Pillow tqdm

echo.
echo Step 3: Downloading AI model (first time only)...
echo This downloads the vision-language model (~2GB).
python "%~dp0main.py" --source "%~dp0Photos" --dest "%~dp0Categorized" --model "Qwen/Qwen2.5-VL-3B-Instruct" --device cpu --categories birthday vacation holiday wedding everyday pet food landscape family_event other --max_new_tokens 30
if errorlevel 1 (
  echo.
  echo The setup encountered an error during model download or testing.
  echo Please check the README.txt file for help.
  echo.
  pause
  exit /b 1
)

echo.
echo ============================================================
echo SETUP COMPLETE!
echo ============================================================
echo.
echo How to use:
echo   1. Put your family photos in the "Photos" folder
echo      (create it if it doesn't exist)
echo   2. Double-click "run.bat" to start the program
echo   3. Find your sorted photos in the "Categorized" folder
echo.
echo First-time users:
echo   - The program may take a few minutes per photo on first run
echo   - Subsequent runs will be faster (model stays in memory)
echo   - Press Ctrl+C to stop the program anytime
echo.
pause
