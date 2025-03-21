import json
from os import path

base_path = path.join('.', '.')

data = []
files = ['database_panos.json', 'database_photos.json']

for file in files:
    with open(path.join(base_path, 'data', file), 'r') as f:
        data.extend(json.load(f))

with open(path.join(base_path, 'data', 'database.json'), 'w') as f:
    json.dump(data, f)
