import requests
from datetime import date
from bs4 import BeautifulSoup
from orders import get_executive_order_links
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv
import os

load_dotenv()
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
if not WEBHOOK_URL:
    print("Error: WEBHOOK_URL not found in the environment file.")
else:
    for link in get_executive_order_links(date.today()):
        url = link
        print(url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        response = requests.get(url, headers=headers)

        if "Request Access" in response.text:
            print("Still blocked — site is likely using bot protection.")
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            h1_title = soup.find("h1", {"id": "h-1"})
            if h1_title:
                title = h1_title.text.strip()
                print(f"Title: {title}")

                webhook = DiscordWebhook(url=WEBHOOK_URL)
                embed = DiscordEmbed(
                    title="New Executive Order",
                    description=title,
                    color=0x00ff00,
                    url=url 
                )
                embed.set_author(name="U.S. Government", url="https://www.whitehouse.gov/", icon_url="https://www.whitehouse.gov/wp-content/themes/whitehouse/assets/img/whitehouse-47-logo.webp")
                webhook.add_embed(embed)
                response = webhook.execute()
                if response.status_code == 200:
                    print(f"Successfully sent '{title}' to Discord.")
                else:
                    print(f"Error sending '{title}' to Discord. Status code: {response.status_code}, Response: {response.text}")

            else:
                print("No <h1> tag found")