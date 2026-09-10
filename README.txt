===========================================================
FAMILY PHOTO CATEGORIZER - QUICK START GUIDE
===========================================================

THIS PROGRAM IS DESIGNED FOR PEOPLE WITH NO IT KNOWLEDGE!
===========================================================

What this program does:
--------------------------
This program automatically organizes your family photos into folders like:
  - birthday/
  - vacation/
  - wedding/
  - everyday/
  - pet/
  - food/
  - landscape/
  - family_event/
  - other/


HOW TO SET UP (FIRST TIME USERS):
----------------------------------

OPTION 1: IF YOU HAVE INTERNET (RECOMMENDED):
----------------------------------------
1. Open the "setup.bat" file
2. Click YES when it asks for permission
3. Wait for the setup (takes 5-10 minutes to download AI model)
4. Follow the instructions on screen

OPTION 2: IF YOU HAVE PYTHON ALREADY:
------------------------------------
1. Open the "run.bat" file
2. Click YES when it asks for permission
3. Follow the prompts

NOTE: The AI model is downloaded only once and saved locally.
After that, the program runs faster.


HOW TO USE AFTER SETUP:
-----------------------

METHOD 1: GRAPHICAL INTERFACE (EASIEST):
----------------------------------------
1. Double-click "gui.py" (this opens a picture of your computer)
2. Click "Choose Folder" for "Folder with Photos"
3. Click "Choose Folder" for "Output Folder"
4. Press "Start Categorizing"

METHOD 2: TEXT INTERFACE (IF GUI DOESN'T WORK):
-----------------------------------------------
1. Open "run.bat" (simple blue window)
2. Follow the instructions on screen


COMMON PROBLEMS & SOLUTIONS:
---------------------------

PROBLEM: "Python is not installed"
SOLUTION:
  1. Download Python from: https://www.python.org/downloads/
  2. During installation, CHECK the box that says
     "Add Python to PATH"
  3. Close and reopen this folder, then try again

PROBLEM: "Images were not sorted"
SOLUTION:
  - Make sure you selected a folder with photos (look for .jpg, .png files)
  - The output folder will be created in your selected location
  - Check the log messages in the window

PROBLEM: "The program stopped unexpectedly"
SOLUTION:
  - Close any other windows that might be blocking
  - Make sure you have at least 500 MB of free space
  - Try running "run.bat" again


GET HELP:
---------
1. If problems persist, look at the "design.md" file for technical details
2. The program creates log files with more information
3. Contact support if you can't solve the problem


WHAT HAPPENS DURING CATEGORIZATION:
-----------------------------------
1. The program reads each photo (AI model looks at each picture)
2. AI guesses which category the photo belongs to
3. Photos are copied to the right folder
4. You can see progress in the window

SAFETY:
-------
- The program NEVER uploads photos to the internet
- Photos are never shared with anyone
- All processing happens on your computer only
- Source photos are NEVER changed, moved, or deleted (unless you choose to move them)


INFO:
-----
Version: 1.0
Author: Hermes AI Agent
Date: 2026-09-10
License: Open Source

For technical documentation, see "design.md" file.

===========================================================
"DONE! This program is ready for any computer user."
===========================================================
