import json
import pandas as pd
from os import path
from shapely import wkt

m_per_coord = 1e5

base_path = path.join('.', '.')
file_macros = path.join(base_path, 'data', 'map_macro.csv')
df_macros = pd.read_csv(file_macros)
file_submacros = path.join(base_path, 'data', 'map_submacro.csv')
df_submacros = pd.read_csv(file_submacros)

data = []
with open(path.join(base_path, 'data', 'database.json'), 'r') as f:
    data = json.load(f)

macros = []
for index, row in df_macros.dropna(how='all')[['WKT', 'name']].iterrows():
    macros.append({'poly': wkt.loads(row['WKT']), 'name': row['name']})

submacros = []
for index, row in df_submacros.dropna(how='all')[['WKT', 'name']].iterrows():
    submacros.append({'poly': wkt.loads(row['WKT']), 'name': row['name']})

for record in data:
    p = wkt.loads(f'POINT({record["long"]} {record["lat"]})')
    for macro in macros:
        if macro['poly'].contains(p):
            record['macro'] = macro['name']
            break

    for submacro in submacros:
        if submacro['poly'].contains(p):
            record['submacro'] = submacro['name']
            break

with open(path.join(base_path, 'data', 'database.json'), 'w') as f:
    json.dump(data, f)

# print(row['name'], poly.contains(p), poly.boundary.distance(p)*m_per_coord)