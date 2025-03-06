import os
from concurrent.futures import ThreadPoolExecutor
import requests
from dagster import op

SAVE_BASE_DIR = "csv_data"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})

@op
def download_csv_files(context, csv_files: list):
    current_dir = os.path.dirname(os.path.abspath(__file__)) 
    parent_dir = os.path.dirname(current_dir) 
    save_dir = os.path.join(parent_dir, SAVE_BASE_DIR) 
    os.makedirs(save_dir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {}
        for file_url, file_name in csv_files:
            save_path = os.path.join(save_dir, file_name)
            futures[executor.submit(session.get, file_url, timeout=200)] = save_path

        for future in futures:
            save_path = futures[future]
            try:
                response = future.result()
                response.raise_for_status()  
                with open(save_path, "wb") as f:
                    f.write(response.content)
                context.log.info(f"✅ Downloaded: {save_path}")
            except requests.RequestException as e:
                context.log.error(f"❌ Failed to download {save_path}: {e}")

    context.log.info("All downloads completed.")
    return save_dir
