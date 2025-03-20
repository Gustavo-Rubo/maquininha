# scrape_maps

scripts for extracting panorama images from google maps

### panoids.py
opens a .har file and extracts the panoids (panorama ids) from it

the .har file is obtained using by opening firefox devtools in the "network" tab, hovering the mouse over the blue streetview lines and then right click, "save all as HAR"

### panoids2.py
obtains panoids from a set of coordinates that determine vertices of rectangles in a map

### tile.py
reads all panoids and for each of them downloads tiles at zoom levels 1 and 5

### stitch.py
gets all raw tiles and stitches them in one image for each panorama and zoom level

### ocr.py
runs ocr (optical character recognition) on all high resolution images. saves the recognized text in a .json file


## creating the images and thumbs

```
time for i in images_raw/street_view/stitched/z5/*; do convert "$i" -resize 4000x500 -quality 95 webapp/images/"$(basename $i)"; done;
time for i in images_raw/street_view/stitched/z4/*; do convert "$i" -resize 4000x500 -quality 95 webapp/images/"$(basename $i)"; done;
time for i in images_raw/photos/*; do convert "$i" -resize 1000x1000 -quality 95 webapp/images/"$(basename $i)"; done;


time for i in images_raw/street_view/stitched/z5/*; do convert "$i" -resize 400x50 -quality 95 webapp/thumbs/"$(basename $i)"; done;
time for i in images_raw/street_view/stitched/z4/*; do convert "$i" -resize 400x50 -quality 95 webapp/thumbs/"$(basename $i)"; done;
time for i in images_raw/photos/*; do convert "$i" -resize 200x200 -quality 95 webapp/thumbs/"$(basename $i)"; done;
```