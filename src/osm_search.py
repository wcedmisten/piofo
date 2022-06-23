import json

import gpxpy
import gpxpy.gpx

import psycopg2
import psycopg2.extras
import json

from PIL import Image


def search_osm(FILE_NAME, WORKING_DIR, GPX_FILE):
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


    # Connect to your postgres DB
    conn = psycopg2.connect("host=localhost dbname=postgres user=postgres port=5432 password=password")

    # Open a cursor to perform database operations
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    osm_query = """SELECT osm_id, name, maxspeed, highway, 
    way <-> ST_Transform(ST_GeomFromText('POINT(%s %s)',4326),3857) AS dist
    FROM planet_osm_roads
    WHERE highway IS NOT NULL
    ORDER BY dist
    LIMIT 1;"""


    for key, item in ocr_data.items():
        if 'limit' in item['ocr'] or 'speed' in item['ocr']:
            lat, lon = item['latlon']
            
            # Execute a query
            cur.execute(osm_query, [lon, lat])

            # Retrieve query results
            records = cur.fetchall()

            print()

            for row in records:
                if row['maxspeed'] == None:
                    print("WARNING! NO SPEED LIMIT TAGGED IN OSM,")
                    print("BUT OCR FOUND THE FOLLOWING TEXT:")
                    print(item['ocr'])
                # print(json.dumps(row))
                print("Check feature:")
                print(f"https://www.openstreetmap.org/way/{row.get('osm_id')}")

                print("Image:")
                print(f"file://{key}")
