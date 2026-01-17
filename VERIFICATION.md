# Installation & Verification Checklist

## ✅ Pre-Installation Checklist

Before you start, make sure you have:

- [ ] Python 3.8 or higher installed
- [ ] Administrator access to install packages
- [ ] Approximately 500MB free disk space
- [ ] 10-15 minutes for setup
- [ ] Internet connection (for pip install)

---

## 🔧 Installation Steps

### Step 1: Install Python
- [ ] Download from https://www.python.org/downloads/
- [ ] Run installer
- [ ] **IMPORTANT**: Check "Add Python to PATH" during installation
- [ ] Verify: `python --version` in terminal (should show 3.8+)

### Step 2: Install FFmpeg
**Windows - Option A (Chocolatey):**
```powershell
choco install ffmpeg
```

**Windows - Option B (Manual):**
- [ ] Download from https://ffmpeg.org/download.html
- [ ] Add to Windows PATH manually
- [ ] Verify: `ffmpeg -version` in terminal

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### Step 3: Install Python Packages
```bash
cd path/to/2xkoGPAnalyzer_VisualStudio
pip install -r requirements.txt
```

- [ ] Installation completes without errors
- [ ] Shows: "Successfully installed [packages]"

---

## ✅ Verification Checklist

### Step 1: Verify Python
```bash
python --version
```
**Expected**: `Python 3.x.x` (3.8 or higher)

- [ ] Python version 3.8+
- [ ] Path includes Python

### Step 2: Verify FFmpeg
```bash
ffmpeg -version
```
**Expected**: Shows FFmpeg version info

- [ ] FFmpeg version displayed
- [ ] No "command not found" error

### Step 3: Verify Dependencies
```bash
python -c "import cv2, numpy, yaml; print('All dependencies OK')"
```
**Expected**: "All dependencies OK"

- [ ] No import errors
- [ ] All packages installed

### Step 4: Run Test Suite
```bash
python tests.py
```
**Expected**: 
```
Ran 12 tests
OK
```

- [ ] All tests pass
- [ ] No errors or failures

### Step 5: Launch Application
```bash
python main.py
```
**Expected**: 
```
╔════════════════════════════════════════════════════════╗
║          2XKO GAMEPLAY ANALYZER v1.0                    ║
║                                                         ║
║  Analyze fighting game footage & get improvement tips   ║
║  Focus: Frame Data, Mistakes, Playstyle Analysis       ║
╚════════════════════════════════════════════════════════╝

MAIN MENU
═══════════════════════════════════════════════════════
1. Analyze Gameplay Video
2. View Available Characters
3. View Blitzcrank Frame Data
4. View Blitzcrank Tips
5. Exit
```

- [ ] Application starts successfully
- [ ] Menu displays correctly
- [ ] Can select options (try 2 or 3)

---

## 🧪 Full System Test

### Test 1: Frame Data Access
```
1. Run: python main.py
2. Select: 3 (View Blitzcrank Frame Data)
3. Select: "5L" or search for "Rocket"
4. Should see move data with:
   - Damage
   - Startup frames
   - Recovery frames
   - On-block advantage
```

**Result**: ✅ / ❌

### Test 2: Tips Access
```
1. Run: python main.py
2. Select: 4 (View Blitzcrank Tips)
3. Should see multiple sections:
   - Neutral Game Tips
   - Mix-up Game
   - Neutral Tools
   - Steam Mechanic
   - Mirror Matchup
```

**Result**: ✅ / ❌

### Test 3: Character Selection
```
1. Run: python main.py
2. Select: 2 (View Available Characters)
3. Should list 11 characters
4. Blitzcrank should have "Frame data available"
```

**Result**: ✅ / ❌

### Test 4: Menu Navigation
```
1. Run: python main.py
2. Test all menu options 1-5
3. Test "0" to go back from submenus
4. Test invalid input handling
```

**Result**: ✅ / ❌

---

## 🆘 Troubleshooting Guide

### Issue: "Python is not recognized"
**Cause**: Python not in system PATH  
**Solution**:
- Reinstall Python
- Check "Add Python to PATH" during installation
- Restart terminal/computer after installation

### Issue: "pip is not recognized"
**Cause**: pip not properly installed with Python  
**Solution**:
```bash
python -m pip install -r requirements.txt
```

### Issue: "FFmpeg not found"
**Cause**: FFmpeg not installed or not in PATH  
**Solution**:
- Install FFmpeg (see Installation Step 2)
- Add FFmpeg to system PATH
- Restart terminal after installation

