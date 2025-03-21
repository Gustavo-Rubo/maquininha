import json
import time
import random
import easyocr
import numpy as np
from os import path
from PIL import Image
from glob import glob

easyocr_reader = easyocr.Reader(['pt', 'en'])
reprocess_existing = True


def ocr(file_og):
    file = path.split(file_og)[1]
    panoid = file.split('=')[0]
    source = 'streetview-google' if len(panoid) <= 23 else 'streetview-user'
    long = float(file[:-5].split('=')[1])
    lat = float(file[:-5].split('=')[2])

    img = Image.open(file_og)
    box1 = (0, 0, img.width//2, img.height)
    box2 = (img.width//2, 0, img.width, img.height)
    canvas_size = 2100

    easyocr_res = easyocr_reader.readtext(np.array(img.crop(box1)),
        batch_size=1, detail=0, text_threshold=.6, canvas_size=canvas_size)
    easyocr_res.extend(easyocr_reader.readtext(np.array(img.crop(box1).rotate(-90, expand=1)),
        batch_size=1, detail=0, text_threshold=.6, canvas_size=canvas_size))
    easyocr_res.extend(easyocr_reader.readtext(np.array(img.crop(box2)),
        batch_size=1, detail=0, text_threshold=.6, canvas_size=canvas_size))
    easyocr_res.extend(easyocr_reader.readtext(np.array(img.crop(box2).rotate(-90, expand=1)),
        batch_size=1, detail=0, text_threshold=.6, canvas_size=canvas_size))


    return {
        'id': '',
        'macroid': '',
        'submacroid': '',
        'daterecorded': '',
        'originalfilepath': file,
        'panoid': panoid,
        'lat': lat,
        'long': long,
        'origin': source,
        'name': '',
        'ocr': easyocr_res,
        'description': ' '.join(easyocr_res),
    }


base_path = path.join('.', '.')
paths = glob(path.join(base_path, 'images_raw', 'street_view', 'stitched', 'z5', '*'))
paths.extend(glob(path.join(base_path, 'images_raw', 'street_view', 'stitched', 'z4', '*')))

old_data = []
if not reprocess_existing:
    with open(path.join(base_path, 'data', 'database_panos.json'), 'r') as f:
        old_data = json.load(f)
    new_paths = []
    old_panoids = [d['panoid'] for d in old_data]
    for p in paths:
        panoid = path.split(p)[1].split('=')[0]
        if panoid not in old_panoids:
            new_paths.append(p)

    paths = new_paths

random.shuffle(paths)

start = time.time()
data = []
batch = 800
for i, p in enumerate(paths[:batch]):
    print(f'ocr {i+1}/{len(paths[:batch])}')
    data.append(ocr(p))
stop = time.time()

new_data = [*old_data, *data]

print(f'performed ocr in {len(data)} files')
print(f'run time: {stop - start:.0f}s')
print(f'time per file: {(stop - start)/len(paths):.2f}s')

with open(path.join(base_path, 'data', 'database_panos.json'), 'w') as f:
    json.dump(new_data, f)
