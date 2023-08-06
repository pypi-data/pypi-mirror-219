import re
import json


class Parser:
    def json_parse(text: str) -> dict:
        try:
            # Greedy search for 1st json candidate.
            match = re.search(
                "\{.*\}", text.strip(), re.MULTILINE | re.IGNORECASE | re.DOTALL
            )
            json_str = ""
            if match:
                json_str = match.group()
            json_object = json.loads(json_str)
            return json_object
        except json.JSONDecodeError as e:
            raise ValueError(f"Could not parse {text} json: {e}")
