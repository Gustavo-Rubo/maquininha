import json
from os import path

base_path = path.join('.', '.')

data = []
with open(path.join(base_path, 'data', 'database_photos copy.json'), 'r') as f:
    data = json.load(f)

filepaths = []
data_new = []
for d in data:
    if d['originalfilepath'] not in filepaths:
        data_new.append(d)
        filepaths.append(d['originalfilepath'])
        
with open(path.join(base_path, 'data', 'database_photos.json'), 'w') as f:
    json.dump(data_new, f)
