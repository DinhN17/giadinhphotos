@echo off
echo ============================================================
echo             FAMILY PHOTO CATEGORIZER
echo ============================================================
echo.
echo This program will help you organize your family photos
echo using a local AI model on your computer.
echo.
echo IMPORTANT:
echo   - This program needs Python to be installed first
echo   - It will ask you for the folder containing your photos
echo   - It will create a new folder with all photos sorted by category
echo.
echo If you see an error, please check the README.txt file.
echo.
echo Press any key to continue...
pause > nul

python "%~dp0main.py" --source "%~dp0Photos" --dest "%~dp0Categorized" --device cpu
if errorlevel 1 (
  echo.
  echo Something went wrong. Please check the README.txt file.
  echo.
  pause
  exit /b 1
)

echo.
echo Done! Your photos have been organized.
echo You can find them in the "Categorized" folder.
echo.
pause > nul
