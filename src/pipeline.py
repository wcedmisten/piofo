from nvtk_mp42gpx import main
import ocr
import osm_search

import shutil

import subprocess

import os
from pathlib import Path

# create the GPX file and extract 1-second images
def create_gpx_and_jpg(input_mp4, gpx_filename, VIDEO_WORKSPACE):
    if not os.path.exists(input_mp4):
        print("Video file not found! ", input_mp4)
        return

    if not os.path.exists(VIDEO_WORKSPACE):
        print("Creating workspace ", VIDEO_WORKSPACE)
        os.mkdir(VIDEO_WORKSPACE)

    # print("Deleting directory: ", VIDEO_WORKSPACE)
    # shutil.rmtree(f"{WORKSPACE_DIR}/{fname_base}")

    if not os.path.exists(gpx_filename):
        print("Creating GPX file")
        # generate the GPX file
        main(['-i', f'{input_mp4}', '-o', gpx_filename, '-f'])
    
    if not os.path.exists(f"{VIDEO_WORKSPACE}/{fname_base}_001.jpg"):
        print("Extracting images")
        # extract 1-second images
        ffmpeg_cmd = ['ffmpeg', '-i', input_mp4, '-qscale:v', '1', '-vf', "crop=2560:1395:0:0", '-r', '1', f"{VIDEO_WORKSPACE}/{fname_base}_%03d.jpg"]

        rc = subprocess.call(ffmpeg_cmd)


# get the path of the "piofo" directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WORKSPACE_DIR = f'{BASE_DIR}/workspace'

input_mp4='/home/wedmisten/Videos/dashcam_2/20220602164844_005000.MP4'
fname_base = Path(input_mp4).stem


VIDEO_WORKSPACE = f"{WORKSPACE_DIR}/{fname_base}"

gpx_filename = f'{VIDEO_WORKSPACE}/{fname_base}.gpx'

# step 1, create the GPX and JPG files
create_gpx_and_jpg(input_mp4, gpx_filename, VIDEO_WORKSPACE)

# step 2, run OCR on the images
ocr.run_ocr(VIDEO_WORKSPACE)

# step 3, search the OSM DB for nearest roads
osm_search.search_osm(fname_base, VIDEO_WORKSPACE, gpx_filename)

