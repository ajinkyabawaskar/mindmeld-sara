from .root import app 
from mindmeld.core import FormEntity

@app.handle(intent = 'confirm_destination')
def get_destination(request, responder):

    if(responder.frame.get('state') == 'ask_user_for_local_culture'):
        responder.frame['state'] = 'confirm_for_local_culture'
        responder.slots['destination'] = responder.frame.get('destination').title()
        responder.reply("We believe in a culture of Atithi Devo Bhava. "
                        "For you to explore the life in rural India, we've reached out to some"
                        " folks in villages near {destination} who would like to host you."
                        "\nWould you like to stay at their place or hotels?")
        return

    if(responder.frame.get('state')=='confirm_for_local_culture'):
        responder.frame['state'] = 'if_wants_local_stay'
        responder.reply("Cool! Looking for someone to host you in "+responder.frame.get('destination').title())
    
        return
    
    if(responder.frame.get('state')=='if_wants_local_stay'):
        responder.frame['state'] = 'local_accomodation'
        responder.reply("Your accomodation at Ajinkya's place is confirmed at "+responder.frame.get('destination').title())

    else:
        responder.reply("You haven't chose a destination yet. Where would you like to travel?")
    
@app.handle(intent = 'confirm_date')
def set_date(request, responder):

    if((len(request.entities) == 1) and request.entities[0]['type']=='sys_time'):
        responder.slots['when'] = request.entities[0]['value']
    else:
        responder.slots['when'] = "Unable to get date"

    responder.reply("Confirming - {when}")

#slot filling logic requires a form which has your needed entities for the intent
dest_form = {
    "entities": [
        FormEntity(
        #specify the entity custom or system
           entity = 'location',
           role = 'destination',
        #the response to prompt the user with if it is missing in the request
           responses=['Okay, to where?']),
        FormEntity(
           entity="location",
           role="source",
           responses=["Sure, from where?"]),
        FormEntity(
        #specify the entity custom or system
           entity = 'sys_number',
        #    role = 'destination',
        #the response to prompt the user with if it is missing in the request
           responses=['How many people?'])
        ],
     #keys to specify if you want to break out of the slot filling logic
    'exit_keys' : ['cancel', 'restart', 'exit', 'reset', 'no', 'nevermind', 'stop', 'back', 'help', 'stop it', 'go back'
            'new task', 'nothing', 'other', 'return'],
    #a message to prompt the user after exit
    'exit_msg' : 'A few other sara tasks you can try are, booking hotels, checking ticket status',
    #the number of max tries for the user to specify the entity
    'max_retries' : 1
}
#the @app.auto_fill decorator indicates it is a dialogue state handler that requires a form and uses the slot filling logic
@app.auto_fill(intent='plan_route', form = dest_form)
#Control is passed on to this dialogue state handler one the slot-filling process is completed and all required entities in this form have been obtained.
def dest_handler(request, responder):
    for entity in request.entities:
        if entity["type"] == "location":
            if entity["role"] == "source":
                source = entity['text']
                responder.slots['source'] = source
            elif entity["role"] == "destination":
                destination = entity['text']
                responder.slots['destination'] = destination
        elif entity["type"] == 'sys_number':
            responder.slots['people'] = entity['text']

    try:
        responder.slots['directions'] = 'https://www.google.com/maps/dir/'+source+"/"+destination
    except:
        responder.slots['directions'] = 'Coming soon'
    responder.reply("Planning route from {source} to {destination} for {people} people\n {directions}")
# @app.handle(intent = 'plan_route')
# def send_route(request, responder):
    
#     for entity in request.entities:
#         if(entity['type'] == 'location'):
#             if(entity['role'] == 'source'):
#                 source = entity['text']
#             if(entity['role']=='destination'):
#                 destination = entity['text']
#     try:
#         # seeing if source and destination are there in query
#         route = _get_routes_from_name(source, destination)
#         if(route != False):
#             responder.slots['directions'] = "\n".join(route)
#         else:
#             responder.slots['directions'] = 'https://www.google.com/maps/dir/'+source+"/"+destination

#         responder.reply("Here's what I found: \n{directions}")
#     except:
#         responder.reply("Oops! I can't find the locations :(\nCould you try again by including where you are and where you want to go?")

@app.handle(intent = 'get_ticket_status')
def send_ticket_status(request, responder):
    responder.reply("You are asking about your ticket")


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
            directions.append(mode+" - "+from_l+ " to "+to_l)
        return directions
    except:
        # return (route['notices'][0]['title'])
        return False

