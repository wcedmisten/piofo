import psycopg2
import psycopg2.extras
import json

OUTPATH="/home/wedmisten/piofo/20220605145527_005152"

with open(f'{OUTPATH}/ocr_gpx.json', 'r') as ocr_gpx_file:
    ocr_gpx = json.load(ocr_gpx_file)


# Connect to your postgres DB
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres port=5432 password=password")

# Open a cursor to perform database operations
cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

def construct_query():
    return f"""SELECT osm_id, name, maxspeed, highway, 
way <-> ST_Transform(ST_GeomFromText('POINT(%s %s)',4326),3857) AS dist
FROM planet_osm_roads
WHERE highway IS NOT NULL
ORDER BY dist
LIMIT 3;"""


for key, item in ocr_gpx.items():
    if 'limit' in item['ocr'] or 'speed' in item['ocr']:
        lat, lon = item['latlon']
        
        # Execute a query
        cur.execute(construct_query(), [lon, lat])

        # Retrieve query results
        records = cur.fetchall()

        for row in records:
            print(row)

