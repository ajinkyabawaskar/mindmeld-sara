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
    try:           
        responder.slots['source'] = source_entity
    except:
        responder.slots['source'] = "No Source"
    try:
        responder.slots['destination'] = destination_entity
    except:
        responder.slots['destination'] = "No destination"
    # try:
    #     responder.slots['seats'] = seats
    # try:
    #     responder.slots['departure'] = departure
    source = source_entity['value'][0]['cname']
    destination = destination_entity['value'][0]['cname']
    seats = no_of_ppl['value'][0]['value']
    departure = departure_entity['value'][0]['value']
        # call an api for availability and pricing...
        # url = 'myacademic.space/flights/?apiKey=ykb234v2hg4vmh2gvm242&source='+source
        # url = url + '&destination='+destination+'&flight_class='+flight_class+'
        #  source, destination, flight_class, seats, arrival, departure
    responder.reply("flights from {source} to {destination} for {seats} people departing at {departure}")


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