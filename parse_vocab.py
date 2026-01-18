import re
import json
from pathlib import Path

file_path = '/Users/admin/Cass_french/french_vocabulary.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Naive regex parsing because I can't rely on bs4 being installed, 
# though standard library HTMLParser is an option. Regex is often robust enough for simple tables.

items = []
# Find all rows
row_pattern = re.compile(r'<tr>(.*?)</tr>', re.DOTALL)
cell_pattern = re.compile(r'<td.*?>(.*?)</td>', re.DOTALL)
rows = row_pattern.findall(content)

for row in rows:
    if 'section-header' in row:
        continue
    
    cells = cell_pattern.findall(row)
    if len(cells) >= 2:
        french_raw = cells[0].strip()
        english_raw = cells[1].strip()
        needed_raw = cells[2].strip() if len(cells) > 2 else "Yes"

        # Cleaning HTML tags usually not needed inside cells here, 
        # but pure text extraction is safer.
        # Remove simple tags if any
        french_clean = re.sub(r'<[^>]+>', '', french_raw).strip()
        english_clean = re.sub(r'<[^>]+>', '', english_raw).strip()
        needed_clean = re.sub(r'<[^>]+>', '', needed_raw).strip()

        # simple structure
        if french_clean and english_clean:
            items.append({
                "french": french_clean,
                "english": english_clean,
                "needed": needed_clean
            })

print(json.dumps(items, indent=2))
