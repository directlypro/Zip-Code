from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
import folium

def get_location_info(place):
    try:
        geolocator = Nominatim(user_agent="abcd")
        location = geolocator.geocode(place)
        
        if location:
            data = location.raw
            loc_data = data['display_name'].split()
            print('Full Location:', location.address)
            print('Latitude:', location.latitude)
            print('Longitude:', location.longitude)
            print('Zip Code:', loc_data[-3])
        else:
            print("Location not found.")
    except GeocoderServiceError as e:
        print("Geocoding error:", e)

def reverse_geocode(lat, lon):
    try:
        geolocator = Nominatim(user_agent="abcd")
        location = geolocator.reverse((lat, lon))
        
        if location:
            print('Full Location:', location.address)
            print('Latitude:', location.latitude)
            print('Longitude:', location.longitude)
        else:
            print("Location not found.")
    except GeocoderServiceError as e:
        print("Geocoding error:", e)

def visualize_location(lat, lon):
    map_ = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker([lat, lon], popup="Location").add_to(map_)
    return map_

def main():
    choice = input("Enter '1' for place name or '2' for coordinates: ")
    if choice == '1':
        place = input('Enter Place: ')
        get_location_info(place)
    elif choice == '2':
        lat = float(input('Enter Latitude: '))
        lon = float(input('Enter Longitude: '))
        reverse_geocode(lat, lon)
        map_ = visualize_location(lat, lon)
        map_.save('location.html')
        print("Map saved as 'location.html'. Open this file in a browser to view the location.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
