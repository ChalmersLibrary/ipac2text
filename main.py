import json
import sys
from dotenv import load_dotenv
from ocr import ocr_with_claude

load_dotenv()

# Script for testing the Claude Vision OCR functions with scanned images from Chalmers IPAC. The extracted data is printed as JSON.

if len(sys.argv) < 2:
    print("Usage: python3 main.py <image_path>")
    sys.exit(1)

image = sys.argv[1]
result = ocr_with_claude(image)
print("Response for " + image + ": ", json.dumps(result, indent=2, ensure_ascii=False))


# TODO
# Batch processing of multiple images
# Lookup existing record in Libris using the extracted title and author?
# Create MarcXML record (or something else) from the extracted data?
# Logging and error handling
# Something else? 
