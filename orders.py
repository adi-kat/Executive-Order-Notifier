import requests
from datetime import date

url = \
"https://www.federalregister.gov/api/v1/documents.json?per_page=20&conditions[president][]=donald-trump"

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
                    urls.append(doc['html_url'])
        return urls
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return []
    except ValueError:
        print("Error decoding JSON response.")
        return []
    except KeyError:
        print("Unexpected response format from the API.")
        return []

if __name__ == "__main__":
    search_date = date.today()
    executive_order_urls = get_executive_order_links(search_date)
    if executive_order_urls:
        print(f"URLs of executive orders published on {search_date}:")
        for url in executive_order_urls:
            print(url)
    else:
        print(f"No executive orders found for {search_date}.")
