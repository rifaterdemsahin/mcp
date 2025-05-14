To send an email via Gmail using an MCP (Model Context Protocol) server, you can utilize the `gmail-mcp-server` developed by MaitreyaM. This server is designed to integrate with AI agents and facilitates sending emails through Gmail's SMTP server. Here's a step-by-step guide to set it up:

---

### 📦 Prerequisites

1. **Python 3.x**: Ensure you have Python installed on your system.
2. **Gmail Account**: You'll need a Gmail account with SMTP access enabled.
3. **App Password**: If your Gmail account has 2-Step Verification enabled, generate an App Password to use for SMTP authentication.

---

### 🔧 Installation Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/MaitreyaM/gmail-mcp-server.git
   cd gmail-mcp-server
   ```

2. **Set Up Environment Variables**:

   Create a `.env` file in the root directory with the following content:

   ```env
   SMTP_USERNAME=your.email@gmail.com
   SMTP_PASSWORD=your_app_password
   ```

   Replace `your.email@gmail.com` with your Gmail address and `your_app_password` with the App Password you generated.

3. **Install Dependencies**:

   It's recommended to use a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Run the Server**:

   Start the MCP server:

   ```bash
   python server.py
   ```

   The server will start on `127.0.0.1:5000` and can be accessed by your MCP clients or agents.

---

### ✉️ Sending an Email

You can send emails using the `send_email_tool` with the following parameters:

* `recipient`: Email address of the recipient.
* `subject`: Subject of the email.
* `body`: Body content of the email.
* `attachment_path` (optional): Path to a local file to attach.
* `attachment_url` (optional): URL of a file to download and attach.
* `attachment_name` (optional): Name to assign to the attachment.

**Example: Sending an Email with a Local Attachment**

```json
{
  "recipient": "friend@example.com",
  "subject": "Hello with attachment",
  "body": "Please see the attached document.",
  "attachment_path": "C:\\path\\to\\document.pdf"
}
```

**Example: Sending an Email with an Attachment from a URL**

```json
{
  "recipient": "friend@example.com",
  "subject": "Hello with attachment",
  "body": "Please see the attached image.",
  "attachment_url": "https://example.com/image.png",
  "attachment_name": "image.png"
}
```

**Example: Sending an Email with a Pre-Staged Attachment**

Place your file in the `available_attachments` directory and reference it by name:

```json
{
  "recipient": "friend@example.com",
  "subject": "Hello with attachment",
  "body": "Please see the attached file.",
  "attachment_name": "document.pdf"
}
```

---

### 🛠️ Integration with Claude Desktop

To integrate the MCP server with Claude Desktop:

1. **Configure Claude**:

   Open `claude_desktop_config.json` and add the following configuration:

   ```json
   {
     "mcpServers": {
       "gmail-mcp": {
         "command": "python",
         "args": ["PATH_TO_gmail_mcp.py"],
         "host": "127.0.0.1",
         "port": 5000,
         "timeout": 30000
       }
     }
   }
   ```

   Replace `PATH_TO_gmail_mcp.py` with the actual path to your `gmail_mcp.py` script.

2. **Install via Smithery (Optional)**:

   If you prefer, you can install the server automatically using Smithery:

   ```bash
   npx -y @smithery/cli install @MaitreyaM/gmail-mcp-server --client claude
   ```

---

For more detailed information and advanced configurations, refer to the [Gmail MCP Server GitHub repository](https://github.com/MaitreyaM/gmail-mcp-server).
