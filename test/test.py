import unittest
import subprocess
import filecmp
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

print(THIS_DIR)


class TestScript(unittest.TestCase):
    def test_img1(self):
        subprocess.call(
            [
                f"{THIS_DIR}/../dashcam2josm.sh",
                "test/data/small_dashcam.MP4",
            ],
            # suppress stdout and stderr from ffmpeg
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # self.assertEqual(THIS_DIR, "")
        self.assertTrue(
            filecmp.cmp(
                f"{THIS_DIR}/data/small_dashcam_001.jpg",
                f"{THIS_DIR}/../small_dashcam/small_dashcam_001.jpg",
            ),
            "First image did not match standard data.",
        )

        self.assertTrue(
            filecmp.cmp(
                f"{THIS_DIR}/data/small_dashcam_007.jpg",
                f"{THIS_DIR}/../small_dashcam/small_dashcam_007.jpg",
            ),
            "7th image did not match standard data.",
        )

        self.assertTrue(
            filecmp.cmp(
                f"{THIS_DIR}/data/small_dashcam.gpx",
                f"{THIS_DIR}/../small_dashcam/small_dashcam.gpx",
            ),
            "GPX file did not match standard data",
        )


if __name__ == "__main__":
    unittest.main()
