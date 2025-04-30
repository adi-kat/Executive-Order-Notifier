import requests
from bs4 import BeautifulSoup
import re

def scrape_title(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return "Title not found"

    if "Request Access" in response.text:
        print(f"Blocked by bot protection at {url}.")
        return "Title not found"

    soup = BeautifulSoup(response.content, "html.parser")

    title_text = None

    if "whitehouse.gov" in url:
        h1_title = soup.find("h1", class_="wp-block-whitehouse-topper__headline")
        if h1_title:
            title_text = h1_title.get_text(separator=" ", strip=True)
    elif "federalregister.gov" in url:
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.get_text(separator=" ", strip=True)
            if " :: " in title_text:
                title_text = title_text.split(" :: ")[1]

    if not title_text:
        title_tag = soup.find("title")
        if title_tag:
            title_text = title_tag.get_text(separator=" ", strip=True)
        else:
            print(f"No title found at {url}")
            return "Title not found"

    if title_text.isupper():
        title_text = title_text.title()

    title_text = re.sub(r'\s+', ' ', title_text)

    return title_text

if __name__ == "__main__":
    whitehouse_url = "https://www.whitehouse.gov/presidential-actions/2025/04/28/white-house-initiative-to-promote-excellence-and-innovation-at-historically-black-colleges-and/"
    federal_register_url = "https://www.federalregister.gov/documents/2025/04/28/2025-07380/white-house-initiative-to-promote-excellence-and-innovation-at-historically-black-colleges-and"

    whitehouse_title = scrape_title(whitehouse_url)
    federal_register_title = scrape_title(federal_register_url)

    print(f"White House Title: {whitehouse_title}")
    print(f"Federal Register Title: {federal_register_title}")
