# Executive Order Discord Notifier

🏛️ A Python script that checks the Federal Register API for new U.S. Presidential Executive Orders on a specified date and posts them to a Discord channel using a webhook.
## 🔧 Features

    ✅ Fetches executive orders published on a specific date using the Federal Register API

    ✅ Scrapes the order’s HTML page for the title

    ✅ Sends a formatted embed to Discord with the order's title and link

    ✅ Gracefully handles errors and bot detection

## 📦 Requirements

    Python 3.7+

    requests

    beautifulsoup4

    python-dotenv

    discord-webhook

Install dependencies:
```
pip install -r requirements.txt
```
## 📁 Project Structure
```
.
├── discord.py                     # Main script that posts to Discord
├── orders.py                   # Contains the API fetching logic
├── .env                        # Stores your Discord webhook URL
├── README.md                   # You're here!
```
## 🔐 Environment Variables

Create a .env file with the following content:
```
WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url_here
```
    ⚠️ Never expose your webhook URL in public repositories.

## 🚀 How to Use

Run the script by specifying the desired date:
```
python discord.py
```
You can modify the date in the script or update it to always use today's date (date.today()).
## 🧠 How It Works

    The script calls the Federal Register API to get executive orders for a specific date.

    For each document, it requests the HTML page.

    If successful, it scrapes the title from the <h1> tag.

    It then sends the title and link as a rich embed to a Discord channel using a webhook.

## 🛡️ Bot Detection Handling

If the page returns a "Request Access" message, the script skips that link and logs a message. This indicates bot protection is active.

## 📅 Sample Output

https://www.federalregister.gov/documents/2025-04-22/...

Title: Executive Order on Ensuring American Leadership

Successfully sent 'Executive Order on Ensuring American Leadership' to Discord.

## 🧪 Example API Call

get_executive_order_links("2025-04-22")

Returns a list of HTML URLs to executive orders published on April 22, 2025.

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to change.

Let me know if you'd like me to generate a requirements.txt file or split the script into separate files (main.py, orders.py).
