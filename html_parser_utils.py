"""HTML parser utilities wrapping the standard library html.parser module.

Provides helpers for parsing HTML with validation and convenient utilities.
"""

from html.parser import HTMLParser
from typing import Dict, List, Optional, Union

__all__ = [
    "HTMLParser",
    "HTMLStripper",
    "strip_html_tags",
    "extract_tags",
    "is_available",
]


def is_available() -> bool:
    """Return True if html.parser is available."""
    return True


class HTMLStripper(HTMLParser):
    """HTML parser that strips tags and returns plain text."""

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def handle_entityref(self, name):
        self.fed.append(f"&{name};")

    def handle_charref(self, name):
        self.fed.append(f"&#{name};")

    def get_data(self) -> str:
        return "".join(self.fed)


def strip_html_tags(html: str) -> str:
    """Strip HTML tags from string and return plain text."""
    if not isinstance(html, str):
        raise TypeError(f"html must be a string, got {type(html).__name__}")
    if not html:
        return html
    stripper = HTMLStripper()
    stripper.feed(html)
    stripper.close()
    return stripper.get_data()


def extract_tags(
    html: str, tag: Optional[str] = None
) -> List[Dict[str, Union[str, Dict[str, str]]]]:
    """Extract tags from HTML with their attributes and data."""
    if not isinstance(html, str):
        raise TypeError(f"html must be a string, got {type(html).__name__}")
    if tag is not None and not isinstance(tag, str):
        raise TypeError(f"tag must be a string or None, got {type(tag).__name__}")

    results = []

    class TagExtractor(HTMLParser):
        def handle_starttag(self, tag_name, attrs):
            if tag is None or tag_name == tag:
                results.append({
                    "tag": tag_name,
                    "attrs": dict(attrs),
                    "type": "start",
                    "data": ""
                })

        def handle_startendtag(self, tag_name, attrs):
            if tag is None or tag_name == tag:
                results.append({
                    "tag": tag_name,
                    "attrs": dict(attrs),
                    "type": "self_closing",
                    "data": ""
                })

        def handle_endtag(self, tag_name):
            if tag is None or tag_name == tag:
                # Just record end, don't add as separate entry if we have start
                pass

        def handle_data(self, data):
            # Add data to last start tag
            for i in range(len(results) - 1, -1, -1):
                if results[i].get("type") in ("start", "self_closing"):
                    if "data" not in results[i]:
                        results[i]["data"] = ""
                    results[i]["data"] += data
                    break

    parser = TagExtractor()
    parser.feed(html)
    parser.close()
    return results
