import os
import json
from dotenv import load_dotenv
from google import genai
from week6.schema import FutureStockEventListSchema

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_future_stock_events():
    prompt = """
Generate exactly 10 future stock events for a toy store.

Return valid JSON only in this structure:
{
  "events": [
    {
      "title": "string",
      "event_type": "string",
      "expected_date": "YYYY-MM-DD",
      "product_name": "string",
      "quantity_change": 10,
      "note": "string"
    }
  ]
}

Rules:
- Include exactly 10 events
- All dates must be future dates
- Keep events realistic for toy inventory
- event_type can be:
  incoming_shipment,
  seasonal_spike,
  low_stock_warning,
  preorder_arrival,
  supplier_delay,
  warehouse_transfer
- title must not be empty
- product_name must not be empty
- quantity_change must be an integer
- output valid JSON only
- do not include markdown
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "temperature": 0.3,
            "response_mime_type": "application/json",
            "response_schema": FutureStockEventListSchema,
        }
    )
    print("\nRAW GEMINI RESPONSE:\n")
    print(response.text)
    validated_events = FutureStockEventListSchema.model_validate_json(
        response.text)
    print(f"\nValidated event count: {len(validated_events.events)}")
    return validated_events


def export_events_to_json(validated_events, filepath: str = "week6/future_stock_events.json"):
    events_as_dicts = []
    for event in validated_events.events:
        event_dict = event.model_dump()
        events_as_dicts.append(event_dict)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump({"events": events_as_dicts}, file, indent=2)
    print(f"\nValidated events exported to {filepath}")


if __name__ == "__main__":
    validated_events = generate_future_stock_events()
    export_events_to_json(validated_events)
