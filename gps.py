import gpsd

def get_gps_coordinates():
    try:
        # 连接到gpsd服务
        gpsd.connect()

        # 获取GPS信息
        packet = gpsd.get_current()

        # 提取经纬度信息
        latitude = packet.lat
        longitude = packet.lon

        return latitude, longitude
    except Exception as e:
        print("Error fetching GPS coordinates:", e)
        return None, None

if __name__ == "__main__":
    latitude, longitude = get_gps_coordinates()
    if latitude is not None and longitude is not None:
        print("Latitude:", latitude)
        print("Longitude:", longitude)
    else:
        print("Failed to fetch GPS coordinates.")

#https://nominatim.openstreetmap.org/ui/search.html