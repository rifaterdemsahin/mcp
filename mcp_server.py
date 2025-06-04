#!/usr/bin/env python3

import asyncio
import sys
import smtplib
import os
import re
from email.message import EmailMessage
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from dotenv import load_dotenv
from types import SimpleNamespace
import logging
from typing import Dict, List, Optional


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


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger('demo-server')

# Load environment variables
load_dotenv()
logger.debug("Loaded environment variables from .env file")

# Create a server instance
server = Server("demo-server")
logger.debug("Initialized server instance: demo-server")

def remove_non_ascii(text: str) -> str:
    """Remove non-ASCII characters from the input text."""
    logger.debug("Removing non-ASCII characters from text: %s", text[:50])
    return re.sub(r'[^\x00-\x7F]+', '', text)

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available tools with JSON Schema validation."""
    logger.debug("Listing available tools")
    tools = [
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
                        "default": "Happy Birthday! Party Time!"
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
    logger.debug("Returning %d tools", len(tools))
    return tools

async def send_birthday_email(to_email: str, subject: str, message: str) -> List[types.TextContent]:
    """Send a birthday email and return the result as TextContent."""
    logger.debug("Preparing to send email to: %s, subject: %s", to_email, subject)
    
    # Normalize message and subject
    message = message.replace('\xa0', ' ').replace('\r\n', '\n').replace('\r', '\n')
    subject_clean = remove_non_ascii(subject)
    message_clean = remove_non_ascii(message)
    
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'info@pexabo.com')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your-default-password')
    
    msg = EmailMessage()
    msg['Subject'] = subject_clean
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(message_clean.encode('utf-8', errors='ignore').decode('utf-8'), charset='utf-8')
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            logger.debug("Logging into SMTP server")
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            logger.info("Successfully sent email to %s", to_email)
            return [types.TextContent(
                type="text",
                text=f"Birthday email sent to {to_email}!\nSubject: {subject_clean}"
            )]
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP authentication failed")
        return [types.TextContent(type="text", text="Email failed: Authentication error")]
    except smtplib.SMTPException as e:
        logger.error("SMTP error occurred: %s", str(e))
        return [types.TextContent(type="text", text=f"Email failed: {str(e)}")]
    except Exception as e:
        logger.exception("Unexpected error while sending email")
        return [types.TextContent(type="text", text=f"Email failed: {str(e)}")]

# Tool handler dispatch table
TOOL_HANDLERS = {
    "echo": lambda args: [types.TextContent(type="text", text=f"Echo: {args.get('text', '')}")],
    "add_numbers": lambda args: [types.TextContent(
        type="text",
        text=f"Result: {args['a']} + {args['b']} = {args['a'] + args['b']}"
    )],
    "send_birthday_email": lambda args: send_birthday_email(
        args["to_email"],
        args.get("subject", "Happy Birthday! Party Time!"),
        args["message"]
    )
}

@server.call_tool()
async def handle_call_tool(name: str, arguments: Optional[Dict]) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests using a dispatch table."""
    logger.debug("Handling tool call: %s with arguments: %s", name, arguments)
    
    if not arguments:
        logger.error("Missing arguments for tool: %s", name)
        raise ValueError("Missing arguments")
    
    handler = TOOL_HANDLERS.get(name)
    if not handler:
        logger.error("Unknown tool: %s", name)
        raise ValueError(f"Unknown tool: {name}")
    
    try:
        result = await (handler(arguments) if asyncio.iscoroutinefunction(handler) else handler(arguments))
        logger.debug("Tool %s executed successfully", name)
        return result
    except KeyError as e:
        logger.error("Invalid arguments for tool %s: %s", name, str(e))
        raise ValueError(f"Invalid arguments: {str(e)}")
    except Exception as e:
        logger.exception("Error executing tool %s", name)
        raise

async def main():
    logger.debug("Starting main function")
    notification_options = SimpleNamespace(tools_changed=False)
    logger.debug("Notification options: %s", vars(notification_options))
    
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            logger.debug("Starting server with read_stream=%s, write_stream=%s", read_stream, write_stream)
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
            logger.info("Server shutdown successfully")
    except Exception as e:
        logger.exception("Fatal error in main")
        raise

if __name__ == "__main__":
    logger.debug("Starting application")
    asyncio.run(main())