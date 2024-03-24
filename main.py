import os
import csv
import json

def extract_coordinates(geojson_file):
    with open(geojson_file, 'r') as f:
        data = json.load(f)
        
    coordinates = []
    for feature in data['features']:
        location_name = feature['properties'].get('name', '')
        geometry_type = feature['geometry']['type']
        if geometry_type == 'MultiPolygon':
            coords = feature['geometry']['coordinates']
            for polygon in coords:
                for sub_polygon in polygon:
                    for point in sub_polygon:
                        coordinates.append((location_name, point[1], point[0]))
        else:
            print("Unsupported geometry type:", geometry_type)
    
    return coordinates

def write_coordinates_to_csv(coordinates, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Latitude', 'Longitude'])
        for name, lat, lon in coordinates:
            writer.writerow([name, lat, lon])

def process_geojson_files(path):
    geojson_files = [f for f in os.listdir(path) if f.endswith('.geojson')]
    for file in geojson_files:
        cur_path = os.path.join(path, file)
        file_name = os.path.splitext(file)[0]
        output_file = f'{file_name}.csv'
        coordinates = extract_coordinates(cur_path)
        write_coordinates_to_csv(coordinates, output_file)

# Provide the path to the directory containing GeoJSON files
path = 'Geojson_shapefiles'
process_geojson_files(path)
