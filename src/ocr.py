import json
import glob
import os

import keras_ocr


def run_ocr(OUTPATH, BATCH_SIZE=4):
    if os.path.exists(f"{OUTPATH}/ocr.json"):
        return
    else:
        pipeline = keras_ocr.pipeline.Pipeline(scale=1)

        images = glob.glob(f"{OUTPATH}/*.jpg")

        print("Running OCR on ", len(images), "images")

        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        data = {}

        for group in chunks(images, BATCH_SIZE):
            images = [
                keras_ocr.tools.read(url) for url in group
            ]

            # Each list of predictions in prediction_groups is a list of
            # (word, box) tuples.
            prediction_groups = pipeline.recognize(images)

            for filename, prediction in zip(group, prediction_groups):
                data[filename] = list(map(lambda pred: pred[0], prediction))

        with open(f"{OUTPATH}/ocr.json", 'w') as f:
            json.dump(data, f, indent=2)
