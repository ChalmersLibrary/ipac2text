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
                    "text": """This is a scanned type written library catalog card with handwritten notes.
Please OCR the text and extract these fields if present:
- authors (surnames are often underlined and sometimes following the first name, "/" is often used to mark calling name, / should be excluded in response)
- editors (usually preceded by "ed" or "ed." or "red." or "redaktör" or "editor") and in the form "firstname lastname" (if possible to determine, otherwise return as is)
- title
- place_of_publication
- publisher
- year_of_publication
- pages (often preceded or followed by "s." or "sidor" or or "s" or "p" or "pp")
- format - Example of formats are ["4:o", "8:o", "12:o", "Fol"]
- source_publication (usually preceded by "in:" or "i:" or "ur:")
- series - often preceded by "serie" or "=", can be enclosed in slashes (“/”) or parentheses
- isbn
- classification_code (usually in the top right corner, normally hand written, usually in the format letters and numbers, i.e. "QC 21", sometimes preceeded by a handwritten abbreviation [e.g. "br] that should not be included in response, sometimes preceded by "+")
- call_number (usually in the top right corner, first alphabetic part of classification_code, e.g. "QB "
- main_heading - usually in top left corner, often in the form of a single word or short sentence, usually underlined with a dashed line, e.g. "Physics" (underlined with dashed line)
- subject_headings (as a list if there are multiple)
- shelf (in the form of a square root symbol followed by a string, e.g. "√123-456", often preceded by a handwritten abbreviation, e.g. "br" or "hylla"), square root symbol should be excluded in response
- items (repeatable, usually located in the bottom left corner, normally notated, e.g., 59.123), sometimes beginning with aphabetic characters, e.g. "Sv.", usually typed)
- reference (usually preceded by "se: " or "se " or "hänvis" or "ref:")
- notes
- bottom_note (bottom center, usually an acronym, e.g. ["vb" or "kh"])
- systematic_card, 1 or 0, return 1 if the card only consists of a single call number and short description (otherwise return 0)
- reference_card, 1 or 0, return 1 if reference has a value, otherwise return 0
- serial_publication_card, 1 or 0, usually indicated by year_of_publication being a range (e.g. "1950-") or multiple years (e.g. "1990, 1992, 1995"), often has information about volume ("vol." or "Vol.")
- multipart_work_card, 1 or 0, return 1 if the card is describing a multipart work, usually identified with "Bd" or Band" or "bd." or "Bd" followed by numbers, eg "Bd 1-2" , otherwise return 0
- monograph_card, 1 or 0, return 1 if all the previous are 0 and the card has a title and author/editor, otherwise return 0 
Also include these quality/review fields:
- needs_review (true/false — set true if you are uncertain about any part of the transcription and/or overall confidence is classified as low)
- review_reasons (a list of specific reasons if needs_review is true, e.g. ["ambiguous call numbers","author name unclear", "possible smudge on year", "handwriting difficult to read"])
- confidence (overall confidence as "high", "medium", or "low")

Return as JSON only, no explanation."""
                }
            ]
        }]
    )

    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    return json.loads(text)
