import unittest
import subprocess
import os

import gpxpy
import datetime

from PIL import Image

from src.extract_geotag import get_geotagging

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

print(THIS_DIR)


class TestScript(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestScript, cls).setUpClass()
        subprocess.call(
            [
                f"{THIS_DIR}/../src/dashcam2josm.sh",
                "test/data/small_dashcam.MP4",
            ],
            # suppress stdout and stderr from ffmpeg
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def test_gpx(self):
        with open(f"{THIS_DIR}/../small_dashcam/small_dashcam.gpx", "r") as gpx_file:
            gpx = gpxpy.parse(gpx_file)

            expected_points = [
                {
                    "latitude": 38.067253,
                    "longitude": -78.485986,
                    "time": datetime.datetime(
                        2022, 5, 18, 17, 8, 8, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "latitude": 38.067253,
                    "longitude": -78.485986,
                    "time": datetime.datetime(
                        2022, 5, 18, 17, 8, 8, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "latitude": 38.067244,
                    "longitude": -78.485994,
                    "time": datetime.datetime(
                        2022, 5, 18, 17, 8, 10, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "latitude": 38.06724,
                    "longitude": -78.485994,
                    "time": datetime.datetime(
                        2022, 5, 18, 17, 8, 11, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "latitude": 38.06724,
                    "longitude": -78.485994,
                    "time": datetime.datetime(
                        2022, 5, 18, 17, 8, 12, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "latitude": 38.06724,
                    "longitude": -78.485994,
                    "time": datetime.datetime(
                        2022, 5, 18, 17, 8, 13, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "latitude": 38.06724,
                    "longitude": -78.485994,
                    "time": datetime.datetime(
                        2022, 5, 18, 17, 8, 14, tzinfo=datetime.timezone.utc
                    ),
                },
            ]

            points = []

            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        points.append(
                            {
                                "latitude": point.latitude,
                                "longitude": point.longitude,
                                "time": point.time,
                            }
                        )

            self.assertEqual(expected_points, points)
    # cleanup files
    @classmethod
    def tearDownClass(cls):
        os.remove(f"{THIS_DIR}/../small_dashcam/small_dashcam.gpx")

        for i in range(1, 8):
            os.remove(f"{THIS_DIR}/../small_dashcam/small_dashcam_00{i}.jpg")


if __name__ == "__main__":
    unittest.main()
