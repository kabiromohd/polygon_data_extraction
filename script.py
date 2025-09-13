import requests
import os
import json
import openai
from dotenv import load_dotenv
import time
import csv

load_dotenv()
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

#print(POLYGON_API_KEY)
print("Fetching tickers from Polygon.io API...")

limit = 1000
url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&sort=ticker&order=asc&limit={limit}&apiKey={POLYGON_API_KEY}"
response = requests.get(url)
data = response.json()  

tickers = []
for ticker in data["results"]:
    tickers.append(ticker)
time.sleep(10)

while "next_url" in data:
    print("Fetching next page...", data["next_url"])
    next_url = data["next_url"] + f"&apiKey={POLYGON_API_KEY}"
    response = requests.get(next_url)
    data = response.json()
    #print(data)
    print()
    for ticker in data["results"]:
        tickers.append(ticker)
    time.sleep(10)  # To respect rate limits


#print(f"Total tickers fetched: {len(tickers)}")

example_ticker = {'ticker': 'ZYN',
                'name': 'Defiance Daily Target 2x Long PM ETF',
   'market': 'stocks',
    'locale': 'us',
    'primary_exchange': 'XNAS',
    'type': 'ETF',
    'active': True,
    'currency_name': 'usd',
    'composite_figi': 'BBG01X1031X2',
    'share_class_figi': 'BBG01X103821',
    'last_updated_utc': '2025-09-13T06:11:08.184043717Z'}

fieldnames = list(example_ticker.keys())
output_file = "tickers.csv"
with open(output_file, mode = "w", newline = "", encoding = "utf-8") as f:
    # Create a CSV writer object
   
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the data rows
    for ticker in tickers:
        row = {key: ticker.get(key, "") for key in fieldnames}
        writer.writerow(row)

print(f"Write {len(tickers)} row saved to {output_file}")