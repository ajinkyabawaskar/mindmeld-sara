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
        responder.slots['seats'] = seats
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
