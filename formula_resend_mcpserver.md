Yes, there are publicly available MCP (Model Context Protocol) servers that you can integrate with Cursor to send emails. These servers utilize third-party email APIs and can be set up with minimal effort.

---

### 📧 Option 1: Resend MCP Server

The [Resend MCP Server](https://github.com/resend/mcp-send-email) allows you to send emails directly from Cursor using [Resend's API](https://resend.com/). This setup requires minimal configuration and is suitable for sending plain text and HTML emails.([GitHub][1])

#### 🔧 Setup Steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/resend/mcp-send-email.git
   cd mcp-send-email
   ```



2. **Install Dependencies:**

   ```bash
   npm install
   npm run build
   ```



3. **Configure in Cursor:**

   In your `.cursor/mcp.json` file, add the following configuration:

   ```json
   {
     "mcpServers": {
       "resend": {
         "type": "command",
         "command": "node",
         "args": [
           "/absolute/path/to/mcp-send-email/build/index.js",
           "--key=YOUR_RESEND_API_KEY"
         ]
       }
     }
   }
   ```



Replace `/absolute/path/to/mcp-send-email/build/index.js` with the actual path to the `index.js` file in the cloned repository. Replace `YOUR_RESEND_API_KEY` with your actual Resend API key.

4. **Obtain Resend API Key:**

   Sign up at [Resend](https://resend.com/) and obtain your API key from the dashboard.

5. **Verify Domain (Optional):**

   To send emails from your own domain, you may need to verify your domain within the Resend dashboard.

6. **Test Email Sending:**

   Within Cursor, you can now use the Resend MCP server to send emails. For example, create a file `email.md` with your email content, select it, and instruct Cursor to "send this as an email."

---

### 📧 Option 2: Mailtrap MCP Server

The [Mailtrap MCP Server](https://mailtrap.io/blog/vs-code-send-email/) is another option that allows sending emails using [Mailtrap's Email API](https://mailtrap.io/). This is particularly useful for testing and development purposes.([Mailtrap][2])

#### 🔧 Setup Steps:

1. **Install the MCP Server:**

   ```bash
   npx -y mcp-mailtrap
   ```



2. **Configure in Cursor:**

   In your `.cursor/mcp.json` file, add the following configuration:

   ```json
   {
     "mcpServers": {
       "mailtrap": {
         "command": "npx",
         "args": ["-y", "mcp-mailtrap"],
         "env": {
           "MAILTRAP_API_TOKEN": "your_mailtrap_api_token",
           "DEFAULT_FROM_EMAIL": "your_sender@example.com"
         }
       }
     }
   }
   ```



Replace `your_mailtrap_api_token` with your actual Mailtrap API token and `your_sender@example.com` with your sender email address.

3. **Obtain Mailtrap API Token:**

   Sign up at [Mailtrap](https://mailtrap.io/) and obtain your API token from the dashboard.

4. **Test Email Sending:**

   Within Cursor, you can now use the Mailtrap MCP server to send emails. Compose your email content and instruct Cursor to send it using the configured MCP server.

---

### ✅ Summary

Both Resend and Mailtrap offer publicly accessible MCP servers that can be integrated with Cursor for email sending capabilities.

* **Resend MCP Server**: Suitable for production use, supports plain text and HTML emails, and allows domain verification.([GitHub][1])

* **Mailtrap MCP Server**: Ideal for testing and development, provides a safe environment to test email sending without spamming real inboxes.

Choose the one that best fits your needs.

If you need further assistance with the setup or have specific requirements, feel free to ask!

[1]: https://github.com/resend/mcp-send-email?utm_source=chatgpt.com "resend/mcp-send-email - GitHub"
[2]: https://mailtrap.io/blog/vs-code-send-email/?utm_source=chatgpt.com "How to Send Emails in VS Code with Mailtrap MCP Server"
