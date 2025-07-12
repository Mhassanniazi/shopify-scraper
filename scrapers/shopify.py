import requests
import pandas as pd

def make_request(URL):
    # param: page (for iterating through pages)
    page, data = 1, []
    while True:
        try:
            url = f"{URL}/products.json?limit=250&page={page}"
            print("> Performing request to", url)

            response = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
            parsed_data = response.json()

            if parsed_data.get("products"):
                data.extend(parsed_data["products"])
                page += 1
            else:
                break
        except:
            print(f"Error fetching data from {url} on page {page}")
            break

    return {"products": data, "total": len(data)}

def main(URL):
    URL = URL[:-1] if URL.endswith('/') else URL
    parsed_data = make_request(URL)

    return parsed_data