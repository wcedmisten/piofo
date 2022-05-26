import unittest
import subprocess
import filecmp
import os

from PIL import Image

from src.extract_geotag import get_geotagging

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

print(THIS_DIR)


class TestScript(unittest.TestCase):
    def test_img1(self):
        subprocess.call(
            [
                f"{THIS_DIR}/../src/dashcam2josm.sh",
                "test/data/small_dashcam.MP4",
            ],
            # suppress stdout and stderr from ffmpeg
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        self.assertTrue(
            filecmp.cmp(
                f"{THIS_DIR}/data/small_dashcam.gpx",
                f"{THIS_DIR}/../small_dashcam/small_dashcam.gpx",
            ),
            "GPX file did not match standard data",
        )

        image1 = Image.open(f"{THIS_DIR}/../small_dashcam/small_dashcam_001.jpg")
        image1.verify()

        self.assertEqual(
            {
                "GPSDateStamp": "2022:05:18",
                "GPSImgDirection": 65.87000296120817,
                "GPSImgDirectionRef": "T",
                "GPSLatitude": (38.0, 4.0, 2.1108),
                "GPSLatitudeRef": "N",
                "GPSLongitude": (78.0, 29.0, 9.5496),
                "GPSLongitudeRef": "W",
                "GPSTimeStamp": (17.0, 8.0, 8.0),
                "GPSVersionID": b"\x02\x03\x00\x00",
            },
            get_geotagging(image1._getexif()),
        )

        image7 = Image.open(f"{THIS_DIR}/../small_dashcam/small_dashcam_007.jpg")
        image7.verify()

        self.assertEqual(
            {
                "GPSDateStamp": "2022:05:18",
                "GPSImgDirection": 65.87000296120817,
                "GPSImgDirectionRef": "T",
                "GPSLatitude": (38.0, 4.0, 2.064),
                "GPSLatitudeRef": "N",
                "GPSLongitude": (78.0, 29.0, 9.5784),
                "GPSLongitudeRef": "W",
                "GPSTimeStamp": (17.0, 8.0, 14.0),
                "GPSVersionID": b"\x02\x03\x00\x00",
            },
            get_geotagging(image7._getexif()),
        )

    # cleanup files
    def tearDown(self):
        os.remove(f"{THIS_DIR}/../small_dashcam/small_dashcam.gpx")

        for i in range(1, 8):
            os.remove(f"{THIS_DIR}/../small_dashcam/small_dashcam_00{i}.jpg")


if __name__ == "__main__":
    unittest.main()
