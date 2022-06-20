from gpxplotter import create_folium_map, read_gpx_file, add_segment_to_map
import folium
import json

import gpxpy
import gpxpy.gpx

FILE_NAME = '20220605145527_005152'
WORKING_DIR = f'/home/wedmisten/piofo/{FILE_NAME}'

GPX_FILE = f'{WORKING_DIR}/{FILE_NAME}.gpx'

# get a list of coordinates from the GPX file
gpx_points = []
with open(GPX_FILE, 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                gpx_points.append((point.latitude, point.longitude))

# read the OCR data
ocr_data = {}
with open(f"{WORKING_DIR}/ocr.json", 'r') as ocr_data_file:
    ocr_data = json.load(ocr_data_file)

for key in ocr_data.keys():
    tmp = ocr_data[key]
    ocr_data[key] = {}
    ocr_data[key]['ocr'] = tmp

# Add, markers to the gps-locations we read from the images
for idx, latlon in enumerate(gpx_points):
    filepath = f'{WORKING_DIR}/{FILE_NAME}_{(idx+1):03}.jpg'

    if filepath not in ocr_data:
        print(filepath)
        ocr_data[filepath] = {'ocr': []}

    ocr_data[filepath]['latlon'] = latlon

    if 'speed' in ocr_data[filepath]['ocr'] or 'limit' in ocr_data[filepath]['ocr']:
        print(ocr_data[filepath]['ocr'], ocr_data[filepath]['latlon'])

folium_map = create_folium_map()
for track in read_gpx_file(GPX_FILE):
    for i, segment in enumerate(track['segments']):
        add_segment_to_map(folium_map, segment)


# Add, markers to the gps-locations we read from the images
for idx, latlon in enumerate(gpx_points):
    filepath = f'{WORKING_DIR}/{FILE_NAME}_{(idx+1):03}.jpg'

    words = "<br>".join(ocr_data.get(filepath, {}).get('ocr', []))

    marker = folium.Marker(
        location=latlon,
        popup = folium.Popup(
        f'<p style="font-size:30px">{words}</p><img alt="img" src="{filepath}", width=200px/>',
        show=(idx % 10 == 0),
    ))
    marker.add_to(folium_map)

boundary = folium_map.get_bounds()
folium_map.fit_bounds(boundary, padding=(3, 3))

# Display initial map:
folium_map.save(f'{WORKING_DIR}/test.html')

with open(f"{WORKING_DIR}/ocr_gpx.json", 'w') as f:
    json.dump(ocr_data, f, indent=2)