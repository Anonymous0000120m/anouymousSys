import sys
import socket
import requests
import datetime

def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror as e:
        print("Error resolving domain name:", e)
        return None

def get_location(ip_address):
    try:
        url = f"https://ipapi.co/{ip_address}/json/"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        latitude = data['latitude']
        longitude = data['longitude']
        return latitude, longitude
    except requests.exceptions.RequestException as e:
        print("Error fetching location data:", e)
        return None, None
    except KeyError as e:
        print("Error parsing location data:", e)
        return None, None

def log_location(ip_address, latitude, longitude):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}: IP Address: {ip_address}, Latitude: {latitude}, Longitude: {longitude}\n"
    with open("location_log.txt", "a") as log_file:
        log_file.write(log_entry)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py domain")
        sys.exit(1)
    
    domain = sys.argv[1]

    ip_address = get_ip_address(domain)
    if ip_address:
        latitude, longitude = get_location(ip_address)
        if latitude is not None and longitude is not None:
            print("Latitude:", latitude)
            print("Longitude:", longitude)
            log_location(ip_address, latitude, longitude)
        else:
            print("Failed to fetch location data for IP:", ip_address)
    else:
        print("Failed to resolve IP address for domain:", domain)
