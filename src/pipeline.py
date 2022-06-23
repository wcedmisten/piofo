from nvtk_mp42gpx import main
import ocr
import osm_search

import shutil

import subprocess

import os

# get the path of the "piofo" directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WORKSPACE_DIR = f'{BASE_DIR}/workspace'

fname_base = '20220531181027_004969'
input_mp4='/home/wedmisten/Videos/dashcam_2/20220531181027_004969.MP4'

VIDEO_WORKSPACE = f"{WORKSPACE_DIR}/{fname_base}"

gpx_filename = f'{VIDEO_WORKSPACE}/{fname_base}.gpx'

# create the GPX file and extract 1-second images
def create_gpx_and_jpg():
    print("Deleting directory: ", VIDEO_WORKSPACE)
    # shutil.rmtree(f"{WORKSPACE_DIR}/{fname_base}")

    os.mkdir(VIDEO_WORKSPACE)

    # generate the GPX file
    main(['-i', f'{input_mp4}', '-o', gpx_filename, '-f'])
    # extract 1-second images
    ffmpeg_cmd = ['ffmpeg', '-i', input_mp4, '-qscale:v', '1', '-vf', "crop=2560:1395:0:0", '-r', '1', f"{VIDEO_WORKSPACE}/{fname_base}_%03d.jpg"]

    rc = subprocess.call(ffmpeg_cmd)

# step 1, create the GPX and JPG files
# create_gpx_and_jpg()

# step 2, run OCR on the images
# ocr.run_ocr(VIDEO_WORKSPACE)

# step 3, search the OSM DB for nearest roads
osm_search.search_osm(fname_base, VIDEO_WORKSPACE, gpx_filename)

