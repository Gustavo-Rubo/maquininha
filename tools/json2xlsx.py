import pandas as pd
from os import path
import json

base_path = path.join('.', '.')
with open(path.join(base_path, 'data', 'database.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    item['ocr'] = '; '.join(item['ocr'])

df = pd.DataFrame(data)

df = df[['name', 'macro', 'submacro', 'origin', 'daterecorded', 'originalfilepath', 'panoid', 'lat', 'long', 'ocr', 'description']]
df.to_excel(path.join(base_path, 'data', 'database.xlsx'), index=False)