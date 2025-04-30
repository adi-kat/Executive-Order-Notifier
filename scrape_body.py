import requests
from bs4 import BeautifulSoup
from orders import get_executive_order_links  
from summary import summarize_text 
from datetime import date

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

def fetch_and_scrape_executive_orders(target_date_str):
    executive_order_urls = get_executive_order_links(target_date_str)
    
    if executive_order_urls:
        print(f"Scraping and summarizing executive orders published on {target_date_str}:")
        for url in executive_order_urls:
            print(f"Scraping: {url}")
            body_text = scrape_body_text(url)
            if body_text:
                summary = summarize_text(body_text)
                print(f"Summary for {url}:\n{summary}\n")
            else:
                print(f"No body text found for {url}.")
    else:
        print(f"No executive orders found for {target_date_str}.")

if __name__ == "__main__":
    search_date = date.today().strftime('%Y-%m-%d')
    fetch_and_scrape_executive_orders(search_date)
