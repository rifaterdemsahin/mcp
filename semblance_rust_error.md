The error you're encountering is due to a version compatibility issue between Python 3.14 and PyO3 (a Rust-Python binding library used by pydantic-core). Here are several solutions to fix this:**Recommended Solution (Try in this order):**

1. **Quick Fix - Set compatibility flag:**
   ```powershell
   $env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY = "1"
   pip install mcp python-dotenv
   ```

2. **If that doesn't work, try pre-built wheels:**
   ```bash
   pip install --only-binary=all mcp python-dotenv
   ```

3. **Most reliable - Use Python 3.12:**
   Since Python 3.14 is very new and many packages haven't caught up with compatibility, I'd recommend creating a new virtual environment with Python 3.12:
   
   ```powershell
   # Deactivate current environment
   deactivate
   
   # Create new environment with Python 3.12
   py -3.12 -m venv mcp_env_312
   mcp_env_312\Scripts\activate
   
   # Install packages
   pip install --upgrade pip
   pip install mcp python-dotenv
   ```

**Why this happens:**
- Python 3.14 is very recent and cutting-edge
- The `pydantic-core` library (dependency of `mcp`) uses Rust bindings via PyO3
- PyO3 v0.24.1 doesn't officially support Python 3.14 yet
- The library tries to compile from source and fails

**Best long-term approach:** Use Python 3.12 for production projects as it has the best package compatibility while still being modern and supported.

Try the first solution first - it should work for your immediate needs!