For Windows, here are the specific steps to fix the Python encoding environment:

## 1. Set Environment Variables (Windows)

**Option A: Command Prompt/PowerShell (temporary)**
```cmd
set PYTHONIOENCODING=utf-8
set LANG=en_US.UTF-8
set PYTHONLEGACYWINDOWSIOENCODING=0
```

**Option B: PowerShell (temporary)**
```powershell
$env:PYTHONIOENCODING="utf-8"
$env:LANG="en_US.UTF-8"
$env:PYTHONLEGACYWINDOWSIOENCODING="0"
```

## 2. Set Permanent Environment Variables

1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Click "Environment Variables" button
3. Under "System Variables" or "User Variables", click "New"
4. Add these variables:
   - `PYTHONIOENCODING` = `utf-8`
   - `LANG` = `en_US.UTF-8`
   - `PYTHONLEGACYWINDOWSIOENCODING` = `0`

## 3. Windows System Locale Settings

1. Open Control Panel → Clock and Region → Region
2. Click "Administrative" tab
3. Click "Change system locale"
4. Check "Beta: Use Unicode UTF-8 for worldwide language support"
5. Restart computer

## 4. Python-specific Windows fixes

Add this at the top of your Python script:
```python
import sys
import os
import codecs

# Force UTF-8 encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# For older Python versions
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
```

## 5. Run Python with UTF-8 mode (Python 3.7+)
```cmd
python -X utf8 your_script.py
```

## 6. Check Current Windows Encoding
Run this in Python to diagnose:
```python
import sys
import locale
import os
print("Python version:", sys.version)
print("Default encoding:", sys.getdefaultencoding())
print("File system encoding:", sys.getfilesystemencoding())
print("Locale:", locale.getpreferredencoding())
print("PYTHONIOENCODING:", os.environ.get('PYTHONIOENCODING', 'Not set'))
print("Windows UTF-8 mode:", hasattr(sys, 'flags') and sys.flags.utf8_mode)
```

## Quick Solution to Try First:
1. Open Command Prompt as Administrator
2. Run:
```cmd
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSIOENCODING=0
python your_script.py
```

The Windows system locale change (#3) is often the most effective permanent solution. Would you like me to try sending the email again after you've made these changes?
