# Family Photo Categorizer - Simple Setup for Everyone

## 🎯 What This Does
This program automatically sorts your family photos into folders like:
- 🎉 `birthday/` 
- 🏖️ `vacation/`
- 💍 `wedding/`
- 👨‍👩‍👧‍👦 `family_event/`
- 🐶 `pet/`
- 🍽️ `food/`
- 🏞️ `landscape/`
- 🎄 `holiday/`
- ☀️ `everyday/`
- ❓ `other/`

It runs completely on your computer - **no internet needed after setup**, **no privacy risks**, **no photo uploads**.

## 📋 Quick Start for Beginners

### Option 1: Super Simple (Recommended)
1. **Double-click `setup.bat`** and click "YES" when asked
2. **Wait 5-10 minutes** for setup to complete (downloads AI brain)
3. **Copy your photos** into the `Photos` folder inside this directory
4. **Double-click `gui.py`** to open the friendly window
5. **Click "Choose Folder"** for both source and destination
6. **Press "Start Categorizing"** and wait for completion
7. **Check your output folder** for sorted photos!

### Option 2: Just Want to Try (If You Have Python)
1. Double-click `run.bat`
2. Follow the instructions
3. Uses the built-in `Photos` and `Categorized` folders by default

## 🖥️ System Requirements
- Windows 10 or 11
- Minimum 500 MB free disk space
- Internet connection needed **only for first-time setup**
- Works on most computers from the last 5 years

## 🛠️ What's Included
- `setup.bat` - One-click setup (downloads everything needed)
- `gui.py` - Friendly graphical interface (no typing!)
- `run.bat` - Simple text-based interface
- `main.py` - The core AI program
- `design.md` - Technical details (if you're curious)

## ❓ Common Questions

**Q: Is my data private?**  
A: Yes! All processing happens on your computer. Nothing is uploaded or shared.

**Q: Will it delete my original photos?**  
A: No! By default it **copies** photos. You can choose to move them if you want.

**Q: How long does it take?**  
A: First photo: 2-3 minutes (loading AI). Subsequent photos: 30-60 seconds each. 
Total time ≈ (Number of photos × 45 seconds) + 2 minutes.

**Q: What if I make a mistake?**  
A: Original photos stay safe in your source folder. You can always re-run with different settings.

**Q: Why is the AI model so big?**  
A: The AI needs to recognize thousands of concepts (birthday cakes, beaches, wedding dresses, etc.) 
to accurately categorize your family memories.

## 🔧 Technical Details (Optional)
See `design.md` for information about:
- The AI model (Qwen2.5-VL-3B-Instruct)
- How the categorization works
- Performance benchmarks
- Future enhancement ideas

## 🆘 Need Help?
1. Read `HOW_TO_USE.txt` for step-by-step instructions with pictures
2. Check `README.txt` for quick troubleshooting
3. Look at error messages in the black window if something fails
4. Most issues are solved by re-running `setup.bat`

---

**Ready to organize your family photos? Start with `setup.bat`!**