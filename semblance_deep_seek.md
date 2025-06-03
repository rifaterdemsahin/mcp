2025-06-03T20:54:12.969Z [demo-server] [info] Initializing server...
2025-06-03T20:54:12.991Z [demo-server] [info] Server started and connected successfully
2025-06-03T20:54:12.993Z [demo-server] [info] Message from client: {"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"claude-ai","version":"0.1.0"}},"jsonrpc":"2.0","id":0}
  File "C:\projects\mcp\mcp_server.py", line 117
    nucl�aire
             ^
IndentationError: unindent does not match any outer indentation level
2025-06-03T20:54:13.331Z [demo-server] [info] Server transport closed
2025-06-03T20:54:13.331Z [demo-server] [info] Client transport closed
2025-06-03T20:54:13.332Z [demo-server] [info] Server transport closed unexpectedly, this is likely due to the process exiting early. If you are developing this MCP server you can add output to stderr (i.e. `console.error('...')` in JavaScript, `print('...', file=sys.stderr)` in python) and it will appear in this log.
2025-06-03T20:54:13.332Z [demo-server] [error] Server disconnected. For troubleshooting guidance, please visit our [debugging documentation](https://modelcontextprotocol.io/docs/tools/debugging) {"context":"connection"}
2025-06-03T20:54:13.333Z [demo-server] [info] Client transport closed
2025-06-03T20:55:02.828Z [demo-server] [info] Initializing server...
2025-06-03T20:55:02.881Z [demo-server] [info] Server started and connected successfully
2025-06-03T20:55:02.883Z [demo-server] [info] Message from client: {"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"claude-ai","version":"0.1.0"}},"jsonrpc":"2.0","id":0}
Debug: Preparing notification_options
Debug: Calling get_capabilities with notification_options={'tools_changed': False}
Debug: Error in main: unhandled errors in a TaskGroup (1 sub-exception)
  + Exception Group Traceback (most recent call last):
  |   File "C:\projects\mcp\mcp_server.py", line 217, in <module>
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
  |   File "C:\projects\mcp\mcp_server.py", line 198, in main
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
    |   File "C:\projects\mcp\mcp_server.py", line 206, in main
    |     capabilities=server.get_capabilities(
    |                  ~~~~~~~~~~~~~~~~~~~~~~~^
    |         notification_options=notification_options,
    |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |         experimental_capabilities={}
    |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |     ),
    |     ^
    |   File "C:\projects\mcp\mcp_env\Lib\site-packages\mcp\server\lowlevel\server.py", line 205, in get_capabilities
    |     listChanged=notification_options.tools_changed
    |                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    | AttributeError: 'dict' object has no attribute 'tools_changed'
    +------------------------------------
2025-06-03T20:55:04.275Z [demo-server] [info] Server transport closed
2025-06-03T20:55:04.276Z [demo-server] [info] Client transport closed
2025-06-03T20:55:04.276Z [demo-server] [info] Server transport closed unexpectedly, this is likely due to the process exiting early. If you are developing this MCP server you can add output to stderr (i.e. `console.error('...')` in JavaScript, `print('...', file=sys.stderr)` in python) and it will appear in this log.
2025-06-03T20:55:04.276Z [demo-server] [error] Server disconnected. For troubleshooting guidance, please visit our [debugging documentation](https://modelcontextprotocol.io/docs/tools/debugging) {"context":"connection"}
2025-06-03T20:55:04.277Z [demo-server] [info] Client transport closed


---


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
    # Debug: Print notification_options type
    print("Debug: Preparing notification_options", file=sys.stderr)
    try:
        # Try using a dictionary with tools_changed
        notification_options = {"tools_changed": False}
        
        # Run the server using stdin/stdout streams
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            print(f"Debug: Calling get_capabilities with notification_options={notification_options}", file=sys.stderr)
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="demo-server",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=notification_options,
                        experimental_capabilities={}
                    ),
                ),
            )
    except Exception as e:
        print(f"Debug: Error in main: {str(e)}", file=sys.stderr)
        raise

if __name__ == "__main__":
    asyncio.run(main())