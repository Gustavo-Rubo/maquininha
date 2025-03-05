import shutil
import requests
import numpy as np
from os import path, makedirs
from multiprocessing import Pool

REDOWNLOAD_EXISTING = False
RAW_BASE_DIR = path.join('..', '..', 'assets', 'raw')

# panoids = ['eTPYmbok7Ho94LG2bW9XgA', 'tQbB6SQ_anc7hOUEJNxHfg', 'Bpw-92VrITn2LIim3gzlZw', 'wS2g9Ay4DqTuOPOQ5fPErg']
panoids = np.load('panoids.npy')
user_panoids = np.load('user_panoids.npy')


def download_and_save_tile(args):
    url = args[0]
    path = args[1]

    try:
        img = requests.get(url, stream=True)

        if img.status_code == 200:
            with open(path, 'wb') as f:
                shutil.copyfileobj(img.raw, f)
        else:
            print(img.status_code, path)
    except Exception as e:
        print('Request exception', e)


for i, panoid in enumerate(panoids):
    print(f'tile z5 {i+1}/{len(panoids)}')

    BASE_STREETWIEW_URL = 'https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile'

    z = 1
    base_dir = path.join(RAW_BASE_DIR, f'z{z}', '='.join(panoid))
    if REDOWNLOAD_EXISTING or not path.isdir(base_dir):
        makedirs(base_dir, exist_ok=True)
        for y in [0]:
            with Pool(2) as p:
                args = [
                    [BASE_STREETWIEW_URL + f'&panoid={panoid[0]}&x={x}&y={y}&zoom={z}&nbt=1&fover=2',
                     path.join(base_dir, f'z{z}-y{y:02}-x{x:02}.jpeg')] for x in range(2)]
                p.map(download_and_save_tile, args)

    z = 5
    base_dir = path.join(RAW_BASE_DIR, f'z{z}', '='.join(panoid))
    if REDOWNLOAD_EXISTING or not path.isdir(base_dir):
        makedirs(base_dir, exist_ok=True)
        args = []
        for y in range(7, 10):
            args.extend([
                [BASE_STREETWIEW_URL + f'&panoid={panoid[0]}&x={x}&y={y}&zoom={z}&nbt=1&fover=2',
                 path.join(base_dir, f'z{z}-y{y:02}-x{x:02}.jpeg')] for x in range(32)])

        with Pool() as p:
            p.map(download_and_save_tile, args)


for i, user_panoid in enumerate(user_panoids):
    print(f'tile z4 {i+1}/{len(user_panoids)}')

    BASE_URL = 'https://lh3.ggpht.com/p/'

    z = 1
    base_dir = path.join(RAW_BASE_DIR, f'z{z}', '='.join(user_panoid))
    if REDOWNLOAD_EXISTING or not path.isdir(base_dir):
        makedirs(base_dir, exist_ok=True)
        for y in [0]:
            with Pool(2) as p:
                args = [
                    [BASE_URL + f'{user_panoid[0]}=x{x}-y{y}-z{z}',
                     path.join(base_dir, f'z{z}-y{y:02}-x{x:02}.jpeg')] for x in range(2)]
                p.map(download_and_save_tile, args)

    z = 4
    base_dir = path.join(RAW_BASE_DIR, f'z{z}', '='.join(user_panoid))
    if REDOWNLOAD_EXISTING or not path.isdir(base_dir):
        makedirs(base_dir, exist_ok=True)
        args = []
        for y in range(2, 6):
            args.extend([
                [BASE_URL + f'{user_panoid[0]}=x{x}-y{y}-z{z}',
                    path.join(base_dir, f'z{z}-y{y:02}-x{x:02}.jpeg')] for x in range(16)])

        with Pool() as p:
            p.map(download_and_save_tile, args)
