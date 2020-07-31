from .root import app 

# @app.auto_fill(FormEntity flightEntity)
@app.handle(intent='get_flights')
def send_flights(request, responder):
    for entity in request.entities:
        if entity['type'] == 'location':
            if entity['role'] == 'source':
                source_entity = entity
            if entity['role'] == 'destination':
                destination_entity = entity

        if entity['type'] == 'flight_class':
            flight_class_entity = entity

        if entity['type'] == 'sys_number':
            no_of_ppl = entity

        if entity['type'] == 'sys_time':
            if entity['role'] == 'arrival':
                arrival_entity = entity
            if entity['role'] == 'departure':
                departure_entity = entity
    source = source_entity['value'][0]['cname']
    destination = destination_entity['value'][0]['cname']
    seats = no_of_ppl['value'][0]['value']
    arrival = arrival_entity['value'][0]['value']
    
    responder.slots['source'] = source
    responder.slots['destination'] = destination
    responder.slots['seats'] = seats 
    responder.slots['arrival'] = arrival
        # call an api for availability and pricing...
        # url = 'myacademic.space/flights/?apiKey=ykb234v2hg4vmh2gvm242&source='+source
        # url = url + '&destination='+destination+'&flight_class='+flight_class+'
        #  source, destination, flight_class, seats, arrival, departure
    responder.reply("flights from {source} to {destination} for {seats} people arriving at {arrival}")


@app.handle(intent='get_recommendations')
def send_recommendations(request, responder):
    for entity in request.entities:
        if entity['type'] == 'experiences':
            experience = entity
    try:
        responder.slots['exp'] = experience
        responder.reply('{exp}')
    except:
        responder.reply("Recommending..")