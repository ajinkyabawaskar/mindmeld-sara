from .root import app 
from mindmeld.core import FormEntity
import requests

flight_form = {
    "entities": [
        # FormEntity(
        #    entity = 'location',
        #    responses=['Where will you be visiting?']),
        FormEntity(
           entity="location",
           role = 'source',
           responses=["Where will you be boarding from?"]),
        FormEntity(
           entity="location",
           role = 'destination',
           responses=["Awesome! Where will you be landing?"]),
        FormEntity(
           entity="sys_number",
           responses=["Cool. How many seats do you want to book?"]),
        FormEntity(
           entity = 'flight_class',
           responses=['By which class would you like to fly?']),
        FormEntity(
           entity="sys_time",
           role="arrival",
           responses=["Okay. By when would you like to reach?"]),
        FormEntity(
           entity = 'sys_time',
           role = 'departure',
           responses=['And when will you be departing?'])
        ],
     #keys to specify if you want to break out of the slot filling logic
    'exit_keys' : ['cancel', 'restart', 'exit', 'reset', 'no', 'nevermind', 'stop', 'back', 'help', 'stop it', 'go back'
            'new task', 'nothing', 'other', 'return'],
    #a message to prompt the user after exit
    'exit_msg' : 'A few other sara tasks you can try are, booking hotels, checking ticket status',
    #the number of max tries for the user to specify the entity
    'max_retries' : 2
}
# @app.handle(intent='get_flights')
@app.auto_fill(intent='get_flights',form=flight_form)
def send_flights(request, responder):
    for entity in request.entities:
        if entity['type'] == 'location' and entity['role'] == 'source':
            source_entity = entity
        if entity['type'] == 'location' and entity['role'] == 'destination':
            destination_entity = entity

        if entity['type'] == 'flight_class':
            flight_class_entity = entity

        if entity['type'] == 'sys_number':
            no_of_ppl = entity

        if entity['type'] == 'sys_time' and entity['role'] == 'arrival':
            arrival_entity = entity
        if entity['type'] == 'sys_time'and entity['role'] == 'departure':
            departure_entity = entity
            
    try:
        source = source_entity['value'][0]['cname']
        responder.slots['source'] = source
    except:
        responder.slots['source'] = "no source found"
    try:
        destination = destination_entity['value'][0]['cname']
        responder.slots['destination'] = destination
    except:
        responder.slots['destination'] = "no destination found"
    try:
        seats = no_of_ppl['value'][0]['value']
        responder.slots['seats'] = str(seats)
    except:
        responder.slots['seats'] = "no seats specified"
    try:
        departure = departure_entity['value'][0]['value']
        responder.slots['departure'] = departure
    except:
        responder.slots['departure'] = "no departure found"
    try:
        arrival = arrival_entity['value'][0]['value']
        responder.slots['arrival'] = arrival
    except:
        responder.slots['arrival'] = "no arrival found"
    try:
        flightclass = flight_class_entity['value'][0]['cname']
        responder.slots['flightclass'] = flightclass
    except:
        responder.slots['flightclass'] = "no flightclass found"

        # call an api for availability and pricing...
        # url = 'myacademic.space/flights/?apiKey=ykb234v2hg4vmh2gvm242&source='+source
        # url = url + '&destination='+destination+'&flight_class='+flight_class+'
        #  source, destination, flight_class, seats, arrival, departure
    responder.reply("flights from {source} to {destination} for {seats} people arriving on {arrival} and departing on {departure} by {flightclass}")


@app.handle(intent='get_recommendations')
def send_recommendations(request, responder):
    try:
            
        for entity in request.entities:
            if entity['type'] == 'experiences':
                experience = entity
            if entity['type'] == 'tourist_attractions':
                tourist_attractions = entity
        try:
            responder.slots['exp'] = experience
        except:
            responder.slots['exp'] = "No EXP"
        try:
            responder.slots['ta'] = tourist_attractions
        except:
            responder.slots['ta'] = "No TA"
        
        responder.reply('{exp}\n{ta}')
    except:
        responder.reply("Recommending..")
