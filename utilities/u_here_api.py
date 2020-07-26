import requests, json

apiKey = 'x_QwMrXk6NkNWpdkZzTsEH1JyzETot06I-FNTd4Ur6Y'

def _get_transit_from_geocode(origin, destination):
    """
        This fucntion will take origin and destination as string [lat,long] & [lat, long] param
        and return a json if all went good else return False
    """
    transit_url = 'https://transit.router.hereapi.com/v8/routes?apiKey='+apiKey
    transit_location = '&origin='+origin+'&destination='+destination
    response = requests.get(transit_url + transit_location)
    if(response.status_code == 200):
        return response.json()
    else:
        return False

def _get_geocode(origin, format='ll'):
    """
        This function will take a location as string param
        and return a geocode string if all went good else return False
    """
    geocode_url = 'https://geocode.search.hereapi.com/v1/geocode?apiKey='+apiKey
    geocode_location = '&q='+ origin
    response = requests.get(geocode_url + geocode_location)
    if(response.status_code == 200):
        response = response.json()['items'][0]
        if(format == 'll'):
            return str(response['position']['lat'])+","+str(response['position']['lng'])
        elif(format == 'lat'):
            return str(response['position']['lat'])
        elif(format == 'lon'):
            return str(response['position']['lng'])
        else:
            return False
    else:
        return False

def _get_poi_from_geocode(origin, poi='tourism', limit='3'):
    """
        This function takes lat,long as comma seperated string param.
        poi or point of interest as string, defaults to tourism
        limit or number of results expected, defaults to 3
        and returns list if all went good else return False
    """
    discover_url = 'https://discover.search.hereapi.com/v1/discover?apiKey='+apiKey
    discover_location = '&limit='+limit+'&q='+poi+'&at='+origin

    response = requests.get(discover_url + discover_location)
    if(response.status_code == 200):
        response = response.json()['items']
        return response
    else:
        return False

def _get_poi_from_name(origin, poi='tourism', limit = '3'):
    """
        This method takes origin as name string
        poi as string (defaults to tourism)
        limit as string (defaults to 3)
        and returns a list with details of said POIs with length = limit
        return defaults to False
    """
    # get geocode first
    geo_code = _get_geocode(origin)
    if(geo_code):
        pass
    else:
        return False
    # get the pois using geo code
    poi = _get_poi_from_geocode(geo_code, poi = poi, limit = limit)
    if(poi):
        pass
    else:
        return False
    items = []
    for one_item in poi:
        title = one_item['address']['label']
        try:
            contact = ("Contact: " + one_item['contacts'][0]['phone'][0]['value'] + " | Website: " + one_item['contacts'][0]['www'][0]['value']) 
            title = (title+'\n'+contact)
            items.append(title)
        except:
            items.append(title)
    if(items):
        return items
    else:
        return False

def _get_transit_from_name(origin, destination):
    try:
        origin_gc = _get_geocode(origin)
        destination_gc = _get_geocode(destination)
        route = _get_transit_from_geocode(origin=origin_gc, destination=destination_gc)
        sections = (route['routes'][0]['sections'])
        directions = []
        for section in sections:
            try:
                mode = section['transport']['mode'].title()
                from_l = section['departure']['place']['name'].title() + " (" + section['departure']['place']['type'].title()+")"
                to_l = section['arrival']['place']['name'].title() + " (" + section['arrival']['place']['type'].title()+")"
            except:
                mode = section['transport']['mode'].title()
                from_l = origin.title() + " ("+ section['departure']['place']['type'].title()+")"
                to_l = destination.title()+ " (" +section['arrival']['place']['type'].title()+")"
            directions.append(mode+'\n'+from_l+ ' to '+to_l)
        return directions
    except:
        # return (route['notices'][0]['title'])
        return False

def _get_routes_from_geocode(origin, destination, transportMode='car'):
    """
    This method takes origin and destination as string of lat,lng as parameter
    and returns list of directions
    """
    routes_url = 'https://router.hereapi.com/v8/routes?apiKey='+apiKey
    routes_location = '&transportMode='+ transportMode+'&origin='+origin+'&destination='+destination
    response = requests.get(routes_url + routes_location)
    if(response.status_code == 200):
        return response.json()
    else:
        return False

def _get_routes_from_name(origin, destination):
    try:
        origin_gc = _get_geocode(origin)
        destination_gc = _get_geocode(destination)
        route = _get_routes_from_geocode(origin=origin_gc, destination=destination_gc)
        sections = (route['routes'][0]['sections'])
        directions = []
        for section in sections:
            try:
                mode = section['transport']['mode'].title()
                from_l =  section['departure']['place']['name'].title() + " | " + section['departure']['place']['type'].title()
                to_l =  section['arrival']['place']['name'].title() + "|" + section['arrival']['place']['type'].title()
            except:
                mode = section['transport']['mode'].title()
                from_l = origin.title() + " ("+ section['departure']['place']['type'].title()+")"
                to_l =  destination.title()+ " (" +section['arrival']['place']['type'].title()+")"
            directions.append(mode+"\n"+from_l+ " to "+to_l)
        return directions
    except:
        # return (route['notices'][0]['title'])
        return False

