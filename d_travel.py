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
        source = "not defined"
        responder.slots['source'] = "no source found"
    try:
        destination = destination_entity['value'][0]['cname']
        responder.slots['destination'] = destination
    except:
        destination = "not defined"
        responder.slots['destination'] = "no destination found"
    try:
        seats = no_of_ppl['value'][0]['value']
        responder.slots['seats'] = str(seats)
        responder.frame['seats'] = str(seats)
    except:
        responder.slots['seats'] = "no seats specified"
        responder.frame['seats'] = "no seats specified"
    try:
        departure = departure_entity['value'][0]['value']
        responder.slots['departure'] = departure
        responder.frame['departure'] = departure
    except:
        responder.slots['departure'] = "no departure found"
        responder.frame['departure'] = "no departure found"
    try:
        arrival = arrival_entity['value'][0]['value']
        responder.slots['arrival'] = arrival
        responder.frame['arrival'] = departure
    except:
        responder.slots['arrival'] = "no arrival found"
        responder.frame['arrival'] = "no arrival found"
    try:
        flightclass = flight_class_entity['value'][0]['cname']
        responder.slots['flightclass'] = flightclass
        responder.frame['flightclass'] = departure
    except:
        responder.slots['flightclass'] = "no flightclass found"
        responder.frame['flightclass'] = "no flightclass found"

        # call an api for availability and pricing...
    flight_url = 'https://myacademic.space/flights/?apiKey=761b43d33fc96a69e58d0f281eb68742'
    flight_url = flight_url + '&destination='+destination+'&source='+source
    response = requests.get(flight_url)
    if response.status_code == 200:
        availability = response.json()
        if availability:
            available_flights = availability
            display = ' '
            responder.slots['source_airport'] = available_flights['source']['airport']
            responder.slots['destination_airport'] = available_flights['destination']['airport']
            for a_flight in available_flights['flight']:
                display = display+'\n'+'Departs '+a_flight['departure_time'][12:]+' · '+a_flight['airline']+' · ₹ '+str(a_flight['price'])
            responder.slots['flights'] = display
            responder.reply('Here you go: {source_airport} - {destination_airport}{flights}\nWould you like to know anything else?')
        else:
            responder.reply("There are no flights available at the given location. Please try again with differnt location.")
    else:
        responder.reply("I couldn't check the availability. Please try again after some time.")

    # except:
    #     responder.slots['response'] = "no data found"
        #  source, destination, flight_class, seats, arrival, departure
    # responder.reply("{response}")

