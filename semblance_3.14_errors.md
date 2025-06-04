The issue is clear now - you're using Python 3.14.0b2 (beta version) which is too new for the current ecosystem. The Rust bindings are failing because they don't support Python 3.14 yet. Here are your options:**The problem:** You're using Python 3.14.0b2 (beta), which is too bleeding-edge. The Rust ecosystem hasn't caught up with Python 3.14 support yet.

**RECOMMENDED SOLUTION:**

1. **Check what Python versions you have:**
   ```powershell
   py -0
   ```

2. **Create a new environment with Python 3.12 or 3.11:**
   ```powershell
   # Deactivate current environment
   deactivate
   
   # Try Python 3.12 first
   py -3.12 -m venv mcp_env_stable
   
   # If 3.12 isn't available, try 3.11
   py -3.11 -m venv mcp_env_stable
   
   # Activate the new environment
   mcp_env_stable\Scripts\activate
   
   # Verify version
   python --version
   
   # Install packages
   pip install --upgrade pip
   pip install mcp python-dotenv
   ```

3. **If you don't have Python 3.12 installed:**
   - Download Python 3.12.8 from: https://www.python.org/downloads/release/python-3128/
   - Install it alongside your current Python 3.14
   - Then follow step 2

**Why Python 3.14 beta doesn't work:**
- It's a beta version with breaking changes
- Rust libraries (pydantic-core uses Rust) haven't updated their bindings yet
- The `PyUnicode_DATA` function was likely removed or changed in Python 3.14
- Production libraries need time to catch up with new Python versions

**For your MCP server project, Python 3.12 is perfect** - it's stable, well-supported, and has excellent package compatibility.

Run `py -0` first to see what versions you have available, then create a new environment with a stable Python version.