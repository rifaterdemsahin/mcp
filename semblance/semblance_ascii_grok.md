The encoding issue in the send_birthday_email function stems from the smtplib library's handling of non-ASCII characters, particularly when the email content or headers contain characters like emojis or non-breaking spaces (\xa0). Despite the remove_non_ascii function and setting charset='utf-8' in the EmailMessage, the error persists, indicating that the SMTP library or server configuration is enforcing ASCII encoding, likely due to how the email content is processed or transmitted.
Root Cause
The error 'ascii' codec can't encode character '\xa0' in position 21: ordinal not in range(128) suggests that a non-ASCII character (e.g., a non-breaking space or an emoji) is present in the email content or headers, and the SMTP library is attempting to encode it in ASCII, which only supports characters in the range 0–127. The remove_non_ascii function is not catching all problematic characters, or the email headers/content are being processed in a way that bypasses the UTF-8 encoding.
Analysis of Logs
The logs show successful execution of the tools/list method (IDs 5 and 6), confirming that the MCP server is operational and the tool definitions (including send_birthday_email) are correctly registered.
The resources/list and prompts/list methods (IDs 7 and 8) return "Method not found" errors, which is expected if these methods are not implemented.
The tools/call requests for send_birthday_email (IDs 9 and 10) fail with the same encoding error, pointing to a consistent issue in the email function.
The input for ID 9 includes a subject with emojis (MCP Server Status Update 🎉), which are stripped by remove_non_ascii, but the message body may still contain a non-breaking space (\xa0) from the newline formatting or editor input.
The input for ID 10 uses a plain subject (MCP Server Working), but the same error occurs, suggesting the issue is likely in the message body or an underlying configuration.
Suggested Fix
To resolve the encoding issue, we need to ensure that all parts of the email (subject, body, and headers) are properly encoded in UTF-8 and that no non-ASCII characters (like \xa0) sneak into the content. Additionally, we should explicitly handle the email content to avoid encoding mismatches.
Here’s an updated version of the send_birthday_email function with additional safeguards:
python
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
        subject = arguments.get("subject", "Happy Birthday! Party Time!")
        message = arguments["message"]

        # Replace non-breaking spaces and normalize newlines
        message = message.replace('\xa0', ' ').replace('\r\n', '\n').replace('\r', '\n')
        # Remove non-ASCII characters from subject and message
        subject_clean = re.sub(r'[^\x00-\x7F]+', '', subject)
        message_clean = re.sub(r'[^\x00-\x7F]+', '', message)

        EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'info@pexabo.com')
        EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your-default-password')
        
        msg = EmailMessage()
        msg['Subject'] = subject_clean
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        # Explicitly encode content as UTF-8
        msg.set_content(message_clean.encode('utf-8', errors='ignore').decode('utf-8'), charset='utf-8')
        
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            return [types.TextContent(
                type="text", 
                text=f"Birthday email sent to {to_email}!\nSubject: {subject_clean}"
            )]
        except Exception as e:
            return [types.TextContent(
                type="text", 
                text=f"Email failed: {str(e)}"
            )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")
Key Changes
Non-Breaking Space Handling: Explicitly replace \xa0 (non-breaking space) with a regular space and normalize newlines (\r\n or \r to \n) to prevent invisible characters from causing issues.
Explicit UTF-8 Encoding: Encode the message content as UTF-8 with errors='ignore' to strip any problematic characters, then decode back to a string for compatibility.
Simplified Default Subject: Removed emojis from the default subject in the function to avoid potential encoding issues, as they’re already stripped by remove_non_ascii.
Error Reporting: Maintains the same error reporting structure for consistency.
Additional Considerations
SMTP Server Configuration: Ensure that the SMTP server (e.g., smtp.gmail.com) is configured to accept UTF-8 encoded emails. Gmail supports UTF-8, but the issue may arise from the smtplib library’s default behavior. If the issue persists, consider using a library like email.mime.text.MIMEText for more control over encoding.
Environment Variables: Verify that EMAIL_ADDRESS and EMAIL_PASSWORD are correctly set in the .env file. Incorrect credentials could cause unrelated SMTP errors, though the logs point to encoding as the primary issue.
Input Validation: The to_email field should be validated for proper email format (e.g., using a regex like r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'). This wasn’t the issue here, but it’s a good practice.
Debugging Non-ASCII Characters: Add logging to inspect the raw message and subject before cleaning to identify the exact source of \xa0. For example:
python
print(f"Debug: Raw subject: {repr(subject)}", file=sys.stderr)
print(f"Debug: Raw message: {repr(message)}", file=sys.stderr)
Testing the Fix
To test the updated function:
Update the handle_call_tool function with the code above.
Ensure the .env file contains valid EMAIL_ADDRESS and EMAIL_PASSWORD.
Send a test request with a simple message and subject, avoiding emojis or special characters:
json
{
    "method": "tools/call",
    "params": {
        "name": "send_birthday_email",
        "arguments": {
            "to_email": "iletisim@vebende.com",
            "subject": "Test Email",
            "message": "This is a test email from the MCP server."
        }
    },
    "jsonrpc": "2.0",
    "id": 11
}
Check the server logs for the response and verify if the email is sent successfully.
If the Issue Persists
If the encoding error continues:
Inspect Input Source: The \xa0 may be introduced by the client sending the JSON request (e.g., a text editor or UI inserting non-breaking spaces). Log the raw input (arguments) to confirm.
Use Alternative Libraries: Consider using aiosmtplib for async SMTP operations, which may handle encoding better:
python
import aiosmtplib
async def send_email(to_email, subject, message):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(message, charset='utf-8')
    await aiosmtplib.send(msg, hostname='smtp.gmail.com', port=465, username=EMAIL_ADDRESS, password=EMAIL_PASSWORD, use_tls=True)
Check SMTP Server: If using a different SMTP server, verify its encoding requirements. Some servers may require explicit MIME encoding for headers (e.g., email.header.Header).
This solution should resolve the encoding issue while maintaining the functionality of the MCP server’s other tools. Let me know if you need further assistance or want to test specific inputs!

---

