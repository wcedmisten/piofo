#!/bin/bash
#
# Author: Tod Fitch (tod at fitchfamily dot org)
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

#   The place you can find videos on a Macintosh when a microSD card
#   formatted by a Viofo A119s v2 camera is mounted.
sdcard="/Volumes/VOLUME1/DCIM/Movie/"
src=${1}
skew=${2:-0.0}

ext='.jpg'

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null;)

#
#   truncate a positive floating point bc number to integer
#
trunc() {
    e=${1:-0}
    r=$( echo "scale=0; (${e})/1" | bc -l )
    echo ${r}
}

#
#   Way more kludgy than I'd like. Extract hours, minutes, seconds as strings
#   then convert them while forcing base 10. If extracted as numbers then
#   08 and 09 give errors as they are not proper octal.
#
#   Once we have hours, minutes and seconds then easy conversion to seconds
#   since midnight.
#
seconds() {
    t1=${1:-11:48:30}
    t1s="${t1##*:}"   # Extract the seconds from $t1
    t1s=$((10#$t1s))
    t1h="${t1%%:*}"   # Extract the hours from $t1
    t1h=$((10#$t1h))
    t1m=${t1%:*}    # Extract the minutes from $t1 (step 1)
    t1m="${t1m#*:}"   # Extract the minutes from $t1 (step 2)
    t1m=$((10#$t1m))
    t1ssm=$((t1h * 3600 + t1m * 60 + t1s)) # Calculate $t1 seconds since midnight
    #echo "${t1} -> ${t1ssm}"
    echo ${t1ssm}
}

#
#   The reverse of seconds(). Return string formatted as hh:mm:ss.0
hms() {
    s=${1:-12345.6789}
    h=$( echo "scale=0 ; ${s} / 3600.0000" | bc -l )
    s=$( echo "scale=4 ; ${s} - (${h} * 3600)" | bc -l)
    m=$( echo "scale=0 ; ${s} / 60.0000" | bc -l)
    s=$( echo "scale=4 ; ${s} - (${m} * 60)" | bc -l)

    ph=`printf "%02d" $h`
    pm=`printf "%02d" $m`
    ps=`printf "%02.6f" $s`
    if [[ ${ps:0:1} == '0' ]]
    then
        ps="0${ps}"
    fi
    echo "$ph:$pm:$ps"
}

#
#   Search various places for the desired video starting with the
#   filename/path as given. If not found, the see if a file of that
#   name is available on the microSD card.
#
if [ -f "${src}" ]
then
    path="${src}"
else
    if [ -f "${src}.MP4" ]
    then
        path="${src}.MP4"
    else
        if [ -f "${sdcard}${src}" ]
        then
            path="${sdcard}${src}"
        else
            if [ -f "${sdcard}${src}.MP4" ]
            then
                path="${sdcard}${src}.MP4"
            else
                echo "${src} not found."
                exit
            fi
        fi
    fi
fi

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
fname="${path##*/}"
outname="${fname%.*}"
gpx="${outname}/${outname}.gpx"

#
#   Create output directory, copy video into output
#   extract GPX into output directory
#
rm -rf "${outname}"
mkdir -p "${outname}"
rm -rf "${outname}/*${ext}"
cp -p "${path}" "${outname}/${fname}"
${SCRIPT_DIR}/nvtk_mp42gpx.py "-i${outname}/${fname}" "-o${gpx}" -f

#
#  For each time stamp in the GPX file, compute the starting offset in
#  the video. We extract a frame from that time stamp and set the image
#  time and data metadata.
#
createTime=-1000
fnum=1
for ts in `grep "time>.*Z" -o ${gpx} | sed 's/time>//' | sed 's/Z//' | sed 's/-/:/g' `
do
    padded_fnum=`printf "%03d" $fnum`
    time=`echo "${ts}" | sed 's/T/ /'`
    s=$(seconds "${time#* }")
    if [ $(trunc $createTime) -lt -100 ]
    then
        createTime=$( echo "scale=4; (${s} + ${skew} - 1.0000)/1" | bc -l )
        echo "GPS time=${s}, skew=${skew}, createTime => ${createTime}"
    fi

    delta=$(echo "scale=4; $s - $createTime" | bc -l)
    echo "delta = ${delta}"

    if [[ ${delta:0:1} != "-" ]]
    then
        ss=$(hms $delta)
        f="${outname}/${outname}_${padded_fnum}${ext}"
        echo "File=\"${f}\", Time=\"${time}\", Sec=${s}, Delta=${delta}, ss=\"${ss}\""

        ffmpeg -ss "${ss}" -i "${outname}/${fname}" -frames:v 1 -qscale:v 1 "${f}"
        exiftool -CreateDate="${time}" -DateTimeOriginal="${time}" -FileModifyDate="${time}" ${f}
        fnum=$(( $fnum + 1 ))
    fi
done

#
#  Tag the extracted images with the GPS location per the GPX file
#
exiftool -geotag "${gpx}" "-Geotime<DateTimeOriginal" -P ${outname}/${outname}*${ext}

#
#   Clean up after ourselves
#
rm -f ${outname}/*original
rm -f ${outname}/*.MP4
