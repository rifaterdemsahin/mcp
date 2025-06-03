2025-06-03T20:42:52.122Z [demo-server] [info] Initializing server...
2025-06-03T20:42:52.144Z [demo-server] [info] Server started and connected successfully
2025-06-03T20:42:52.146Z [demo-server] [info] Message from client: {"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"claude-ai","version":"0.1.0"}},"jsonrpc":"2.0","id":0}
  + Exception Group Traceback (most recent call last):
  |   File "C:\projects\mcp\mcp_server.py", line 202, in <module>
  |     asyncio.run(main())
  |     ~~~~~~~~~~~^^^^^^^^
  |   File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.1008.0_x64__qbz5n2kfra8p0\Lib\asyncio\runners.py", line 195, in run
  |     return runner.run(main)
  |            ~~~~~~~~~~^^^^^^
  |   File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.1008.0_x64__qbz5n2kfra8p0\Lib\asyncio\runners.py", line 118, in run
  |     return self._loop.run_until_complete(task)
  |            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  |   File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.1008.0_x64__qbz5n2kfra8p0\Lib\asyncio\base_events.py", line 719, in run_until_complete
  |     return future.result()
  |            ~~~~~~~~~~~~~^^
  |   File "C:\projects\mcp\mcp_server.py", line 190, in main
  |     async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
  |                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  |   File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.1008.0_x64__qbz5n2kfra8p0\Lib\contextlib.py", line 235, in __aexit__
  |     await self.gen.athrow(value)
  |   File "C:\projects\mcp\mcp_env\Lib\site-packages\mcp\server\stdio.py", line 87, in stdio_server
  |     async with anyio.create_task_group() as tg:
  |                ~~~~~~~~~~~~~~~~~~~~~~~^^
  |   File "C:\projects\mcp\mcp_env\Lib\site-packages\anyio\_backends\_asyncio.py", line 772, in __aexit__
  |     raise BaseExceptionGroup(
  |         "unhandled errors in a TaskGroup", self._exceptions
  |     ) from None
  | ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
  +-+---------------- 1 ----------------
    | Traceback (most recent call last):
    |   File "C:\projects\mcp\mcp_env\Lib\site-packages\mcp\server\stdio.py", line 90, in stdio_server
    |     yield read_stream, write_stream
    |   File "C:\projects\mcp\mcp_server.py", line 197, in main
    |     capabilities=server.get_capabilities(),
    |                  ~~~~~~~~~~~~~~~~~~~~~~~^^
    | TypeError: Server.get_capabilities() missing 2 required positional arguments: 'notification_options' and 'experimental_capabilities'
    +------------------------------------
2025-06-03T20:42:53.059Z [demo-server] [info] Server transport closed
2025-06-03T20:42:53.059Z [demo-server] [info] Client transport closed
2025-06-03T20:42:53.060Z [demo-server] [info] Server transport closed unexpectedly, this is likely due to the process exiting early. If you are developing this MCP server you can add output to stderr (i.e. `console.error('...')` in JavaScript, `print('...', file=sys.stderr)` in python) and it will appear in this log.
2025-06-03T20:42:53.060Z [demo-server] [error] Server disconnected. For troubleshooting guidance, please visit our [debugging documentation](https://modelcontextprotocol.io/docs/tools/debugging) {"context":"connection"}
2025-06-03T20:42:53.061Z [demo-server] [info] Client transport closed


---
#!/usr/bin/env python3

import asyncio
import sys
import smtplib
from email.message import EmailMessage
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types


# Create a server instance
server = Server("demo-server")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="echo",
            description="Echo back the input text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to echo back",
                    }
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="add_numbers",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number",
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number",
                    }
                },
                "required": ["a", "b"],
            },
        ),
        types.Tool(
            name="send_birthday_email",
            description="Send a birthday email with emojis and Japanese greetings",
            inputSchema={
                "type": "object",
                "properties": {
                    "to_email": {
                        "type": "string",
                        "description": "Recipient email address",
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line",
                        "default": "🎉 Happy Birthday! Party Time! 🎂"
                    }
                },
                "required": ["to_email"],
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    """
    if name == "echo":
        text = arguments.get("text", "") if arguments else ""
        return [types.TextContent(type="text", text=f"Echo: {text}")]
    
    elif name == "add_numbers":
        if not arguments:
            raise ValueError("Missing arguments")
        
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        result = a + b
        return [types.TextContent(type="text", text=f"Result: {a} + {b} = {result}")]
    
    elif name == "send_birthday_email":
        if not arguments:
            raise ValueError("Missing arguments")
        
        to_email = arguments.get("to_email")
        subject = arguments.get("subject", "🎉 Happy Birthday! Party Time! 🎂")
        
        # Email configuration
        EMAIL_ADDRESS = 'info@pexabo.com'
        EMAIL_PASSWORD = 'ivxn scrz gvqa dyre'
        
        # Create email message
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        
        # Birthday message with emojis and Japanese greetings
        birthday_message = """🎉 HAPPY BIRTHDAY! 🎂
お誕生日おめでとうございます！🎌

Dear Birthday Star! ⭐

Wishing you the most amazing birthday ever! 🌟

May your special day be filled with:
🎁 Wonderful surprises
😄 Lots of laughter and joy  
🎊 Fun celebrations
💕 Love from friends and family
✨ Magical moments
😊 Happiness that lasts all year
📸 Unforgettable memories

Here's to another fantastic year ahead! 🥂

Hope your birthday is as awesome as you are! 🌈

Blow out those candles and make a wish! 🕯️💫

🎵 Happy Birthday to You! 🎵
🎵 Happy Birthday to You! 🎵
🎵 Happy Birthday Dear Friend! 🎵
🎵 Happy Birthday to You! 🎵

🎌 Japanese Birthday Greetings:
お誕生日おめでとうございます！(Otanjoubi omedetou gozaimasu!)
素敵な一年になりますように！🌸 (Suteki na ichinen ni narimasu you ni!)
Happy Birthday & May you have a wonderful year! 

🎋 Japanese Holiday Greetings:
新年明けましておめでとうございます！🎍 (Akemashite omedetou gozaimasu!)
今年もよろしくお願いします！⛩️ (Kotoshi mo yoroshiku onegaishimasu!)
Happy New Year & Please treat me favorably this year too!

春の季節、桜の花のように美しい日々でありますように！🌸
(Haru no kisetsu, sakura no hana no you ni utsukushii hibi de arimasu you ni!)
In spring season, may your days be as beautiful as cherry blossoms!

With warmest birthday wishes, 💝
Your MCP-powered friend 🐍💻

P.S. This birthday greeting was sent with love using MCP! 💖🎈

🎂🎉🎁🎊🌟⭐✨🎈💫🥳🎌🌸🎋
"""
        
        msg.set_content(birthday_message, charset='utf-8')
        
        try:
            # Send email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            
            return [types.TextContent(
                type="text", 
                text=f"🎉 Birthday email sent successfully to {to_email}! 🎂\n📧 Subject: {subject}\n✨ Birthday wishes delivered!"
            )]
            
        except Exception as e:
            return [types.TextContent(
                type="text", 
                text=f"❌ Failed to send birthday email: {str(e)}"
            )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="demo-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())

---

gRok

The error in your log indicates that the Server.get_capabilities() method is missing two required positional arguments: notification_options and experimental_capabilities. This suggests that the mcp library you're using has a version of the Server class that expects these arguments when calling get_capabilities().
Root Cause
The traceback shows the error occurs in the main function at this line:
python
capabilities=server.get_capabilities(),
The get_capabilities method in the Server class (from the mcp.server module) is defined to require notification_options and experimental_capabilities, but your code doesn't provide them.
Fix
To resolve this, you need to pass the required arguments to get_capabilities(). Based on the error, you can provide default values (e.g., empty dictionaries or appropriate defaults) if you're unsure of specific values, or check the mcp library documentation for the expected structure of these arguments.
Here's how you can modify the main function:
python
async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="demo-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options={},  # Provide default or appropriate value
                    experimental_capabilities={}  # Provide default or appropriate value
                ),
            ),
        )
Explanation
notification_options: This likely specifies options for server notifications (e.g., events or updates the server can send to the client). An empty dictionary {} might suffice if you don't need specific notification settings.
experimental_capabilities: This likely defines experimental features supported by the server. Again, an empty dictionary {} can be a safe default if you're not using experimental features.
Check the mcp library's documentation or source code for the Server.get_capabilities method to confirm the expected structure of these arguments. For example, they might expect specific keys or values (e.g., {"enabled": True} for notification_options).
Steps to Verify
Check mcp Library Documentation: Look for details on Server.get_capabilities in the library's documentation or source code (likely in mcp/server/__init__.py or similar). The Model Context Protocol (MCP) documentation at https://modelcontextprotocol.io might also provide guidance.
Inspect Library Version: Ensure the mcp library version you're using matches the expected API. Run pip show mcp to check the version, and verify compatibility with your code.
Test with Defaults: Use the modified code above with empty dictionaries as a quick fix. If it works, refine the arguments based on your needs or documentation.
Debugging: If the error persists, add debug output to stderr (as suggested in the log) to inspect the server's state:
python
import sys
print("Debug: Calling get_capabilities", file=sys.stderr)
Additional Notes
Client Message: The log shows a client (identified as claude-ai, version 0.1.0) sending an initialize request with protocolVersion: "2024-11-05". Ensure your server implementation is compatible with this protocol version.
Email Functionality: The send_birthday_email tool uses an email and password directly in the code, which is insecure. Consider using environment variables or a secure configuration method:
python
import os
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'info@pexabo.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your-default-password')
Error Handling: The server shuts down unexpectedly after the error. Ensure your main function or the mcp library handles exceptions gracefully to prevent abrupt termination.
If You Need Further Help
Share the version of the mcp library you're using (pip show mcp).
Provide any specific requirements for notification_options or experimental_capabilities if you know them.
Let me know if you want me to search for additional details about the mcp library or the Model Context Protocol.
Try the modified code and let me know if it resolves the issue or if you encounter further errors!


---

Setting up a .env file is straightforward, but I’ll guide you step-by-step to ensure it works seamlessly with your Python script (mcp_server.py) for securely managing email credentials. Below are detailed instructions for creating and configuring the .env file, installing the necessary python-dotenv library, and testing the setup. I’ll also address specific considerations for using Gmail with the send_birthday_email tool in your script.
Step-by-Step Guide to Setting Up the .env File
1. Install python-dotenv
The python-dotenv library is required to load environment variables from the .env file into your Python script. Install it using pip:
bash
pip install python-dotenv
Verify the installation:
bash
pip show python-dotenv
This should display details like the version number (e.g., 1.0.1 or similar). If it’s not installed, ensure your Python environment is active (e.g., if using a virtual environment, activate it first).
2. Create the .env File
In the same directory as your mcp_server.py script, create a new file named .env. You can do this:
On Windows: Use a text editor like Notepad or VS Code, or run:
bash
echo. > .env
On macOS/Linux: Use a text editor or run:
bash
touch .env
Open the .env file in a text editor and add the following content:
env
EMAIL_ADDRESS=info@pexabo.com
EMAIL_PASSWORD=your-secure-password
Replace the values:
EMAIL_ADDRESS: Use your actual email address (e.g., yourname@gmail.com if using Gmail).
EMAIL_PASSWORD: Use the appropriate password (see Gmail-specific instructions below for App Passwords if using Gmail with 2FA).
Save the .env file.
Example .env File:
env
EMAIL_ADDRESS=yourname@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
3. Gmail-Specific Setup (If Using Gmail)
Since your script uses smtp.gmail.com for sending emails, and Gmail often requires additional configuration (especially with 2FA), follow these steps:
If 2FA is Enabled (Recommended):
Go to your Google Account: myaccount.google.com.
Navigate to Security > 2-Step Verification.
Scroll to App passwords (you may need to enable 2FA if not already active).
Click App passwords, select Mail as the app, and choose your device (e.g., “Custom” or “Python Script”).
Generate the password (it will look like abcd efgh ijkl mnop).
Copy this 16-character App Password and use it as EMAIL_PASSWORD in the .env file.
env
EMAIL_ADDRESS=yourname@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
If 2FA is Not Enabled:
Go to Google Account > Security > Less secure app access.
Enable Allow less secure apps (not recommended for security reasons).
Use your regular Gmail password in the .env file:
env
EMAIL_ADDRESS=yourname@gmail.com
EMAIL_PASSWORD=your-gmail-password
Note: Google may block this if it detects unusual activity. Using an App Password with 2FA is safer and more reliable.
4. Secure the .env File
Add to .gitignore: If using Git, create or edit a .gitignore file in your project directory and add:
gitignore
.env
This prevents the .env file from being committed to version control, protecting your credentials.
File Permissions: Ensure the .env file is only readable by your user:
macOS/Linux:
bash
chmod 600 .env
Windows: Ensure the file is in a secure directory, and avoid sharing it.
5. Verify Your Python Script
Your script (from the previous response) already includes the necessary changes to load the .env file using python-dotenv. Confirm the following lines are present at the top:
python
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
And in the send_birthday_email tool, ensure the email configuration uses os.getenv:
python
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'info@pexabo.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your-default-password')
Note: The default values ('info@pexabo.com', 'your-default-password') are fallbacks. For production, consider removing them or setting secure defaults, as these will be used if the environment variables are not found.
6. Test the Setup
Directory Structure:
Ensure your project directory looks like this:
your_project/
├── mcp_server.py
├── .env
Run the Script:
bash
python3 mcp_server.py
This starts the MCP server. The .env file should be automatically loaded, and the email credentials will be used by the send_birthday_email tool.
Test the Email Tool:
If you have a client (e.g., claude-ai as mentioned in the logs), send a request to the send_birthday_email tool with a valid to_email (e.g., a test email address you control).
Example JSON-RPC request (for reference):
json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "call_tool",
  "params": {
    "name": "send_birthday_email",
    "arguments": {
      "to_email": "test@example.com",
      "subject": "🎉 Happy Birthday! 🎂"
    }
  }
}
Check if the email is sent successfully. You should see a response like:
🎉 Birthday email sent successfully to test@example.com! 🎂
📧 Subject: 🎉 Happy Birthday! 🎂
✨ Birthday wishes delivered!
If it fails, check the error message (e.g., for invalid credentials).
Debugging Tips:
If the email fails, add debug output to the send_birthday_email tool:
python
print(f"Debug: Attempting to send email with {EMAIL_ADDRESS}", file=sys.stderr)
Check the logs for errors (e.g., authentication failures).
Common issues:
Invalid App Password: Regenerate the App Password and update .env.
SMTP Errors: Ensure smtp.gmail.com:465 is accessible and 2FA settings are correct.
Missing .env: Verify the .env file is in the correct directory and loaded.
7. Troubleshooting
.env Not Loading:
Ensure python-dotenv is installed.
Verify the .env file is in the same directory as mcp_server.py.
Add a debug print to confirm loading:
python
print(f"Debug: EMAIL_ADDRESS={os.getenv('EMAIL_ADDRESS')}", file=sys.stderr)
Gmail Authentication Errors:
Double-check the App Password.
If using “Less secure apps,” ensure it’s enabled (not recommended).
Test SMTP separately:
python
import smtplib
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
        print("SMTP login successful")
except Exception as e:
    print(f"SMTP login failed: {e}")
File Permissions: If the .env file isn’t readable, check permissions (especially on macOS/Linux).
8. Optional: Manual Environment Variables
If you prefer not to use a .env file, you can set environment variables directly:
Windows (Command Prompt):
bash
set EMAIL_ADDRESS=yourname@gmail.com
set EMAIL_PASSWORD=abcd efgh ijkl mnop
python3 mcp_server.py
macOS/Linux:
bash
export EMAIL_ADDRESS=yourname@gmail.com
export EMAIL_PASSWORD=abcd efgh ijkl mnop
python3 mcp_server.py
This is less convenient for persistent use, so the .env file is recommended.
Example .env File (Final)
env
EMAIL_ADDRESS=yourname@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
Additional Notes
Security: Never share your .env file or App Password. If exposed, regenerate the App Password in your Google Account.
MCP Server: The .env setup only affects the email tool. The previous fix for get_capabilities (notification_options={}, experimental_capabilities={}) should resolve the server initialization error.
Testing Email: Use a disposable or test email address for to_email to avoid spamming real users during testing.
If you run into issues (e.g., SMTP errors, .env not loading, or server issues), share the specific error message or log, and I’ll help troubleshoot further. Let me know if you need assistance with any specific step or additional configuration!

---


Below is an example .env file to store the email credentials securely for the provided Python script. This file will hold the EMAIL_ADDRESS and EMAIL_PASSWORD environment variables used in the send_birthday_email tool.
.env File Content
env
EMAIL_ADDRESS=info@pexabo.com
EMAIL_PASSWORD=your-secure-password
Instructions
Create the .env File:
Save the above content in a file named .env in the same directory as your Python script (mcp_server.py).
Replace your-secure-password with the actual email password or app-specific password for your email service (e.g., Gmail requires an App Password if 2FA is enabled).
Update the Python Script:
To load the .env file, you need to use the python-dotenv library. Install it if you haven't already:
bash
pip install python-dotenv
Modify the Python script to load the .env file by adding the following at the top of your script, just below the imports:
python
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
Ensure the EMAIL_ADDRESS and EMAIL_PASSWORD lines in the send_birthday_email tool use os.getenv as already implemented:
python
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'info@pexabo.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your-default-password')
Security Notes:
Do not commit the .env file to version control (e.g., Git). Add .env to your .gitignore file to prevent accidental exposure.
For Gmail, if 2FA is enabled, generate an App Password from your Google Account settings and use it as EMAIL_PASSWORD.
The default values in os.getenv (e.g., 'info@pexabo.com', 'your-default-password') are fallbacks. Remove or replace them in production for security.
Example Directory Structure:
your_project/
├── mcp_server.py
├── .env
Running the Script:
After creating the .env file and updating the script with python-dotenv, run the script as usual:
bash
python3 mcp_server.py
The script will automatically load the credentials from the .env file.
Complete Updated Code (with .env Support)
For clarity, here’s the full script with the python-dotenv integration, incorporating the previous fix for get_capabilities:
python
#!/usr/bin/env python3

import asyncio
import sys
import smtplib
import os
from email.message import EmailMessage
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a server instance
server = Server("demo-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="echo",
            description="Echo back the input text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to echo back",
                    }
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="add_numbers",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number",
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number",
                    }
                },
                "required": ["a", "b"],
            },
        ),
        types.Tool(
            name="send_birthday_email",
            description="Send a birthday email with emojis and Japanese greetings",
            inputSchema={
                "type": "object",
                "properties": {
                    "to_email": {
                        "type": "string",
                        "description": "Recipient email address",
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line",
                        "default": "🎉 Happy Birthday! Party Time! 🎂"
                    }
                },
                "required": ["to_email"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    """
    if name == "echo":
        text = arguments.get("text", "") if arguments else ""
        return [types.TextContent(type="text", text=f"Echo: {text}")]
    
    elif name == "add_numbers":
        if not arguments:
            raise ValueError("Missing arguments")
        
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        result = a + b
        return [types.TextContent(type="text", text=f"Result: {a} + {b} = {result}")]
    
    elif name == "send_birthday_email":
        if not arguments:
            raise ValueError("Missing arguments")
        
        to_email = arguments.get("to_email")
        subject = arguments.get("subject", "🎉 Happy Birthday! Party Time! 🎂")
        
        # Email configuration using environment variables
        EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'info@pexabo.com')
        EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your-default-password')
        
        # Create email message
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        
        # Birthday message with emojis and Japanese greetings
        birthday_message = """🎉 HAPPY BIRTHDAY! 🎂
お誕生日おめでとうございます！🎌

Dear Birthday Star! ⭐

Wishing you the most amazing birthday ever! 🌟

May your special day be filled with:
🎁 Wonderful surprises
😄 Lots of laughter and joy  
🎊 Fun celebrations
💕 Love from friends and family
✨ Magical moments
😊 Happiness that lasts all year
📸 Unforgettable memories

Here's to another fantastic year ahead! 🥂

Hope your birthday is as awesome as you are! 🌈

Blow out those candles and make a wish! 🕯️💫

🎵 Happy Birthday to You! 🎵
🎵 Happy Birthday to You! 🎵
🎵 Happy Birthday Dear Friend! 🎵
🎵 Happy Birthday to You! 🎵

🎌 Japanese Birthday Greetings:
お誕生日おめでとうございます！(Otanjoubi omedetou gozaimasu!)
素敵な一年になりますように！🌸 (Suteki na ichinen ni narimasu you ni!)
Happy Birthday & May you have a wonderful year! 

🎋 Japanese Holiday Greetings:
新年明けましておめでとうございます！🎍 (Akemashite omedetou gozaimasu!)
今年もよろしくお願いします！⛩️ (Kotoshi mo yoroshiku onegaishimasu!)
Happy New Year & Please treat me favorably this year too!

春の季節、桜の花のように美しい日々でありますように！🌸
(Haru no kisetsu, sakura no hana no you ni utsukushii hibi de arimasu you ni!)
In spring season, may your days be as beautiful as cherry blossoms!

With warmest birthday wishes, 💝
Your MCP-powered friend 🐍💻

P.S. This birthday greeting was sent with love using MCP! 💖🎈

🎂🎉🎁🎊🌟⭐✨🎈💫🥳🎌🌸🎋
"""
        
        msg.set_content(birthday_message, charset='utf-8')
        
        try:
            # Send email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            
            return [types.TextContent(
                type="text", 
                text=f"🎉 Birthday email sent successfully to {to_email}! 🎂\n📧 Subject: {subject}\n✨ Birthday wishes delivered!"
            )]
            
        except Exception as e:
            return [types.TextContent(
                type="text", 
                text=f"❌ Failed to send birthday email: {str(e)}"
            )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="demo-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options={},  # Default empty dict for notification options
                    experimental_capabilities={}  # Default empty dict for experimental capabilities
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
Additional Notes
Gmail App Password: If using Gmail with 2FA, generate an App Password:
Go to your Google Account > Security > 2-Step Verification.
Select "App passwords," choose "Mail" and your device, then generate.
Use the generated password in the .env file as EMAIL_PASSWORD.
Testing: After setting up the .env file and updating the script, test the email functionality by calling the send_birthday_email tool with a valid to_email address.
MCP Library: The .env file only addresses email credentials. If you need specific values for notification_options or experimental_capabilities, check the mcp library documentation or share more details for further assistance.
Let me know if you need help setting up the .env file, testing, or resolving any other issues!