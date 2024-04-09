import sys
import csv
import requests
import logging
from datetime import datetime

# 配置日志记录
logging.basicConfig(filename='geocoding.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def geocode_location(location):
    url = f'https://nominatim.openstreetmap.org/search?q={location}&format=json'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            first_result = data[0]
            latitude = float(first_result['lat'])
            longitude = float(first_result['lon'])
            return latitude, longitude
        else:
            logging.error(f'Failed to geocode location: {location}')
            return None, None
    except requests.exceptions.RequestException as e:
        logging.error(f'Error fetching location data: {e}')
        return None, None

def save_to_csv(data):
    with open('geocoding_results.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def main():
    if len(sys.argv) < 2:
        print('Usage: python script.py <location>')
        return

    location = ' '.join(sys.argv[1:])
    latitude, longitude = geocode_location(location)
    if latitude is not None and longitude is not None:
        print(f'Latitude: {latitude}, Longitude: {longitude}')
        save_to_csv([location, latitude, longitude])
        logging.info(f'Successfully geocoded location: {location}')
    else:
        print('Failed to geocode location. Check logs for details.')

if __name__ == "__main__":
    main()

