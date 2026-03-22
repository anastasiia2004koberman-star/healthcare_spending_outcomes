import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time
import json

def pull_data_requests(url):
    """Pull raw HTML data from a website using requests"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_html_data(html_content):
    """Parse HTML content using BeautifulSoup"""
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def extract_table_data(url, table_index=0):
    """Extract table data from a website"""
    try:
        tables = pd.read_html(url)
        return tables[table_index]
    except Exception as e:
        print(f"Error extracting table: {e}")
        return None

def pull_json_data(url):
    """Pull JSON data from an API endpoint"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON: {e}")
        return None

def pull_cms_api_data(dataset_id, limit=1000):
    """Pull data from CMS data.cms.gov API"""
    base_url = f"https://data.cms.gov/data-api/v1/dataset/{dataset_id}/data"
    params = {
        'size': limit,
        'offset': 0
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CMS API data: {e}")
        return None

if __name__ == "__main__":
    print("=" * 50)
    print("CMS Healthcare Data Pull")
    print("=" * 50)

    # Example 1: Pull CMS homepage HTML
    print("\n1. Testing basic HTML pull from CMS...")
    url = "https://www.cms.gov/"
    html = pull_data_requests(url)
    if html:
        soup = parse_html_data(html)
        print(f"✓ Successfully pulled {len(html)} characters from CMS homepage")

    # Example 2: Pull from CMS Data portal
    print("\n2. Testing CMS Data API...")
    dataset_id = "6bd6b1dd-208c-4f9c-88b8-b15fec6db548"
    data = pull_cms_api_data(dataset_id, limit=10)
    if data:
        df = pd.DataFrame(data)
        print(f"✓ Retrieved {len(df)} records from CMS")
        print(df.head())
    else:
        print("✗ Failed to retrieve data from CMS API")

    # Example 3: Extract tables from a page
    print("\n3. Testing table extraction...")
    table_url = "https://www.cms.gov/research-statistics-data-systems/statistics-trends-reports"
    df = extract_table_data(table_url)
    if df is not None:
        print(f"✓ Extracted table with {len(df)} rows")
        print(df.head())
    else:
        print("✗ Could not extract table from page")
