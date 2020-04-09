import geopy.geocoders
from geopy.geocoders import Nominatim
import ssl
import certifi
from json import load as json_load

geopy.geocoders.options.default_user_agent = "corona_india_data"
geopy.geocoders.options.default_timeout = 7
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
geolocator = Nominatim()

def extract_district_name(district_name):
    print('finding latitude longitude for ' + district_name)
    if '\n' in district_name:
        district_name = district_name.split('\n')[0]
    if '(' in district_name:
        district_name = district_name.split('(')[0]
    if ')' in district_name:
        district_name = district_name.split(')')[0]

    return district_name

def extract_state_name(state_name):
    print('finding latitude longitude for ' + state_name)
    if '*' in state_name:
        state_name = state_name.split('*')[0]
    return state_name

def get_lat_lang(district_name, state_name, previous_data):
    #first search for lat, lng in previously uploaded data
    with open(previous_data) as json_file:
        data = json_load(json_file)
    
    if district_name: #function called to get lat, lng for district
        if state_name in data.keys():
            if district_name in data[state_name]['districts'].keys():
                district_field_keys = data[state_name]['districts'][district_name].keys()

                if 'latitude' in district_field_keys and 'longitude' in district_field_keys:
                    latitude = data[state_name]['districts'][district_name]['latitude']
                    longitude = data[state_name]['districts'][district_name]['longitude']
                    return (latitude, longitude)

        district_name = extract_district_name(district_name)
    else: #function called to get lat, lng for state
        if state_name in data.keys():
            state_field_keys = data[state_name].keys()
            if 'latitude' in state_field_keys and 'longitude' in state_field_keys:
                latitude = data[state_name]['latitude']
                longitude = data[state_name]['longitude']
                return (latitude, longitude)
    
        state_name = extract_state_name(state_name)
    
    try:
        if district_name:
            location = geolocator.geocode(district_name + ', ' + state_name + ', India')
        else:
            location = geolocator.geocode(state_name + ', India')
        print('latitude = ' + str(location.latitude))
        print('longitude = ' + str(location.longitude))
        return (location.latitude, location.longitude)
    except:
        if district_name:
            Warning('latitude and longitude not found for ' + district_name)
            print('Manually enter latitude and longitude for ' + district_name)
        else:
            Warning('latitude and longitude not found for ' + state_name)
            print('Manually enter latitude and longitude for ' + state_name)
        latitude = float(input("Enter latitude : "))
        longitude = float(input("Enter longitude : "))
        return (latitude, longitude)
