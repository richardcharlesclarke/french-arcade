import json

with open('vocab_game.json', 'r') as f:
    data = json.load(f)

# Filter out categories that look like "Image X" or are empty
clean_data = []
for cat in data:
    if "Image" in cat['name'] and len(cat['name']) < 10:
        continue
    if not cat['words']:
        continue
    clean_data.append(cat)

with open('vocab_game_clean.json', 'w') as f:
    json.dump(clean_data, f, indent=2)

print(f"Cleaned {len(data)} categories to {len(clean_data)}")
