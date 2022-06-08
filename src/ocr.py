import json
import glob

import keras_ocr

OUTPATH="/home/wedmisten/piofo/20220531181027_004969"

pipeline = keras_ocr.pipeline.Pipeline(scale=1)

images = glob.glob(f"{OUTPATH}/*.jpg")

print(len(images))

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

data = {}

for group in chunks(images, 6):
    images = [
        keras_ocr.tools.read(url) for url in group
    ]

    # Each list of predictions in prediction_groups is a list of
    # (word, box) tuples.
    prediction_groups = pipeline.recognize(images)

    for filename, prediction in zip(group, prediction_groups):
        data[filename] = list(map(lambda pred: pred[0], prediction))

with open(f"{OUTPATH}/ocr.json", 'w') as f:
    json.dump(data, f)
