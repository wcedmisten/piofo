#!/bin/bash
#
# Author: Tod Fitch (tod at fitchfamily dot org)
#         William Edmisten
# License: GPL3
# Warranty: NONE! Use at your own risk!
# Disclaimer: Quick and dirty hack.
# Description: This script extract geo referenced images from
#              Novatek generated MP4 files.
#

#
#   Uses a python script to extract GPS data from the Viofo A119
#   Script is available at:
#
#       https://sergei.nz/extracting-gps-data-from-viofo-a119-and-other-novatek-powered-cameras/
#
#   Also uses ffmpeg and exiftool.

set -e

src=${1}
skew=${2:-0.0}

ext='.jpg'

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null;)

#
#   The nvtk_mp42gpx script assumes the times it finds in the video
#   are the same as the GPX standard (GMT/UTC) but the dash cam is
#   is typically set to local time. Just make everthing else assume
#   GMT/UTC too so they are all working on the same timezone
#
export TZ=Etc/UTC

#
# Output is to a subdirectory with a name based on the base file name for
# the video file.
#
fname="${src##*/}"
outname="${fname%.*}"
gpx="${outname}/${outname}.gpx"

#
#   Create output directory, copy video into output
#   extract GPX into output directory
#
rm -rf "${outname}"
mkdir -p "${outname}"
rm -rf "${outname}/*${ext}"
cp -p "${src}" "${outname}/${fname}"
${SCRIPT_DIR}/nvtk_mp42gpx.py "-i${outname}/${fname}" "-o${gpx}" -f


ffmpeg -i "${outname}/${fname}" -qscale:v 1 -vf "crop=2560:1395:0:0" -r 1 "${outname}/${outname}_%03d.jpg"

#
#   Clean up after ourselves
#
rm -f ${outname}/*original
rm -f ${outname}/*.MP4
