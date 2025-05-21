An MCP (Model Context Protocol) email server enables AI applications to send and receive emails by providing standardized access to email functionalities like SMTP and IMAP. This setup allows AI agents to compose, send, and manage emails, including handling attachments and searching for files, through a unified interface.([Model Context Protocol][1], [Glama – MCP Hosting Platform][2])

### What Is an MCP Email Server?

An MCP email server acts as a bridge between AI models and email services. It allows AI applications to perform email operations such as sending messages, managing attachments, and searching directories for files to include in emails. This integration is particularly useful in environments where AI agents need to interact with email systems seamlessly.

### Key Features

* **Email Composition and Sending**: AI agents can compose and send emails to multiple recipients.
* **Attachment Handling**: Supports adding attachments to emails.
* **File Searching**: Enables searching for files in specified directories based on patterns.
* **Secure Transmission**: Utilizes SMTP for secure email sending.([Glama – MCP Hosting Platform][2])

### Installation and Configuration

To set up an MCP email server, you can use the `mcp-email-server` package available on PyPI. Installation can be done via pip:([GitHub][3])

```bash
pip install mcp-email-server
```



After installation, configure the server using the built-in UI:([GitHub][3])

```bash
mcp-email-server ui
```



This UI allows you to set up your email server configurations, including SMTP settings and directories for file searches.

### Integration with AI Clients

Once configured, the MCP email server can be integrated with AI clients like Claude Desktop. This integration enables AI agents to perform email operations as part of their tasks, enhancing their capabilities in handling communication workflows.([MCP Servers][4], [Medium][5])

### Security Considerations

The MCP email server operates locally, relying on the client's machine resources. This design ensures that sensitive data remains within the user's environment, enhancing security. However, it's essential to ensure that the SMTP configurations are secure and that the directories accessed for file searches are appropriately permissioned.

For more detailed information and advanced configurations, you can refer to the official documentation: [MCP Email Server Documentation](https://ai-zerolab.github.io/mcp-email-server/).

By setting up an MCP email server, you empower AI applications to handle email communications effectively, integrating seamlessly into various workflows and enhancing automation capabilities.

[1]: https://modelcontextprotocol.io/introduction?utm_source=chatgpt.com "Model Context Protocol: Introduction"
[2]: https://glama.ai/mcp/servers/%40Shy2593666979/mcp-server-email?utm_source=chatgpt.com "MCP Email Server | Glama"
[3]: https://github.com/ai-zerolab/mcp-email-server?utm_source=chatgpt.com "ai-zerolab/mcp-email-server: IMAP and SMTP via MCP Server"
[4]: https://mcpmarket.com/server/email?utm_source=chatgpt.com "Email: IMAP/SMTP Server via MCP for Developers"
[5]: https://medium.com/data-and-beyond/mcp-servers-a-comprehensive-guide-another-way-to-explain-67c2fa58f650?utm_source=chatgpt.com "MCP Servers: A Comprehensive Guide — Another way to explain"


---

Certainly! To integrate Gmail access into Cursor using an MCP (Model Context Protocol) server, you'll need to configure your `.cursor/mcp.json` file appropriately. Here's a step-by-step guide to set this up:

---

### 📄 Step 1: Configure `.cursor/mcp.json`

Create or update your `.cursor/mcp.json` file with the following content:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/gmail-mcp",
        "run",
        "gmail",
        "--creds-file-path",
        "/absolute/path/to/credentials.json",
        "--token-path",
        "/absolute/path/to/tokens.json"
      ]
    }
  }
}
```

**Replace the placeholders with your actual paths:**

* `/absolute/path/to/gmail-mcp`: The directory where your Gmail MCP server code resides.
* `/absolute/path/to/credentials.json`: The path to your Gmail API credentials file.
* `/absolute/path/to/tokens.json`: The path where authentication tokens will be stored.([Playbooks][1])

---

### 🔐 Step 2: Set Up Gmail API Credentials

1. **Create a Google Cloud Project:**

   * Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
   * Create a new project or select an existing one.

2. **Enable the Gmail API:**

   * In the API Library, search for "Gmail API" and enable it for your project.([Playbooks][2])

3. **Configure OAuth Consent Screen:**

   * Set the user type to "External".
   * Add your email as a test user.
   * Add the scope: `https://www.googleapis.com/auth/gmail.modify`.([Playbooks][2])

4. **Create OAuth 2.0 Credentials:**

   * Navigate to "APIs & Services" > "Credentials".
   * Click "Create Credentials" > "OAuth client ID".
   * Choose "Desktop App" as the application type.
   * Download the JSON file containing your OAuth keys.
   * Save this file securely, e.g., `/Users/yourname/.gmail/credentials.json`.([MCP Server Cloud][3], [Playbooks][4], [Playbooks][1])

---

### 🚀 Step 3: Install and Run the Gmail MCP Server

1. **Clone the Gmail MCP Server Repository:**

   ```bash
   git clone https://github.com/yourusername/gmail-mcp.git
   cd gmail-mcp
   ```



2. **Install Dependencies:**

   ```bash
   uv pip install -e .
   ```



