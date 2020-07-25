import json, requests

def _get_poi(ll, limit, query ='tourism'):
    """
        This function accepts lat,long as string and returns JSON | False
        from FourSquare API
    """
    url = 'https://api.foursquare.com/v2/venues/explore'

    params = dict(
        client_id = '2HJQ0DD5O30IL3PEPO1FYG0ML5LQJOOPEEKSXOXQYW1XEO34',
        client_secret = 'BDXLIMSFPXE25N0OTOKXUM2N0UXE3YGVJXZZBRBPQ3FU1IOV',
        v = '20180323',
        ll = ll,
        query= query,
        limit = limit
    )
    resp = requests.get(url = url, params = params)
    data = json.loads(resp.text)
    if(data['meta']['code'] == 200):
        return (data['response']['groups'][0]['items'][0]['venue'])
    else:
        return False

def _get_lat_lng(location_text):
    """
    This method takes the location string as input and returns lat,lng 
    We use Open Source MapQuest Data for this "forward geocoding"
    Uses MapQuest API
    """
    # geocode_auth = '304259759939526855084x6760'
    # geocode_url = 'https://geocode.xyz/
    mapquest_auth_key = 'gUOWtFA8e8fQa8NoxqDGAxTXG4ivcGB9'
    mapquest_api_endpoint = 'https://www.mapquestapi.com/geocoding/v1/address?key=' + mapquest_auth_key + '&inFormat=json&location='
    city_name_to_location = mapquest_api_endpoint + location_text 
    location = requests.get(city_name_to_location)
    geo_code_response = location.json()
    coordinates = []
    # checking successful API response
    if(geo_code_response['info']['statuscode'] == 0):
        coordinates.insert(0, geo_code_response['results'][0]['locations'][0]['displayLatLng']['lat'])
        coordinates.insert(1, geo_code_response['results'][0]['locations'][0]['displayLatLng']['lng'])
        return coordinates
    else:
        return False
