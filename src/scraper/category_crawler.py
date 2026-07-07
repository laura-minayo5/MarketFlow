# Crawls through the discovered categories, downloads
# each category page, and saves the HTML locally.

# Input: a dictionary of category names → URLs from category_crawler.py.
# Work: download the category pages using URLs from the dictionary, save it locally.
# Output: yield (name, html) for the next stage.  

# Dict category names → URLs
#       ↓
# Download Category Page
#       ↓
# Save HTML Locally
#       ↓
# Pass (name, html) to the next stage

import time

from requests.exceptions import RequestException

from .config import RAW_CATEGORIES, REQUEST_DELAY
from .downloader import download_page


def crawl_categories(categories: dict[str, str]) -> None:
    """Download and save every category page."""

    RAW_CATEGORIES.mkdir(parents=True, exist_ok=True)

    # Iterate over every discovered category.
    for name, url in categories.items():

        print(f"Downloading: {name}")

        # download the category page and handle any potential request errors gracefully.
        try:
            html = download_page(url)

        except RequestException as error:
            print(f"Failed to download {name}: {error}")
            continue

        filename = (
            name.lower()
            .replace("&", "and")
            .replace(" ", "_")
        )

        output_file = RAW_CATEGORIES / f"{filename}.html"
        output_file.write_text(html, encoding="utf-8")

        print(f"Saved {output_file.name}")

        # Pass the downloaded HTML to the next stage.
        yield name, html

        # Be polite to the server by introducing a delay between requests to avoid overwhelming it.
        time.sleep(REQUEST_DELAY)