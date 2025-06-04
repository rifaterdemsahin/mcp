I can help you recreate that virtual environment setup. Here's a step-by-step guide to recreate the MCP virtual environment with the proper encoding settings:The guide above recreates your MCP virtual environment setup with proper UTF-8 encoding configuration. The encoding settings you applied are particularly important for resolving the type of ASCII encoding errors we encountered with the email function.

Key points about your setup:
- You have a virtual environment named `mcp_env` in `C:\projects\mcp`
- Python-dotenv is installed for environment variable management
- UTF-8 encoding is properly configured to handle international characters
- The `PYTHONLEGACYWINDOWSIOENCODING=0` setting ensures modern Unicode handling

These encoding settings should help resolve the character encoding issues that were preventing the email function from working properly. The non-breaking space character (`\xa0`) error we saw earlier is exactly the type of issue these UTF-8 settings are designed to fix.

# MCP Virtual Environment Setup

## Step 1: Create the Project Directory
```powershell
# Navigate to your projects directory or create it
mkdir C:\projects\mcp
cd C:\projects\mcp
```

## Step 2: Create Virtual Environment
```powershell
# Create virtual environment named 'mcp_env'
python -m venv mcp_env

# Activate the virtual environment
.\mcp_env\Scripts\Activate.ps1
```

## Step 3: Install Required Packages
```powershell
# Install python-dotenv (as shown in your output)
pip install python-dotenv

# Optional: Upgrade pip to latest version
python.exe -m pip install --upgrade pip
```

## Step 4: Set Encoding Environment Variables
```powershell
# Method 1: Using set command (Windows CMD style - works in PowerShell)
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSIOENCODING=0

# Method 2: Using PowerShell environment variables (recommended for PowerShell)
$env:PYTHONIOENCODING="utf-8"
$env:LANG="en_US.UTF-8"
$env:PYTHONLEGACYWINDOWSIOENCODING="0"
```

## Step 5: Verify Environment
```powershell
# Check that you're in the virtual environment
# Your prompt should show: (mcp_env) PS C:\projects\mcp>

# Verify environment variables
echo $env:PYTHONIOENCODING
echo $env:LANG
echo $env:PYTHONLEGACYWINDOWSIOENCODING

# Check installed packages
pip list
```

## What These Environment Variables Do:

- **PYTHONIOENCODING=utf-8**: Forces Python to use UTF-8 encoding for input/output operations
- **LANG=en_US.UTF-8**: Sets the system locale to use UTF-8 encoding
- **PYTHONLEGACYWINDOWSIOENCODING=0**: Disables legacy Windows I/O encoding behavior in Python 3.6+

## To Make Environment Variables Persistent:
If you want these settings to persist across sessions, add them to your PowerShell profile:

```powershell
# Edit your PowerShell profile
notepad $PROFILE

# Add these lines to the profile:
$env:PYTHONIOENCODING="utf-8"
$env:LANG="en_US.UTF-8"
$env:PYTHONLEGACYWINDOWSIOENCODING="0"
```

## Reactivating the Environment:
```powershell
# To activate the environment in future sessions:
cd C:\projects\mcp
.\mcp_env\Scripts\Activate.ps1
```

This setup should resolve encoding issues you might encounter when working with MCP servers that handle international characters or special symbols.

---


# Fixing Virtual Environment Creation Error

## Error Analysis
The error `Unable to copy 'venvlauncher.exe' to 'python.exe'` typically occurs due to:
- File permissions issues
- Antivirus software blocking file operations
- Existing corrupted virtual environment
- Windows file system locks

## Solution 1: Run PowerShell as Administrator
```powershell
# Right-click PowerShell and select "Run as Administrator"
# Then navigate to your project directory
cd C:\projects\mcp

# Try creating the virtual environment again
python -m venv mcp_env
```

## Solution 2: Clean Up and Retry
```powershell
# Remove any existing mcp_env directory
Remove-Item -Recurse -Force mcp_env -ErrorAction SilentlyContinue

# Wait a moment, then try again
python -m venv mcp_env
```

## Solution 3: Use Alternative Virtual Environment Tools
```powershell
# Option A: Use virtualenv instead of venv
pip install virtualenv
virtualenv mcp_env

# Option B: Use conda if you have it installed
conda create -n mcp_env python=3.14
conda activate mcp_env
```

## Solution 4: Temporarily Disable Antivirus
```powershell
# Temporarily disable real-time protection in Windows Defender or your antivirus
# Then try creating the virtual environment
python -m venv mcp_env
# Remember to re-enable protection afterwards
```

## Solution 5: Use Different Directory
```powershell
# Try creating in a different location first
cd C:\temp
mkdir mcp_test
cd mcp_test
python -m venv test_env

# If this works, the issue is with the C:\projects\mcp directory permissions
```

