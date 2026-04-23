import json
import re
import sys
from dotenv import load_dotenv
from ocr import ocr_with_claude
import requests

load_dotenv()

# Variables
libris_match = 0
chalmers_holdings = 0
lquery = ''
libris_search_api_endpoint = 'https://libris.kb.se/find'
title = ''
authors = ''

# Script for testing the Claude Vision OCR functions with scanned images from Chalmers IPAC. The extracted data is printed as JSON.

if len(sys.argv) < 2:
    print("Usage: python3 main.py <image_path>")
    sys.exit(1)

image = sys.argv[1]
result = ocr_with_claude(image)
print("Response for " + image + ": ", json.dumps(result, indent=2, ensure_ascii=False))

# Lookup in Libris

if result.get("title"):
    lquery = result["title"]

if result.get("authors"):
    lquery += " " + " ".join(result["authors"])

if result.get("editors"):
    lquery += " " + " ".join(result["editors"])

if result.get("year_of_publication"):
    lquery += " " + result["year_of_publication"]

#if result.get("pages"):
#    lquery += " " + re.sub(r"\D", "", result["pages"])

lquery = lquery.replace(". ", "+").replace(", ", "+")

print('Libris query: ' + lquery)

headers = {'Accept': 'application/json',
           'User-Agent': 'cth-ipac-ocr/1.0'}

libris_lookup = libris_search_api_endpoint + '?q=' + lquery + '&_limit=1'

data = requests.get(url=libris_lookup, headers=headers).text
# convert string to Json
libris_data = json.loads(data)

# print(libris_data)

if libris_data and libris_data['totalItems'] > 0:
    libris_match = 1
    print("Libris match found for query: " + lquery)

    # Extract additional fields from the response
    libris_year = libris_data['items'][0]['publication'][0]['librissearch:year_4_digits_short'] if 'librissearch:year_4_digits_short' in libris_data['items'][0]['publication'][0] else ''
    if 'hasTitle' in libris_data['items'][0]:
        libris_title = next((t["mainTitle"] for t in libris_data['items'][0]["hasTitle"] if t["@type"] == "Title"), None)
    else:
        libris_title = ''
    libris_id = libris_data['items'][0]['@id'] if '@id' in libris_data['items'][0] else ''
    libris_type = libris_data['items'][0]['instanceOf']['@type'] if '@type' in libris_data['items'][0]['instanceOf'] else ''

    print("Libris match details:")
    print("  ID:", libris_id)
    print("  Type:", libris_type)
    print("  Title:", libris_title)
    print("  Year:", libris_year)
    

# TODO
# Batch processing of multiple images
# Looking up records in other databases (WorldCat, LC...)
# Create MarcXML record (or something else) from the extracted data?
# Logging and error handling
# Something else? 
