# piofo
A Python library for extracting GPS data / images from Viofo dashcam videos.

# Requirements

* ffmpeg

# Install Dependencies

```bash
sudo apt-get install ffmpeg
```

```bash
pip install -r requirements.txt
```

# Setting up PostGIS with OSM data

Clone the [wcedmisten/osm2pgsql-docker](https://github.com/wcedmisten/osm2pgsql-docker) repo,
and follow the steps from the README.

# Running the pipeline

The entire pipeline does the following:

* extract the GPS track from a dashcam clip
* extract corresponding images for each point
* run OCR on each image 
* if a "speed limit" sign is found in the image, check OSM to see if the road has "maxspeed" set
* if a missing speed limit is found, output a link to the image, and a link to the OSM feature

```bash
python src/pipeline.py /path/to/input.MP4
```

# Testing

python3 -m unittest test/test.py

# Original Sources:

https://sergei.nz/extracting-gps-data-from-viofo-a119-and-other-novatek-powered-cameras/

https://sergei.nz/files/nvtk_mp42gpx.py
