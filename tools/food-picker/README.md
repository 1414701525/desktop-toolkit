# Suzhou Food Picker

A local-first restaurant picker for Suzhou with multi-dimensional filtering and random selection. All data is embedded — no network required.

## Run

```bash
python suzhou_food_picker.py
```

## Features

- **Multi-filter** — Category, area, budget, time of day, scene, flavor, keyword
- **Random pick** — Animated random selection with a "spinning" effect
- **Alternatives** — Shows 5 backup options after each pick
- **History** — Remembers the last 8 picks
- **Copy to clipboard** — One-click share with friends

## Data Structure

Each restaurant entry:

```python
{
    "name": "Song He Lou",
    "eat": "Squirrel Mandarin Fish / Stir-fried Shrimp / Suzhou Cuisine",
    "category": "Suzhou Cuisine",
    "area": "Guanqian Street / Downtown",
    "budget": "¥¥¥",
    "time": ["Lunch", "Dinner", "Group"],
    "scene": ["Formal", "With friends", "Local flavor"],
    "flavor": ["Light", "Sweet", "Local"],
    "note": "Classic Suzhou cuisine, good for a proper meal.",
    "tags": ["Heritage", "Suzhou Cuisine", "Tourist-friendly"]
}
```

## Customization

Edit the `RESTAURANTS` list in `suzhou_food_picker.py` to add, remove, or modify entries.

## Notes

- Fully offline — no internet connection needed
- Check restaurant hours and locations on a map app before visiting
