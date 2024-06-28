from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
import folium
from prettytable import PrettyTable

def get_location_info(place):
    try:
        geolocator = Nominatim(user_agent="abcd")
        location = geolocator.geocode(place)
        
        if location:
            data = location.raw
            loc_data = data['display_name'].split()
            zip_code = loc_data[-3] if len(loc_data) >= 3 else 'N/A'
            table = PrettyTable()
            table.field_names = ["Description", "Value"]
            table.add_row(['Full Location', location.address])
            table.add_row(['Latitude', location.latitude])
            table.add_row(['Longitude', location.longitude])
            table.add_row(['Zip Code', zip_code])
            print(table)
        else:
            print("Location not found.")
    except GeocoderServiceError as e:
        print("Geocoding error:", e)

def reverse_geocode(lat, lon):
    try:
        geolocator = Nominatim(user_agent="abcd")
        location = geolocator.reverse((lat, lon))
        
        if location:
            data = location.raw
            loc_data = data['display_name'].split()
            zip_code = loc_data[-3] if len(loc_data) >= 3 else 'N/A'
            table = PrettyTable()
            table.field_names = ["Description", "Value"]
            table.add_row(['Full Location', location.address])
            table.add_row(['Latitude', location.latitude])
            table.add_row(['Longitude', location.longitude])
            table.add_row(['Zip Code', zip_code])
            print(table)
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
        try:
            lat = float(input('Enter Latitude: '))
            lon = float(input('Enter Longitude: '))
            reverse_geocode(lat, lon)
            map_ = visualize_location(lat, lon)
            map_.save('location.html')
            print("Map saved as 'location.html'. Open this file in a browser to view the location.")
        except ValueError:
            print("Invalid input. Please enter numeric values for latitude and longitude.")
    else:
        print("Invalid choice. Please try running the scrip again")

if __name__ == "__main__":
    main()