## Solution 6: Check Python Installation
```powershell
# Verify Python installation
python --version
where python

# If using multiple Python versions, be specific
py -3.14 -m venv mcp_env
```

## Solution 7: Alternative Approach with Copy Options
```powershell
# Try with symlinks disabled (sometimes helps on Windows)
python -m venv --copies mcp_env
```

## Solution 8: Directory Permissions Fix
```powershell
# Check and fix directory permissions
icacls C:\projects\mcp /grant %USERNAME%:F /T

# Then try creating the virtual environment
python -m venv mcp_env
```

## Solution 9: Safe Mode Creation
```powershell
# Create directory manually first
mkdir mcp_env

# Try with explicit paths
python -m venv C:\projects\mcp\mcp_env --clear
```

## After Successful Creation:
```powershell
# Activate the environment
.\mcp_env\Scripts\Activate.ps1

# Install required packages
pip install python-dotenv

# Set encoding variables
$env:PYTHONIOENCODING="utf-8"
$env:LANG="en_US.UTF-8"
$env:PYTHONLEGACYWINDOWSIOENCODING="0"
```

## Prevention for Future
- Always run PowerShell as Administrator when creating virtual environments
- Add Python and project directories to antivirus exclusions
- Use shorter path names when possible
- Keep Python installation up to date

---

No, the `python -m venv` command doesn't have a direct UTF-8 parameter option. The UTF-8 encoding settings we discussed earlier are environment variables that affect how Python handles text, not arguments for the venv creation itself.

However, you can set the encoding environment variables **before** creating the virtual environment:

```powershell
# Set UTF-8 encoding first
$env:PYTHONIOENCODING="utf-8"
$env:LANG="en_US.UTF-8" 
$env:PYTHONLEGACYWINDOWSIOENCODING="0"

# Then create the virtual environment
python -m venv mcp_env
```

The `python -m venv` command options are limited to:

```powershell
# Available venv options:
python -m venv --help

# Common useful options:
python -m venv mcp_env                    # Basic creation
python -m venv --clear mcp_env           # Clear if exists
python -m venv --copies mcp_env          # Use copies instead of symlinks
python -m venv --system-site-packages mcp_env  # Include system packages
```

The encoding issue you encountered with the email function happens **after** the virtual environment is created and activated - that's when you need the UTF-8 environment variables set. The venv creation error you're seeing is likely a Windows permissions issue, not an encoding issue.

Try this sequence:

```powershell
# Run as Administrator, then:
$env:PYTHONIOENCODING="utf-8"
$env:PYTHONLEGACYWINDOWSIOENCODING="0"
python -m venv --copies mcp_env
```

The `--copies` flag often helps with Windows permission issues.


---

This error indicates there's an existing virtual environment with locked files (likely because it's currently active or has processes running). Here's how to fix this:

## Solution Steps:

### Step 1: Deactivate any active environment
```powershell
# If you see (mcp_env) in your prompt, deactivate first
deactivate
```

### Step 2: Force remove the existing directory
```powershell
# Run PowerShell as Administrator, then:
Remove-Item -Path "C:\projects\mcp\mcp_env" -Recurse -Force -ErrorAction SilentlyContinue

# Wait a few seconds for file handles to release
Start-Sleep -Seconds 3
```

### Step 3: Alternative removal methods if Step 2 fails:
```powershell
# Method A: Use robocopy to delete (sometimes works when Remove-Item fails)
mkdir C:\temp\empty
robocopy C:\temp\empty C:\projects\mcp\mcp_env /mir /r:0 /w:0
rmdir C:\projects\mcp\mcp_env

# Method B: Use takeown and icacls to gain full control
takeown /f "C:\projects\mcp\mcp_env" /r /d y
icacls "C:\projects\mcp\mcp_env" /grant administrators:F /t
Remove-Item -Path "C:\projects\mcp\mcp_env" -Recurse -Force
```

### Step 4: Create fresh virtual environment
```powershell
# Set encoding variables first
$env:PYTHONIOENCODING="utf-8"
$env:PYTHONLEGACYWINDOWSIOENCODING="0"

# Create new virtual environment
python -m venv mcp_env
```

### Step 5: If still having issues, try different location temporarily:
```powershell
# Create in a simpler path first
cd C:\
mkdir temp_mcp
cd temp_mcp
python -m venv mcp_env

# Then move it if successful
Move-Item C:\temp_mcp\mcp_env C:\projects\mcp\mcp_env
```

The `.pyd` file error specifically indicates that Python extension modules are locked, which usually means:
1. The virtual environment is still active somewhere
2. A Python process is still running
3. An IDE or editor has the environment locked

Try **Step 1 and 2** first - that solves most cases. Make sure to run PowerShell as Administrator for the removal commands.