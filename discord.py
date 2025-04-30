from datetime import date
from orders import get_executive_order_links
from title import scrape_title 
from scrape_body import scrape_body_text
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not WEBHOOK_URL:
    print("Error: WEBHOOK_URL not found in the environment file.")
elif not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in the environment file.")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')

    today = date.today()
    for link in get_executive_order_links(f"{today}"): 
        url = link
        print(url)
        
        title = scrape_title(url)
        print(f"Title: {title}")
        body = scrape_body_text(url) 

        prompt = f"""Summarize the following text into exactly four bolded main bullet points, each labeled **Policy**, **Context**, **General Background Information**, and **Importance**. 

        - **Policy**: related details in sub-bullets.
        - **Context**: information that precedes the overall notion, helping explain why it might be happening, and takes into account any potential biases or differing perspectives if need be, in sub-bullets.
        - **General Background Information**: details outside the article itself that are deeply relevant to understanding the topic, in sub-bullets.
        - **Importance**: related details in sub-bullets.

        Do not add any extra text or formatting. Format exactly as specified.
        Keep the total word count under 100 words.
        If needed, include regular (non-bolded) sub-bullets under each main point for related details.
        Do not add any introductory, concluding, or extra text.\n{body}"""


        response = model.generate_content(prompt)
        summary = response.text

        paragraph = f"""
        {summary}
        """

        webhook = DiscordWebhook(url=WEBHOOK_URL)
        embed = DiscordEmbed(
            title="New Executive Order",
            description=f"**{title}**\n{paragraph}",
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
