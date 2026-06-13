import sys
import json
from pathlib import Path
from typing import Any
import requests
import re
import pdfplumber

# Add project root to sys.path (find the directory containing db_structs.py)
_root = Path(__file__).resolve().parent
while _root.parent != _root:
    if (_root / "db_structs.py").exists():
        if str(_root) not in sys.path:
            sys.path.append(str(_root))
        break
    _root = _root.parent

from db_structs import (
    Circle,
)

PATH_EVENT = Path(__file__).parent
PATH_CIRCLES_JSON = PATH_EVENT / "circles.json"
NAME = PATH_EVENT.name


def retrieve_pdf_fetch_if_needed(url: str) -> Path:
    """Retrieve PDF file path for the given URL, fetching the content if necessary."""
    pdf_path = PATH_EVENT / "raw.pdf"
    if not pdf_path.exists():
        print(f"Raw PDF file not found, fetching from {url} ...")
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(
                f"Failed to retrieve data from {url}, status code: {response.status_code}"
            )
        pdf_path.write_bytes(response.content)
    return pdf_path


def sanitize_string(s: str) -> str:
    if s is None:
        return ""
    s = s.strip()
    s = re.sub(r"[\s\n\t]+", " ", s)
    return s


def main():
    """Create circles.json"""
    print(f"Retrieving circles information for {NAME} ...")
    raw_url = "http://ttc.ninja-web.net/vo-para/150308_circlelist.pdf"

    pdf_path = retrieve_pdf_fetch_if_needed(raw_url)
    circles = []
    seen_positions = set()

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i == 0:
                continue
            
            # 1. Identify the top of the first table on the page
            table_top = page.bbox[3] # Default to bottom of page
            finds = page.find_tables()
            if finds:
                table_top = min(f.bbox[1] for f in finds)

            # 2. Extract "lost" circles above the first table (common in this PDF)
            words = page.extract_words()
            # Sort by top, then x0
            words.sort(key=lambda x: (x["top"], x["x0"]))
            lines = {}
            for w in words:
                if w["top"] < table_top - 2: # Slightly above the table
                    top = round(w["top"], 1)
                    if top not in lines:
                        lines[top] = []
                    lines[top].append(w)
            
            for top in sorted(lines.keys()):
                line_words = lines[top]
                # Try to parse as a circle row using known column x-thresholds
                # Col 0 (Circle): x < 150
                # Col 1 (Pen Name): 150 <= x < 300
                # Col 2 (Position): 300 <= x < 350
                # Col 3 (URL): x >= 350
                row = ["", "", "", ""]
                for w in line_words:
                    x = (w["x0"] + w["x1"]) / 2
                    if x < 150: row[0] += w["text"] + " "
                    elif x < 300: row[1] += w["text"] + " "
                    elif x < 350: row[2] += w["text"] + " "
                    else: row[3] += w["text"] + " "
                
                row = [sanitize_string(r) for r in row]
                circle_name = row[0]
                pen_name = row[1]
                position = row[2]
                circle_link = row[3]
                
                if position and re.search(r"[A-Z]-[0-9]+", position):
                    if position not in seen_positions:
                        # Skip headers that might be misclassified
                        if "サークル名" in circle_name or "ペンネーム" in pen_name:
                            continue
                        
                        circle = Circle(
                            aliases=[circle_name],
                            pen_names=[pen_name] if pen_name else None,
                            position=position,
                            links=[circle_link] if circle_link else None,
                        )
                        circles.append(circle)
                        seen_positions.add(position)
                        print(f"Added top-of-page circle: {circle_name} ({position})")

            # 3. Process tables as usual
            tables = page.extract_tables()
            for table in tables:
                if not table or len(table) < 2:
                    continue

                for row in table:
                    if len(row) != 4:
                        continue

                    circle_name = sanitize_string(row[0])
                    pen_name = sanitize_string(row[1])
                    position = sanitize_string(row[2])
                    circle_link = sanitize_string(row[3])
                    
                    if "サークル名" in circle_name or "ペンネーム・P名" in pen_name:
                        continue
                    if "予備スペース" in circle_name:
                        continue
                    
                    # Basic validation for position
                    if not position or not re.search(r"[A-Z]-[0-9]+", position):
                        continue
                    
                    if position in seen_positions:
                        continue

                    circle = Circle(
                        aliases=[circle_name],
                        pen_names=[pen_name] if pen_name else None,
                        position=f"{position}",
                        links=[circle_link] if circle_link else None,
                    )
                    circles.append(circle)
                    seen_positions.add(position)

    # Save the extracted circle information to a JSON file
    with open(PATH_CIRCLES_JSON, "w", encoding="utf-8") as f:
        json.dump([c.get_json() for c in circles], f, ensure_ascii=False, indent=2)
    print(f"Saved {len(circles)} circles to {PATH_CIRCLES_JSON}")


if __name__ == "__main__":
    main()
