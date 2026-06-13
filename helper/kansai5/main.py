import sys
import json
from pathlib import Path
from typing import Any
import requests
from bs4 import BeautifulSoup
import lxml
import re

# Add project root to sys.path (find the directory containing db_structs.py)
_root = Path(__file__).resolve().parent
while _root.parent != _root:
    if (_root / "db_structs.py").exists():
        if str(_root) not in sys.path:
            sys.path.append(str(_root))
        break
    _root = _root.parent

from db_structs import (
    Medium,
    Circle,
    Event,
    EventGroup,
    Source,
    ReliabilityTypes,
    OriginTypes,
    Location,
)

PATH_EVENT = Path(__file__).parent
PATH_CIRCLES_JSON = PATH_EVENT / "circles.json"
NAME = PATH_EVENT.name


def retrieve_soup_fetch_if_needed(url: str) -> BeautifulSoup:
    """Retrieve BeautifulSoup object for the given URL, fetching the content if necessary."""
    html_path = PATH_EVENT / "raw.html"
    if not html_path.exists():
        print(f"Raw HTML file not found, fetching from {url} ...")
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(
                f"Failed to retrieve data from {url}, status code: {response.status_code}"
            )
        # Use apparent_encoding to handle Japanese encodings (Shift_JIS, etc.)
        response.encoding = response.apparent_encoding
        html_path.write_text(response.text, encoding="utf-8")
    
    # Read as UTF-8 since we saved it as such
    content = html_path.read_text(encoding="utf-8")
    return BeautifulSoup(content, "html.parser")


def sanitize_string(s: str) -> str:
    s = s.strip()
    s = re.sub(r"[\s\n\t]+", " ", s)
    return s


def main():
    """Create circles.json"""
    print(f"Retrieving circles information for {NAME} ...")
    raw_url = "https://web.archive.org/web/20160221081920fw_/http://vo-para.birdzberth.com/cercle_list.html"
    
    # Parse the HTML content to extract circle information
    soup = retrieve_soup_fetch_if_needed(raw_url)
    circles = []

    # table: with border=1
    table = soup.select_one('table[frame="VOID"]')
    if not table:
        raise Exception("Failed to find the circles table in the HTML content.")

    table_rows = table.select("tr")
    if not table_rows:
        raise Exception("No rows found in the circles table.")

    for row in table_rows:
        col_tags = row.select("td")
        if not col_tags:
            print(f"WARNING: invalid row (no columns)")
            continue

        c0 = col_tags[0]
        c0text = c0.get_text(strip=True)        
        if len(col_tags) < 4:
            continue
        if "配置" in c0text or "サークル名" in c0text:
            continue

        position_booth = sanitize_string(col_tags[0].get_text(strip=True))
        circle_name = sanitize_string(col_tags[1].get_text(strip=True))
        pen_name = sanitize_string(col_tags[2].get_text(strip=True))

        circle_url = None
        a_tag = col_tags[3].select_one("a")
        if a_tag and a_tag.has_attr("href"):
            circle_url = sanitize_string(a_tag["href"].replace("https://web.archive.org/web/20160221081920/", ""))

        position_sp=sanitize_string(col_tags[4].get_text(strip=True))
        # chair = sanitize_string(col_tags[5].get_text(strip=True))
        distributed = sanitize_string(col_tags[6].get_text(strip=True))
        
        position = f"{position_booth}, SP数{position_sp}".strip()

        comment_parts: list[str] = []
        if distributed:
            comment_parts.append(f"Distributed media formats: {distributed}")

        circle = Circle(
            aliases=[circle_name],
            pen_names=[pen_name] if pen_name else None,
            links=[circle_url] if circle_url else None,
            position=position,
            comments=", ".join(comment_parts) if comment_parts else None,
        )

        circles.append(circle)

    # Save the extracted circle information to a JSON file
    with open(PATH_CIRCLES_JSON, "w", encoding="utf-8") as f:
        json.dump([c.get_json() for c in circles], f, ensure_ascii=False, indent=2)
    print(f"Saved {len(circles)} circles to {PATH_CIRCLES_JSON}")


if __name__ == "__main__":
    main()