3. **Run the Server:**

   ```bash
   uv run gmail --creds-file-path "/Users/yourname/.gmail/credentials.json" --token-path "/Users/yourname/.gmail/tokens.json"
   ```



On the first run, a browser window will open prompting you to authenticate with your Google account. After authentication, tokens will be saved to the specified `tokens.json` file for future use.

---

### 🧪 Step 4: Test the Integration in Cursor

1. **Restart Cursor:**
   Ensure that Cursor recognizes the new MCP server configuration.

2. **Verify MCP Server Availability:**
   Navigate to `Settings > MCP` in Cursor and confirm that the Gmail MCP server is listed and active.

3. **Test Email Functionality:**
   Use Cursor's interface to send a test email, ensuring that the integration works as expected.

---

**Note:** Ensure that all paths specified in the configuration are absolute paths and that the necessary permissions are set for the files and directories involved.

If you encounter any issues or need further assistance with this setup, feel free to ask!

[1]: https://playbooks.com/mcp/jmonsellier-gmail?utm_source=chatgpt.com "Gmail MCP server for AI agents"
[2]: https://playbooks.com/mcp/theposch-gmail?utm_source=chatgpt.com "Gmail MCP server for AI agents"
[3]: https://mcpserver.cloud/server/gmail-autoauth-mcp-server?utm_source=chatgpt.com "Gmail AutoAuth MCP Server - MCP Server Integration | MCPHub | MCP Hub"
[4]: https://playbooks.com/mcp/sanchisingh-gmail?utm_source=chatgpt.com "Gmail MCP server for AI agents"


---

To set up a public Gmail SMTP server for sending emails via Cursor, you can configure your `.cursor/mcp.json` file to utilize Gmail's SMTP service. Here's how you can do it:

---

### 📄 Step 1: Configure `.cursor/mcp.json`

Update your `.cursor/mcp.json` file with the following configuration:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/gmail-mcp",
        "run",
        "gmail",
        "--smtp-server",
        "smtp.gmail.com",
        "--smtp-port",
        "587",
        "--username",
        "your_email@gmail.com",
        "--password",
        "your_app_password"
      ]
    }
  }
}
```

**Replace the placeholders with your actual information:**

* `/absolute/path/to/gmail-mcp`: The directory where your Gmail MCP server code resides.
* `your_email@gmail.com`: Your Gmail address.
* `your_app_password`: An App Password generated from your Google Account (see Step 2).([Google Groups][1], [controlbyweb.com][2])

---

### 🔐 Step 2: Generate an App Password

If you have Two-Factor Authentication (2FA) enabled on your Google account, you'll need to generate an App Password to allow external applications to access your Gmail SMTP server. Here's how:([Mailmeteor][3])

1. Go to your [Google Account Security Settings](https://myaccount.google.com/security).
2. Under "Signing in to Google," select **App passwords**.
3. You may need to sign in again.
4. Under "Select app," choose **Mail**, and under "Select device," choose **Other** (enter a custom name like "Cursor").
5. Click **Generate**.
6. Google will display a 16-character App Password. Use this password in your `.cursor/mcp.json` configuration.([Mailmeteor][3])

*Note: If you do not have 2FA enabled, it's highly recommended to enable it for security reasons.*

---

### 🚀 Step 3: Install and Run the Gmail MCP Server

1. **Clone the Gmail MCP Server Repository:**

   ```bash
   git clone https://github.com/yourusername/gmail-mcp.git
   cd gmail-mcp
   ```



2. **Install Dependencies:**

   ```bash
   uv pip install -e .
   ```



3. **Run the Server:**

   ```bash
   uv run gmail --smtp-server smtp.gmail.com --smtp-port 587 --username your_email@gmail.com --password your_app_password
   ```



Ensure that the `--username` and `--password` match the credentials specified in your `.cursor/mcp.json` file.

---

### 🧪 Step 4: Test the Integration in Cursor

1. **Restart Cursor:**

   Ensure that Cursor recognizes the new MCP server configuration.

2. **Verify MCP Server Availability:**

   Navigate to `Settings > MCP` in Cursor and confirm that the Gmail MCP server is listed and active.

3. **Test Email Functionality:**

   Use Cursor's interface to send a test email, ensuring that the integration works as expected.

---

**Note:** Gmail's SMTP server has sending limits and security measures. Ensure that your usage complies with Gmail's policies to avoid disruptions. ([Mailmeteor][3])

If you encounter any issues or need further assistance with this setup, feel free to ask!

[1]: https://groups.google.com/g/intersystems-public-cache/c/S5yYxP5gJzM?utm_source=chatgpt.com "Using Google Mail as SMTP Server"
[2]: https://controlbyweb.com/support/email/gmail-as-smtp-server/?srsltid=AfmBOore9R3Hx4GJ2K5nWPbQBJJ6gqWaDAW088KMR0KNALJwhUIc1YTb&utm_source=chatgpt.com "Setting up Gmail as your SMTP Server for Email Notifications"
[3]: https://mailmeteor.com/blog/gmail-smtp-settings?utm_source=chatgpt.com "How To Set Up Your Gmail SMTP Settings (2025 Guide) - Mailmeteor"


---

