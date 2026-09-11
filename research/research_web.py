# from langchain_community.document_loaders import WebBaseLoader

# def scrape(url):
#     loader = WebBaseLoader(["https://www.assorttech.com/"])
#     data = loader.load()
#     return data


# def create_website_research_target(company):
#     return {
#         "company": company,
#         "pages_to_review": [
#             "homepage",
#             "products_services",
#             "customer_journey",
#             "contact",
#             "rfq",
#             "booking",
#             "customer_login",
#             "portal",
#             "resources",
#             "case_studies",
#             "support",
#             "careers",
#             "company_information"
#         ]
#     }

# if __name__ == "__main__":
#     url = "https://www.assorttech.com/"

#     data = scrape(url)

#     print("Number of documents:", len(data))
#     print("First document:")
#     print(data[0].page_content[:1000])

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from langchain_community.document_loaders import WebBaseLoader


def scrape_website(url):
    loader = WebBaseLoader([url])
    data = loader.load()

    return data


def find_relevant_pages(url):
    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    pages = []

    base_domain = urlparse(url).netloc

    for link in soup.find_all("a", href=True):

        text = link.get_text(" ", strip=True)

        if not text:
            continue

        full_url = urljoin(url, link["href"])

        parsed_url = urlparse(full_url)

        # Only keep links from the same website
        if parsed_url.netloc != base_domain:
            continue

        # Remove #section from URL
        clean_url = full_url.split("#")[0]

        # Avoid duplicate URLs
        if any(page["url"] == clean_url for page in pages):
            continue

        pages.append({
            "text": text,
            "url": clean_url
        })

    return pages

def scrape_discovered_pages(pages):
    all_data = []

    for page in pages[:8]:
        url = page["url"]

        try:
            data = scrape_website(url)

            for document in data:
                document.metadata["page_name"] = page["text"]
                all_data.append(document)

            print(f"Scraped: {page['text']} -> {url}")

        except Exception as e:
            print(f"Failed: {url}")
            print(f"Error: {e}")

    return all_data


def create_website_research_target(company):
    return {
        "company": company,
        "pages_to_review": [
            "homepage",
            "products_services",
            "customer_journey",
            "contact",
            "rfq",
            "booking",
            "customer_login",
            "portal",
            "resources",
            "case_studies",
            "support",
            "careers",
            "company_information"
        ]
    }


if __name__ == "__main__":

    url = "https://assorttech.com"

    pages = find_relevant_pages(url)

    print("\nDiscovered links:\n")

    for page in pages:
        print(f"{page['text']} -> {page['url']}")