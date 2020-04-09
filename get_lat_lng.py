from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='corona_india_data')

def extract_district_name(district_name):
    print('finding latitude longitude for ' + district_name)
    if '\n' in district_name:
        district_name = district_name.split('\n')[0]
    if '(' in district_name:
        district_name = district_name.split('(')[0]
    if ')' in district_name:
        district_name = district_name.split(')')[0]

    return district_name

def get_lat_lang(district_name):
    district_name = extract_district_name(district_name)
    try:
        location = geolocator.geocode(district_name + ', India')
        print('latitude = ' + str(location.latitude))
        print('longitude = ' + str(location.longitude))
        return (location.latitude, location.longitude)
    except:
        Warning('latitude and longitude not found for ' + district_name)
        print('Manually enter latitude and longitude for ' + district_name)
        latitude = float(input("Enter latitude : "))
        longitude = float(input("Enter longitude : "))
        return (latitude, longitude)
