from .root import app 
# from .utilities.u_here_api import _get_poi_from_name

@app.handle(intent='get_india_info')
def send_india_info(request, responder):
    try:
        query = request.text
        answers = app.question_answerer.get(index='india', query_type='text', question=query, answer = query)
        if answers:
            reply = ['Here is the top result:', answers[0]['question'], answers[0]['answer']]
            responder.reply('\n'.join(reply))
        else:
            responder.reply("I'm sorry, I couldn't find an answer to your question")
    except:
            responder.reply("I'm sorry, I couldn't find an answer to your question")

    # if(len(answers)>0):
    #     responder.slots['answer'] = answers[0]['answer']
    # else:
    #     responder.slots['answer'] = "I'm sorry, I couldn't find an answer to your question. Can we try rephrasing?"
    # responder.reply('{answer}')
    # responder.reply(request.text)

@app.handle(intent='get_location_info')
def send_location_info(request, responder):
    origin = ''
    poi = ''
    points_of_interest = False
    
    # extract entities from query
    for entity in request.entities:
        if(entity['type'] == 'location'):
            origin = entity['text']
        if(entity['type'] == 'point_of_interest'):
            poi = entity['text']
    
    # get data according to entities present
    if(origin!='' and poi !=''):
        # with both location and point of interest
        points_of_interest = _get_poi_from_name(origin=origin, poi=poi)
        if(points_of_interest != False):    
            responder.slots['poi'] = "\n".join(points_of_interest)
            responder.reply(poi.title()+" in "+origin.title()+":\n"+"{poi}")
        else:
            responder.reply("Whoopsie! Couldn't find it in that location! Maybe try again with another? ;)")

    elif(origin!='' and poi ==''):
        responder.frame['state'] = 'ask_user_for_local_culture'
        responder.frame['destination'] = origin
        responder.slots['destination'] = origin.title()
        # only with location but no poi
        points_of_interest = _get_poi_from_name(origin=origin, limit='1')
        if(points_of_interest != False):    
            response_poi = "\n".join(points_of_interest)
            response_poi = response_poi.split("\n")
            response_poi = response_poi[0][:-13]
            responder.slots['poi'] = response_poi
            # responder.reply("Sorry! I couldn't find that. I found in "+origin.title()+":\n"+"{poi}")
        else:
            pass
            # responder.reply("Whoopsie! Couldn't find the location! Maybe try again with another? ;)")
        responder.reply('Great! Planning travel to {destination}.'
                        ' Tourists coming here often visit {poi}\n'
                        'Would you like to know how to experience the local culture there?')
    
    else:
        responder.reply("Whoopsie! Couldn't find the location! Maybe try again with another? ;)")

def _fetch_from_kb(responder, location):
    """
    This function is used the fetch a particular information about the given location
    from the knowledge base.
    """
    locations = app.question_answerer.get(index='locations', destination=location)
    info = locations[0]

    responder.slots['destination'] = location
    responder.slots['country'] = info['country']
    responder.slots['highlights'] = info['highlights'][0].capitalize() + ", "+ info['highlights'][1].capitalize() + " and "+ info['highlights'][2].capitalize() +"."
    return responder

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
    try:
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
    except:
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

