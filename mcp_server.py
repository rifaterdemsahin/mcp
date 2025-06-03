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
from types import SimpleNamespace

# Load environment variables from .env file
load_dotenv()

# Create a server instance
server = Server("demo-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools with JSON Schema validation."""
    return [
        types.Tool(
            name="echo",
            description="Echo back the input text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to echo back"}
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
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
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
                    },
                    "message": {
                        "type": "string",
                        "description": "The body of the birthday message"
                    }
                },
                "required": ["to_email", "message"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    if name == "echo":
        text = arguments.get("text", "") if arguments else ""
        return [types.TextContent(type="text", text=f"Echo: {text}")]
    
    elif name == "add_numbers":
        if not arguments:
            raise ValueError("Missing arguments")
        result = arguments["a"] + arguments["b"]
        return [types.TextContent(type="text", text=f"Result: {arguments['a']} + {arguments['b']} = {result}")]
    
    elif name == "send_birthday_email":
        if not arguments:
            raise ValueError("Missing arguments")
        
        to_email = arguments["to_email"]
        subject = arguments.get("subject", "🎉 Happy Birthday! Party Time! 🎂")
        message = arguments["message"]  # Now required and explicitly used

        EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'info@pexabo.com')
        EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your-default-password')
        
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg.set_content(message, charset='utf-8')
        
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            return [types.TextContent(
                type="text", 
                text=f"🎉 Birthday email sent to {to_email}! 🎂\n📧 Subject: {subject}"
            )]
        except Exception as e:
            return [types.TextContent(
                type="text", 
                text=f"❌ Email failed: {str(e)}"
            )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    print("Debug: Preparing notification_options", file=sys.stderr)
    
    notification_options = SimpleNamespace(tools_changed=False)
    
    print(f"Debug: Calling get_capabilities with notification_options={notification_options}", 
          file=sys.stderr)
    
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
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
