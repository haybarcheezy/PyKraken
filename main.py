import requests
import logging
import time
from datetime import datetime
from typing import Any, List, Dict, Optional

# Constants
BASE_URL = "https://api.krakenflex.systems/interview-tests-mock-api/v1"
API_KEY = "<API_KEY>"

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_data(endpoint: str, method: str = "GET", data: Any = None, retries: int = 5, backoff_factor: float = 0.5) -> \
        Optional[Any]:
    """
    Fetch data from the given endpoint using the specified method with improved error handling.

    Args:
        endpoint (str): API endpoint to fetch data from.
        method (str): HTTP method. Default is "GET".
        data (Any): Data to send in the request. Default is None.
        retries (int): Number of retries for the request. Default is 3.
        backoff_factor (float): Factor for exponential backoff. Default is 0.5.

    Returns:
        Optional[Any]: Returns the data from the API or None if the request fails.
    """
    headers = {"x-api-key": API_KEY}
    url = f"{BASE_URL}{endpoint}"

    for i in range(retries):
        try:
            response = requests.request(method, url, headers=headers, json=data, timeout=10)

            if response.status_code == 429:
                wait_time = backoff_factor * (2 ** i)
                logging.warning(f"Rate limit reached. Waiting for {wait_time} seconds and retrying...")
                time.sleep(wait_time)
                continue

            if response.status_code == 400:
                logging.error(f"Bad Request. Server Response: {response.content.decode('utf-8')}")
                return None

            response.raise_for_status()
            return response.json()

        except requests.Timeout:
            logging.error("Request timed out.")
        except requests.HTTPError as http_err:
            if response.status_code == 500:
                logging.error("Internal Server Error. Please check with the API server maintainers.")
            else:
                logging.error(f"HTTP error occurred: {http_err}")
        except requests.RequestException as e:
            logging.error(f"Request error: {e}")
            if response.content:
                logging.error(f"API Error Message: {response.content.decode('utf-8')}")

    return None


logging.basicConfig(level=logging.INFO, format='%(message)s')


def get_all_outages() -> Optional[List[Dict]]:
    """
    Fetch all outages from the /outages endpoint.

    Returns:
        Optional[List[Dict]]: List of outages or None if the request fails.
    """
    return fetch_data("/outages")


def get_site_info(site_id: str) -> Optional[Dict]:
    """
    Fetch site information using the /site-info/{siteId} endpoint.

    Args:
        site_id (str): ID of the site.

    Returns:
        Optional[Dict]: Site information or None if the request fails.
    """
    return fetch_data(f"/site-info/{site_id}")


def filter_and_transform_outages(outages: List[Dict], site_info: Dict) -> List[Dict]:
    """
    Filters outages based on the given criteria and attaches device names from the site info.

    Args:
        outages (List[Dict]): List of outages.
        site_info (Dict): Site information.

    Returns:
        List[Dict]: Filtered and transformed outages.
    """
    cutoff_datetime = datetime.fromisoformat("2022-01-01T00:00:00.000Z")
    device_id_name_map = {device["id"]: device["name"] for device in site_info["devices"]}

    return [
        {**outage, "name": device_id_name_map[outage["id"]]}
        for outage in outages
        if datetime.fromisoformat(outage["begin"]) >= cutoff_datetime and outage["id"] in device_id_name_map
    ]


def post_site_outages(site_id: str, outages: List[Dict]) -> Optional[Dict]:
    """
    Post the processed outages to the /site-outages/{siteId} endpoint.

    Args:
        site_id (str): ID of the site.
        outages (List[Dict]): List of processed outages.

    Returns:
        Optional[Dict]: Server response or None if the request fails.
    """
    if not outages:
        logging.warning("No outages to post. Skipping the POST operation.")
        return None

    response = fetch_data(f"/site-outages/{site_id}", method="POST", data=outages)

    if response:
        logging.info("Outages posted successfully.")
    else:
        logging.error("Failed to post the outages.")

    return response


def main():
    """
    Main execution function with enhanced logging and printing for user feedback.
    """
    logging.info("Starting the process...")

    logging.info("Fetching all outages...")
    outages = get_all_outages()
    if not outages:
        return
    logging.info("Fetched all outages successfully.")
    print("\nOutages Data:")
    for outage in outages:
        print(outage)

    logging.info("Fetching site information for 'norwich-pear-tree'...")
    site_info = get_site_info("norwich-pear-tree")
    if not site_info:
        return
    logging.info("Fetched site information successfully.")
    print("\nSite Information:")
    print(site_info)

    logging.info("Filtering and transforming outages...")
    processed_outages = filter_and_transform_outages(outages, site_info)
    logging.info(f"Filtered and transformed {len(processed_outages)} outages.")
    print("\nProcessed Outages:")
    for outage in processed_outages:
        print(outage)

    logging.info("Posting processed outages...")
    response = post_site_outages("norwich-pear-tree", processed_outages)
    if not response:
        return
    print("\nPost Response:")
    print(response)

    logging.info(f"Successfully posted {len(processed_outages)} outages.")
    print("Process completed successfully!")


if __name__ == "__main__":
    main()
