import json
import glob
import os

import easyocr
reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory


def run_ocr(OUTPATH, BATCH_SIZE=2):
    if os.path.exists(f"{OUTPATH}/ocr.json"):
        return
    else:
        images = glob.glob(f"{OUTPATH}/*.jpg")

        print("Running OCR on ", len(images), "images")

        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        data = {}

        for group in chunks(images, BATCH_SIZE):
            images = [
                url for url in group
            ]

            # Each list of predictions in prediction_groups is a list of
            # (word, box) tuples.
            prediction_groups = reader.readtext_batched(images)

            for filename, prediction in zip(group, prediction_groups):
                data[filename] = list(map(lambda pred: pred[1], prediction))

        with open(f"{OUTPATH}/ocr.json", 'w') as f:
            json.dump(data, f, indent=2)
