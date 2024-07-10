from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
import folium
from prettytable import PrettyTable
import logging
import sys

# Set up logging
logging.basicConfig(filename='geolocation_errors.log', level=logging.ERROR)

def log_error(e):
    """Log the error to a file."""
    logging.error(e)

def create_table(location, zip_code):
    """Create a pretty table for displaying location information."""
    table = PrettyTable()
    table.field_names = ["Description", "Value"]
    table.add_row(['Full Location', location.address])
    table.add_row(['Latitude', location.latitude])
    table.add_row(['Longitude', location.longitude])
    table.add_row(['Zip Code', zip_code])
    table.add_row(['City', location.raw.get('address', {}).get('city', 'N/A')])
    table.add_row(['Country', location.raw.get('address', {}).get('country', 'N/A')])
    return table

def get_geolocator():
    """Initialize and return a geolocator instance."""
    """Day One of not making significant changes to my project """
    return Nominatim(user_agent="abcd")

def get_location_info(place):
    """Get location information for a given place name."""
    try:
        geolocator = get_geolocator()
        location = geolocator.geocode(place)
        if location:
            zip_code = location.raw.get('address', {}).get('postcode', 'N/A')
            table = create_table(location, zip_code)
            print(table)
        else:
            print("Location not found.")
    except GeocoderServiceError as e:
        print("Geocoding error:", e)
        log_error(e)

def reverse_geocode(lat, lon):
    """Get location information for given latitude and longitude"""
    try:
        geolocator = get_geolocator()
        location = geolocator.reverse((lat, lon))
        if location:
            zip_code = location.raw.get('address', {}).get('postcode', 'N/A')
            table = create_table(location, zip_code)
            print(table)
        else:
            print("Location not found.")
    except GeocoderServiceError as e:
        print("Geocoding error:", e)
        log_error(e)

def visualize_location(lat, lon):
    """Create a map with a marker at the given latitude and longitude."""
    map_ = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker([lat, lon], popup="Location").add_to(map_)
    folium.CircleMarker([lat, lon], radius=50, color='red', fill=True, fill_color='red').add_to(map_)
    folium.LayerControl().add_to(map_)
    return map_

def process_multiple_locations(locations):
    """Process multiple locations."""
    for place in locations:
        get_location_info(place.strip())

def display_menu():
    """Display the menu options."""
    print("Choose an option:")
    print("1. Enter a place name")
    print("2. Enter coordinates (latitude and longitude)")
    print("3. Batch process locations from a file")

def main():
    """Main function to run the script."""
    if len(sys.argv) > 1:
        # Process command-line arguments
        if sys.argv[1] == 'place':
            place = ' '.join(sys.argv[2:])
            get_location_info(place)
        elif sys.argv[1] == 'coords':
            try:
                lat = float(sys.argv[2])
                lon = float(sys.argv[3])
                reverse_geocode(lat, lon)
                map_ = visualize_location(lat, lon)
                map_.save('location.html')
                print("Map saved as 'location.html'. Open this file in a browser to view the location.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter numeric values for latitude and longitude.")
        else:
            print("Invalid arguments. Usage: script.py place <place_name> or script.py coords <latitude> <longitude>")
    else:
        # Interactive input
        display_menu()
        choice = input("Enter your choice: ")
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
        elif choice == '3':
            file_path = input('Enter the file path: ')
            try:
                with open(file_path, 'r') as file:
                    locations = file.readlines()
                process_multiple_locations(locations)
            except FileNotFoundError:
                print("File not found. Please check the file path and try again.")
        else:
            print("Invalid choice. Please try running the script again.")

if __name__ == "__main__":
    main()
