# 🐙💪 KrakenFlex Back End Test (but in Python 🐍)

This test is designed to help you showcase your back end engineering skills. The primary objective is to interact with a given API to retrieve, filter, transform, and post outages data for a specific site.

This repository is an alternative attempt to the KrakenFlex Back End Test using python instead of javascript. (The original attempt can be found [here](https://github.com/haybarcheezy/flex))

This was not a requirement of the test, but I wanted to demonstrate my ability to work with multiple languages. This is also a good opportunity to compare the two languages and their respective ecosystems although this project still has it's TODO's

## Tasks Completed

1. All outages are retrieved from the `GET /outages` endpoint.
2. Information is retrieved from the `GET /site-info/{siteId}` endpoint for the site with the ID `norwich-pear-tree`.
3. Outages that began before `2022-01-01T00:00:00.000Z` or don't have an ID present in the list of devices in the site information are filtered out.
4. For the remaining outages, the display name of the device from the site information is attached to each appropriate outage.
5. This list of outages is sent to `POST /site-outages/{siteId}` for the site with the ID `norwich-pear-tree`.

Additionally, the solution is resilient to occasional 500 error responses from the API (I upped the retries to 5).

## Setup and Execution

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Set up a virtual environment of your choosing
4. Install the necessary Python packages using the command: `pip install -r requirements.txt`
5. Run the program using the command: `python main.py`

## Testing (TODO)

Unit tests have been outlined in `test_main.py`. To execute the tests:

1. Navigate to the project directory.
2. Run the tests using the command: `python -m unittest test_main.py`
3. etc...

🐙🐙🐙💪💪💪
