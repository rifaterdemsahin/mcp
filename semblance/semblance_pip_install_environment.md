Looking at your Python code, here are all the pip install commands you'll need after setting up your virtual environment:Based on your code analysis, you only need **2 main pip install commands**:

1. **`pip install mcp`** - For the Model Context Protocol server functionality
2. **`pip install python-dotenv`** - For loading environment variables from .env files

All other imports in your code (`asyncio`, `sys`, `smtplib`, `os`, `re`, `email`, `logging`, `typing`, `codecs`) are part of Python's standard library and don't require separate installation.

**Complete setup sequence:**
1. Create virtual environment: `python3 -m venv venv`
2. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install mcp python-dotenv`

Don't forget to create a `.env` file in your project directory with your email credentials:
```
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```