import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dagster import asset, Config

BASE_URL = "https://apps.elections.virginia.gov/SBE_CSV/CF/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})


@asset(required_resource_keys={"global_resource"})
def fetch_csv_links(context):
    year, month = context.resources.global_resource.year, context.resources.global_resource.month
    context.log.info(f"Searching for CSV files for {year}-{month}...")

    response = session.get(BASE_URL, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    csv_files = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.endswith("/") and "/CF/" in href and f"{year}_{month}" in href :
            folder_url = urljoin(BASE_URL, href)
            folder_response = session.get(folder_url, timeout=10)
            folder_response.raise_for_status()

            folder_soup = BeautifulSoup(folder_response.text, "html.parser")
            for file_link in folder_soup.find_all("a"):
                file_href = file_link.get("href")
                if file_href and file_href.endswith(".csv"):
                    file_url = urljoin(folder_url, file_href)
                    file_name = file_href.split("/")[-1]
                    context.log.info(f"File {file_name}: {file_url}")
                    csv_files.append((file_url, file_name))

    context.log.info(f"Found {len(csv_files)} CSV files.")
    return csv_files