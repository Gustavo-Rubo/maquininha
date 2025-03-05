import json
import numpy as np
import matplotlib.pyplot as plt
from os import path

panoids = np.load('../panoids.npy')
user_panoids = np.load('../user_panoids.npy')
with open(path.join('..', '..', 'data', 'database.json', 'r')) as f:
    data = json.load(f)
    ocr_panoids = [[d['panoid'], d['long'], d['lat']] for d in data]
    ocr_panoids = np.array(ocr_panoids)


im_usp = plt.imread('usp.png')
plt.imshow(im_usp, zorder=0)
IM_W = 1281
IM_H = 945

# -23.54893638234242, -46.709208684501455
LAT_0 = -23.54893638234242
LONG_0 = -46.745772557715696-1.2e-4

LAT_D = LAT_0 + 23.57344373805996+1.2e-4
LONG_D = LONG_0 + 46.709208684501455

plt.scatter(
    -IM_W*(ocr_panoids[:, 1].astype('float')-LONG_0)/LONG_D,
    -IM_H*(ocr_panoids[:, 2].astype('float')-LAT_0)/LAT_D,
    color='red', marker='+', s=40, label='panoids with ocr')
plt.scatter(
    -IM_W*(panoids[:, 1].astype('float')-LONG_0)/LONG_D,
    -IM_H*(panoids[:, 2].astype('float')-LAT_0)/LAT_D,
    color='blue', marker='.', s=20, label='panoids')
plt.scatter(
    -IM_W*(user_panoids[:, 1].astype('float')-LONG_0)/LONG_D,
    -IM_H*(user_panoids[:, 2].astype('float')-LAT_0)/LAT_D,
    color='orange', marker='.', s=20, label='user panoids')
plt.legend(loc='upper right')

plt.ylim([840, 50])
plt.xlim([30, 1200])
plt.axis('off')
plt.tight_layout()

plt.show()
