import re

def expand(ingredients):
    expanded = []
    for ing in ingredients:
        name = ing.get("name", "").strip()
        match = re.search(r'\(([^)]+)\)', name)
        if match:
            inside = match.group(1)
            if ',' in inside:
                parent_name = re.sub(r'\s*\([^)]+\)', '', name).strip()
                if parent_name:
                    expanded.append({"name": parent_name})
                sub_names = re.split(r',\s*(?![^\[]*\])', inside)
                for sub_name in sub_names:
                    sub_name = sub_name.strip()
                    if sub_name:
                        expanded.append({"name": sub_name})
                continue
        expanded.append(ing)
    return expanded

test = [
    {"name": "Enriched unbleached flour (wheat flour, malted barley flour, ascorbic acid [dough conditioner, modifier], niacin, reduced iron)"},
    {"name": "Maida (refined flour)"},
    {"name": "Water"}
]

import pprint
pprint.pprint(expand(test))
