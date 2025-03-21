import json
from os import path

base_path = path.join('.', '.')

data = []
with open(path.join(base_path, 'data', 'database_panos copy.json'), 'r') as f:
    data = json.load(f)

data_new = [
    {
        "daterecorded": "",
        "originalfilepath": d['file'],
        "panoid": d['panoid'],
        "lat": d['lat'],
        "long": d['long'],
        "origin": f"streetview-{d['source']}",
        "name": "",
        "ocr": d['ocr'],
        "description": ' '.join(d['ocr']),
        "macro": "",
        "submacro": ""
    } for d in data
]
with open(path.join(base_path, 'data', 'database_panos.json'), 'w') as f:
    json.dump(data_new, f)
