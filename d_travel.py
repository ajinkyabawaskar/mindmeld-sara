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


# @app.handle(intent='get_recommendations')
# def send_recommendations(request, responder):
    # try:
            
    #     for entity in request.entities:
    #         if entity['type'] == 'experiences':
    #             experience = entity
    #         if entity['type'] == 'tourist_attractions':
    #             tourist_attractions = entity
    #     try:
    #         responder.slots['exp'] = experience
    #     except:
    #         responder.slots['exp'] = "No EXP"
    #     try:
    #         responder.slots['ta'] = tourist_attractions
    #     except:
    #         responder.slots['ta'] = "No TA"
        
    #     responder.reply('{exp}\n{ta}')
    # except:
    #     responder.reply("Recommending..")

@app.handle(intent='get_recommendations')
def send_recommendations(request, responder):
    try:    
        for entity in request.entities:
            if entity['type'] == 'experiences':
                experiences_entity = entity
                try:
                    responder.slots['experiences'] = experiences_entity
                except:
                    responder.slots['experiences'] = "No Experiences"

                try:
            	     if len(experiences_entity['value'])>0:   
                        experiences = experiences_entity['value'][0]['cname']
                        responder.frame['experiences'] = experiences
                        responder.slots['experiences'] = experiences
                        experiences = app.question_answerer.get(index='experiences', query_type='text', experiences=experiences)
                        try:
                            responder.frame['experiences'] = experiences
                            responder.slots['descriptions'] =experiences[0]['description']
                            try:
                                city = experiences[0]['location']
                                responder.slots['cities'] = city[0]['city']
                                responder.reply("{descriptions}, {cities} you can visit")
                            except:
                                responder.reply("{descriptions}")
                        except:
                            responder.reply("error fetching experiences from knowledgebase")
                except:
                    responder.reply("No descriptiom found")
            elif entity['type'] == 'tourist_attractions':
                tourist_attractions = entity
                try:
                    responder.slots['tourist_attractions'] = tourist_attractions
                except:
                    responder.slots['tourist_attractions'] = "No Tourist Attractions"
                try:
            	     if len(tourist_attractions['value'])>0:   
                        tourist_attractions = tourist_attractions['value'][0]['cname']
                        responder.frame['tourist_attractions'] = tourist_attractions
                        responder.slots['tourist_attractions'] = tourist_attractions
                        tourist_attractions = app.question_answerer.get(index='tourist_attractions', query_type='text', name=tourist_attractions)
                        try:
                            responder.frame['tourist_attractions'] = tourist_attractions
                            responder.slots['citiess'] =tourist_attractions[0]['city']    
                            responder.reply("{cities} you can visit")
                        except:
                            responder.reply("cities not found")
                except:
                    responder.reply("tourist attraction is not found, please try again")
                                                                                        
    except:
        responder.reply("please try later") 