import nvtk_mp42gpx
import ocr
import osm_search

import argparse
import subprocess
import os
from pathlib import Path

# create the GPX file and extract 1-second images
def create_gpx_and_jpg(input_mp4, gpx_filename, video_workspace, fname_base):
    if not os.path.exists(input_mp4):
        print("Video file not found! ", input_mp4)
        return

    if not os.path.exists(video_workspace):
        print("Creating workspace ", video_workspace)
        os.mkdir(video_workspace)

    if not os.path.exists(gpx_filename):
        print("Creating GPX file")
        # generate the GPX file
        nvtk_mp42gpx.main(['-i', f'{input_mp4}', '-o', gpx_filename, '-f'])
    
    if not os.path.exists(f"{video_workspace}/{fname_base}_001.jpg"):
        print("Extracting images")
        # extract 1-second images
        ffmpeg_cmd = ['ffmpeg', '-i', input_mp4, '-qscale:v', '1', '-vf', "crop=2560:1395:0:0", '-r', '1', f"{video_workspace}/{fname_base}_%03d.jpg"]
        rc = subprocess.call(ffmpeg_cmd)


# get the path of the "piofo" directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = f'{BASE_DIR}/workspace'

def main(input_mp4):
    fname_base = Path(input_mp4).stem

    video_workspace = f"{WORKSPACE_DIR}/{fname_base}"

    gpx_filename = f'{video_workspace}/{fname_base}.gpx'

    # step 1, create the GPX and JPG files
    create_gpx_and_jpg(input_mp4, gpx_filename, video_workspace, fname_base)

    # step 2, run OCR on the images
    ocr.run_ocr(video_workspace)

    # step 3, search the OSM DB for nearest roads
    osm_search.search_osm(fname_base, video_workspace, gpx_filename)

parser = argparse.ArgumentParser(description='Process a dashcam file to find missing features.')
parser.add_argument('input_video_file', type=str,
                    help='A Viofo Dashcam Video File')


args = parser.parse_args()

main(str(args.input_video_file))
