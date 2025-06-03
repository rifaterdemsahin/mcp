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
                capabilities=server.get_capabilities(
                    notification_options=types.ServerNotificationOptions(
                        tools_changed=True,
                        resources_changed=True,
                        prompts_changed=True,
                    ),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())