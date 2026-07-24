
# Crawls through the discovered products, downloads
# each product page, and saves the HTML locally. 

# Input: a dictionary of product names → URLs from product_crawler.py.
# Work: download the product pages using URLs from the dictionary, save it locally.
# Output: yield (name, html) for the next stage.  

# Dict product names → URLs from product_parser.py
#       ↓ 
# Download Product Page using the URLs
#       ↓
# Save products HTML Locally
#       ↓
# Pass (name, html) to the next stage

import time
from requests.exceptions import RequestException
from config.paths import RAW_PRODUCTS, REQUEST_DELAY
from .downloader import download_page

def crawl_products(products: dict[str, str]) -> None:
    """Download and save every product page."""

    RAW_PRODUCTS.mkdir(parents=True, exist_ok=True)

    for name, url in products.items():

        print(f"Downloading: {name}")

        # download the product page and handle any potential request errors gracefully.
        try:
            html = download_page(url)

        except RequestException as error:
            print(f"Failed to download {name}: {error}")
            continue

        filename = (
            name.lower()
                .replace("&", "and")
                .replace("/", "_")
                .replace(" ", "_")
        )

        output_file = RAW_PRODUCTS / f"{filename}.html"
        output_file.write_text(html, encoding="utf-8")

        print(f"Saved {output_file.name}")

        # Pass the downloaded HTML to the next stage.
        yield name, html

        # Be polite to the server by introducing a delay between requests to avoid overwhelming it.
        time.sleep(REQUEST_DELAY)