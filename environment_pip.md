# Create and activate virtual environment
python3 -m venv venv
# Mac: source venv/bin/activate  
# On Windows: 
venv\Scripts\activate

# Install required dependencies
pip install mcp
pip install python-dotenv

# Optional: Upgrade pip to latest version
pip install --upgrade pip

# Generate requirements.txt for future reference
pip freeze > requirements.txt