import re
import json

file_path = '/Users/admin/Cass_french/french_vocabulary.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for rows
row_pattern = re.compile(r'<tr>(.*?)</tr>', re.DOTALL)
# Pattern for section header
header_pattern = re.compile(r'<td[^>]*class="section-header"[^>]*>(.*?)</td>', re.DOTALL)
# Pattern for normal cells
cell_pattern = re.compile(r'<td.*?>(.*?)</td>', re.DOTALL)

rows = row_pattern.findall(content)

categories = []
current_category_name = "General"
current_words = []

def save_category():
    global current_words
    if current_words:
        categories.append({
            "name": current_category_name,
            "words": current_words
        })
    current_words = []

for row in rows:
    # Check if header
    header_match = header_pattern.search(row)
    if header_match:
        # Save previous category
        save_category()
        # Start new
        current_category_name = re.sub(r'<[^>]+>', '', header_match.group(1)).strip()
        continue
    
    # Check if normal row
    cells = cell_pattern.findall(row)
    if len(cells) >= 2:
        french_raw = cells[0].strip()
        english_raw = cells[1].strip()
        needed_raw = cells[2].strip() if len(cells) > 2 else "Yes"

        french_clean = re.sub(r'<[^>]+>', '', french_raw).strip()
        english_clean = re.sub(r'<[^>]+>', '', english_raw).strip()
        needed_clean = re.sub(r'<[^>]+>', '', needed_raw).strip()

        if french_clean and english_clean:
            current_words.append({
                "french": french_clean,
                "english": english_clean,
                "needed": needed_clean
            })

# Save last batch
save_category()

print(json.dumps(categories, indent=2))
