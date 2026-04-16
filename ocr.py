import anthropic
import base64
import json
import os

def ocr_with_claude(image_path):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data,
                    }
                },
                {
                    "type": "text",
                    "text": """This is a scanned type written library catalog card with hand written notes.
Please OCR the text and extract these fields if present:
- authors (surnames are often underlined and sometimes following the first name, "/" is often used to mark calling name, / should be excluded in response)
- title
- place_of_publication
- publisher
- year_of_publication
- pages (often preceded or followed by "s." or "sidor" or or "s" or "p" or "pp")
- source_publication (usually preceded by "in:" or "i:" or "ur:")
- series (often preceded by "serie" or "=")
- isbn
- call_number (usually in the top right corner, normally hand written, usually a short combination of letters and numbers, often with a space in between, e.g., "XZ 1234", sometimes preceded by "+")
- subject_headings (as a list if there are multiple)
- classification_code (usually located in the bottom left corner, normally in Universal Decimal Classification (UDC) format (notation, e.g., 000.123.456), sometimes beginning with aphabetic characters, e.g. "Sv.", usually typed)
- reference (usually preceded by "se" or "ref:")
- notes
- bottom_note (bottom center, usually an acronym, i.e. "vb" or "kh")
- systematic_card, 1 or 0, return 1 if the card only consists of a single call number and short description (otherwise return 0)

Return as JSON only, no explanation."""
                }
            ]
        }]
    )

    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    return json.loads(text)
