from geopy.geocoders import Nominatim 

def zip_code():
    place = input('Enter Place :')

    geolocator = Nominatim(user_agent="abcd")
    location = geolocator.geocode(place)

    data = location.raw
    loc_data = data['display_name'].split()
    print('Full Location')
    print(loc_data)
    print("Zip Code :", loc_data[-3])

zip_code()