### Issue: Module import errors
**Cause**: Dependencies not installed  
**Solution**:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue: "Video file not found"
**Cause**: Incorrect file path  
**Solution**:
- Use absolute path: `C:\Users\YourName\Videos\filename.mp4`
- Or drag-drop file when prompted
- Ensure file exists and isn't corrupted

### Issue: Tests fail
**Cause**: Missing dependencies or installation issue  
**Solution**:
```bash
pip install -r requirements.txt --force-reinstall
python tests.py
```

### Issue: Application won't start
**Cause**: Various possible issues  
**Solution**:
1. Verify Python installation: `python --version`
2. Verify dependencies: `pip list` (check for opencv-python, numpy, etc.)
3. Check if any Python files were corrupted
4. Try running from project directory: `cd 2xkoGPAnalyzer_VisualStudio`

---

## 📋 Complete Setup Verification

Use this checklist to verify everything is working:

### Environment
- [ ] Python 3.8+ installed
- [ ] FFmpeg installed and in PATH
- [ ] Project directory accessible
- [ ] Enough disk space (500MB+)

### Dependencies
- [ ] opencv-python installed
- [ ] numpy installed
- [ ] PyYAML installed
- [ ] scipy installed
- [ ] Pillow installed
- [ ] ffmpeg-python installed

### Application
- [ ] main.py runs without errors
- [ ] Menu displays correctly
- [ ] All 5 menu options accessible
- [ ] Navigation works (select options, go back)

### Modules
- [ ] src/frame_data.py loads
- [ ] src/video_analyzer.py loads
- [ ] src/analysis_engine.py loads
- [ ] All classes instantiate correctly

### Data
- [ ] Blitzcrank frame data loaded (90+ moves)
- [ ] All moves have required fields
- [ ] Frame data searches work
- [ ] Character selection works

### Tests
- [ ] tests.py runs without errors
- [ ] All 12+ tests pass
- [ ] No warnings or deprecations

### Features
- [ ] Frame data browser works
- [ ] Search functionality works
- [ ] Tips display correctly
- [ ] Character list shows all 11 champions

---

## 🎮 Ready to Analyze?

Once all checkboxes are checked, you're ready to:

1. **Analyze videos** with option 1
2. **Learn move data** with option 3
3. **Study strategies** with option 4
4. **Get recommendations** from analysis

---

## 💻 Command Reference

### Essential Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python tests.py

# Start application
python main.py

# Check Python version
python --version

# Check FFmpeg
ffmpeg -version

# List installed packages
pip list
```

### Troubleshooting Commands
```bash
# Force reinstall all packages
pip install -r requirements.txt --force-reinstall

# Upgrade pip
pip install --upgrade pip

# Check if modules can be imported
python -c "import cv2, numpy, yaml; print('OK')"

# Run with verbose output
python main.py --verbose
```

---

## 🚀 Post-Installation

### First Time Setup
1. [ ] Read QUICKSTART.md
2. [ ] Run python tests.py (verify all pass)
3. [ ] Launch python main.py
4. [ ] Explore menu options 2, 3, 4
5. [ ] Prepare a video file for analysis

### Your First Analysis
1. [ ] Have video file ready (MP4 format)
2. [ ] Run python main.py
3. [ ] Select option 1 (Analyze)
4. [ ] Choose video file
5. [ ] Select characters and mode
6. [ ] Review analysis report
7. [ ] Read recommendations

### Next Steps
1. [ ] Analyze 2-3 matches
2. [ ] Study Blitzcrank frame data
3. [ ] Apply tips to your gameplay
4. [ ] Track improvement over time

---

## ✨ System Requirements Summary

| Component | Requirement | Check |
|-----------|-------------|-------|
| Python | 3.8+ | ✓ |
| FFmpeg | Latest | ✓ |
| RAM | 2GB+ | ✓ |
| Disk | 500MB+ | ✓ |
| OS | Windows/Mac/Linux | ✓ |
| Internet | For pip install | ✓ |

---

## 📞 Still Having Issues?

### Check These First
1. [ ] Read QUICKSTART.md
2. [ ] Read README.md FAQ section
3. [ ] Check troubleshooting above
4. [ ] Verify all checklist items
5. [ ] Run tests.py again

### Common Solutions
- Restart terminal/computer after installing Python
- Use absolute paths for video files
- Ensure video is readable MP4 format
- Check that all packages installed correctly with `pip list`

---

## ✅ All Set!

Once you complete this checklist, you're ready to:

🎮 **Analyze fighting game videos**  
📊 **View complete frame data**  
💡 **Get strategy recommendations**  
📈 **Track player improvement**  

**Next step**: Run `python main.py` and explore! 🚀

---

**Version**: 1.0  
**Last Updated**: January 2026  
**Status**: ✅ Complete
