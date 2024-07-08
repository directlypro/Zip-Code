from flask import Flask, request, render_template, jsonify
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
import folium
import logging
from prettytable import PrettyTable

app = Flask(__name__)

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
    return Nominatim(user_agent="abcd")

def get_location_info(place):
    """Get location information for a given place name."""
    try:
        geolocator = get_geolocator()
        location = geolocator.geocode(place)
        if location:
            zip_code = location.raw.get('address', {}).get('postcode', 'N/A')
            table = create_table(location, zip_code)
            return str(table)
        else:
            return "Location not found."
    except GeocoderServiceError as e:
        log_error(e)
        return f"Geocoding error: {e}"

def reverse_geocode(lat, lon):
    """Get location information for given latitude and longitude"""
    try:
        geolocator = get_geolocator()
        location = geolocator.reverse((lat, lon))
        if location:
            zip_code = location.raw.get('address', {}).get('postcode', 'N/A')
            table = create_table(location, zip_code)
            return str(table)
        else:
            return "Location not found."
    except GeocoderServiceError as e:
        log_error(e)
        return f"Geocoding error: {e}"

def visualize_location(lat, lon):
    """Create a map with a marker at the given latitude and longitude."""
    map_ = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker([lat, lon], popup="Location").add_to(map_)
    folium.CircleMarker([lat, lon], radius=50, color='red', fill=True, fill_color='red').add_to(map_)
    folium.LayerControl().add_to(map_)
    map_.save('static/location.html')
    return 'location.html'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/geocode', methods=['POST'])
def geocode():
    data = request.json
    place = data.get('place')
    if place:
        result = get_location_info(place)
        return jsonify({'result': result})
    return jsonify({'error': 'No place provided'}), 400

@app.route('/reverse', methods=['POST'])
def reverse():
    data = request.json
    lat = data.get('lat')
    lon = data.get('lon')
    if lat and lon:
        result = reverse_geocode(lat, lon)
        return jsonify({'result': result})
    return jsonify({'error': 'No coordinates provided'}), 400

@app.route('/map', methods=['POST'])
def map_view():
    data = request.json
    lat = data.get('lat')
    lon = data.get('lon')
    if lat and lon:
        map_file = visualize_location(lat, lon)
        return jsonify({'map_file': map_file})
    return jsonify({'error': 'No coordinates provided'}), 400

if __name__ == "__main__":
    app.run(debug=True)

