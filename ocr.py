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
                    "text": """This is a scanned type written library catalog card with hand written notes etc.
Please OCR the text and extract these fields if present:
- author (surnames are often underlined and following the first name, "/" is often used to mark calling name, / should be excluded in response)
- title
- place_of_publication
- publisher
- year_of_publication
- pages
- source_publication (usually preceded by "in:" or "i:" or "ur:")
- series (often preceded by "serie" or "=")
- isbn
- call_number (usually top right corner)
- classification_number (usually bottom left corner)
- subject_headings (as a list)
- reference (usually preceded by "se" or "ref:")
- notes
- bottom_note (bottom center, usually an acronym, i.e. "vb" or "kh")

Return as JSON only, no explanation."""
                }
            ]
        }]
    )

    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    return json.loads(text)
