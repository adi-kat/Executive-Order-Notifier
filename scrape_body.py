import requests
from bs4 import BeautifulSoup

def scrape_body_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;"
                  "q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return ""

    if "Request Access" in response.text:
        print(f"Blocked by bot protection at {url}.")
        return ""

    soup = BeautifulSoup(response.content, "html.parser")

    p_tags = soup.find_all("p")

    continuous_text = ""
    for p in p_tags:
        text = p.get_text(strip=True)
        if text:
            continuous_text += text + " " 

    return continuous_text.strip()
