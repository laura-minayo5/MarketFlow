from .config import HOME_PAGE, RAW_HOME, PROCESSED_PRODUCTS
from .downloader import download_page
from .homepage_parser import extract_category_urls
from .category_crawler import crawl_categories
from .product_parser import extract_product_urls
from .product_crawler import crawl_products
from .product_details_parser import parse_product_details
from itertools import islice
from pathlib import Path
import json

def save_products(products: list[dict], output_path: Path) -> None:
    """Save parsed products to a JSON file."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(
            products,
            f,
            indent=4,
            ensure_ascii=False,
        )

def main():
    """Run the complete MarketFlow scraping pipeline."""

    # Create the raw homepage directory if it doesn't exist.
    RAW_HOME.mkdir(parents=True, exist_ok=True)

    # 1. Download the homepage HTML.
    homepage_html = download_page(HOME_PAGE)

    # Save the homepage HTML.
    output_file = RAW_HOME / "homepage.html"
    output_file.write_text(homepage_html, encoding="utf-8")

    print(f"Saved homepage to {output_file}")

    # 2. homepage_parser reads homepage.html and extracts:
    # Extract Category names + Category URLs using BeautifulSoup.
    categories = extract_category_urls(homepage_html)

    print(f"\nFound {len(categories)} categories:\n")

    # Print the discovered categories and their URLs in a formatted manner.
    for name, url in categories.items():
        print(f"{name:<25} -> {url}")

    print("\nStarting scraping pipeline...\n")

    # 3. category_crawler uses the Category URLs to download each category page html.
    # it yields (category_name, category_html) for the next stage.
    for category_name, category_html in islice(crawl_categories(categories), 1):  # Limit to the first category for testing

        print(f"\nParsing category: {category_name}")

        # 4. product_parser Reads each category page HTML and extracts:
        # (Product names + Product URLs) using BeautifulSoup.
        products = extract_product_urls(category_html)
        # products = dict(list(products.items())[:5]) # for testing so that we only download 5 products

        print(f"Found {len(products)} products")

        # 5. product_crawler uses the Product URLs to download each product page html.
        # it yields (product_name, product_html) for the next stage.
        # Download first 5 items in generator for testing

        parsed_products = [] # List to hold parsed product details
        
        for product_name, product_html in islice(crawl_products(products), 5):


            print(f"\nDownloaded product: {product_name}")

            # 6. product_details_parser reads each product page HTML and extracts:
            # (Product name, price, old price, discount, rating, reviews) using BeautifulSoup.
            product = parse_product_details(product_html)

            # Append the parsed product details to the list of parsed products.
            parsed_products.append(product)

            # 7. Output the product details to the console.
            print("\nProduct Details")
            print("-" * 60)

            # Print the product details in a formatted manner.
            for field, value in product.items():
                print(f"{field:<15}: {value}")

            print("-" * 60)

    save_products(parsed_products, PROCESSED_PRODUCTS)

    print(f"\nSaved {len(parsed_products)} products to {PROCESSED_PRODUCTS}")

if __name__ == "__main__":
    main()

