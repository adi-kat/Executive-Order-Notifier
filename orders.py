import requests
from title import scrape_title 
from slugify import slugify 

url = "https://www.federalregister.gov/api/v1/documents.json?per_page=20&conditions[president][]=donald-trump"

def get_executive_order_links(target_date_str):
    params = {
        "per_page": 100,
        "order": "newest",
        "conditions[publication_date]": target_date_str,
        "conditions[presidential_document_type]": "executive_order"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        urls = []
        if 'results' in data:
            for doc in data['results']:
                if doc['publication_date'] == target_date_str:
                    fr_url = doc['html_url']  
                    slug = fr_url.rstrip('/').split('/')[-1]

                    pub_date_parts = doc['publication_date'].split('-')
                    year = pub_date_parts[0]
                    month = pub_date_parts[1]

                    white_house_url = f"https://www.whitehouse.gov/presidential-actions/{year}/{month}/{slug}/"

                    try:
                        check_response = requests.head(white_house_url, timeout=5)
                        if check_response.status_code == 200:
                            urls.append(white_house_url)
                            continue
                        else:
                            print(f"White House URL not found (Status {check_response.status_code}). Trying title-based URL.")
                    except requests.RequestException:
                        print("Error checking White House URL. Trying title-based URL.")

                    title = scrape_title(fr_url)
                    if title == "Title not found":
                        urls.append(fr_url)
                        continue

                    title_slug = slugify(title)
                    title_based_white_house_url = f"https://www.whitehouse.gov/presidential-actions/{year}/{month}/{title_slug}/"

                    try:
                        check_response = requests.head(title_based_white_house_url, timeout=5)
                        if check_response.status_code == 200:
                            urls.append(title_based_white_house_url)
                        else:
                            print(f"Title-based White House URL not found (Status {check_response.status_code}). Falling back to Federal Register URL.")
                            urls.append(fr_url)
                    except requests.RequestException:
                        print("Error checking title-based White House URL. Falling back to Federal Register URL.")
                        urls.append(fr_url)
        return urls
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return []
    except requests.exceptions.JSONDecodeError:
        print("Error decoding JSON response.")
        return []
    except KeyError:
        print("Unexpected response format from the API.")
        return []
