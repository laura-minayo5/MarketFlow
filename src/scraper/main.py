from .config import HOME_PAGE, RAW_HOME
from .downloader import download_page
from .category_parser import extract_category_urls
from .category_crawler import crawl_categories
from .product_parser import extract_product_urls
from .product_crawler import crawl_products
from .product_details_parser import parse_product_details


def main():
    """Run the complete MarketFlow scraping pipeline."""

    # Create the raw homepage directory if it doesn't exist.
    RAW_HOME.mkdir(parents=True, exist_ok=True)

    # Download the homepage.
    homepage_html = download_page(HOME_PAGE)

    # Save the homepage HTML.
    output_file = RAW_HOME / "homepage.html"
    output_file.write_text(homepage_html, encoding="utf-8")

    print(f"Saved homepage to {output_file}")

    # Extract category names and URLs from the homepage using BeautifulSoup. (homepage_parser.py).
    categories = extract_category_urls(homepage_html)

    print(f"\nFound {len(categories)} categories:\n")

    for name, url in categories.items():
        print(f"{name:<25} -> {url}")

    print("\nStarting scraping pipeline...\n")

    # Download each category page.
    for category_name, category_url in crawl_categories(categories):

        print(f"\nParsing category: {category_name}")

         # Extract product names and relative URLs from the category page using BeautifulSoup. (product_parser.py)
        products = extract_product_urls(category_url)

        print(f"Found {len(products)} products")

        # Download each product page.
        for product_name, product_html in crawl_products(products):

            print(f"Downloaded product: {product_name}")

            # Parse product details from the product page using BeautifulSoup. (product_details_parser.py)
            product = parse_product_details(product_html)
            print(product)

if __name__ == "__main__":
    main()

