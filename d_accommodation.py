from .root import app 

@app.handle(intent='get_hotels')
def send_hotels(request, responder):
    for entity in request.entities:
        if entity['type'] == 'location':
            location_entity = entity
        if entity['type'] == 'room_type':
            room_type_entity = entity
        if entity['type'] == 'sys_number':
            no_of_ppl = entity
        if entity['type'] == 'hotel':
            hotel_name_entity = entity
        if entity['type'] == 'sys_time' and entity['role'] == 'checkin':
            checkin_entity_role = entity
        if entity['type'] == 'sys_time' and entity['role'] == 'checkout':
            checkout_entity_role = entity
    """
    Getting hotels from location name
    """
    # try:
    #     if len(location_entity['value'])>0:
    #         location = location_entity['value'][0]['cname']
    #         hotels = app.question_answerer.get(index='locations', query_type='text', city=location)
    #         try:
    #             responder.slots['location'] =", ".join(hotels[0]['hotels'])
    #         except:
    #             responder.slots['location'] = " found but no hotel"
    # except:
    #     responder.slots['location'] = "No Location"
    try:
        responder.slots['location'] = location_entity['value'][0]['cname']
    except:
        responder.slots['location'] = "No location"
    try:
        responder.slots['room_type'] = room_type_entity['value'][0]['cname']
    except:
        responder.slots['room_type'] = "No Room Type"
    
    try:
        responder.slots['no_of_ppl'] = no_of_ppl['value'][0]['value']
    except:
        responder.slots['no_of_ppl'] = "No headcount"

    try:
        responder.slots['hotel_name_entity'] = hotel_name_entity['value'][0]['cname']
    except:
        responder.slots['hotel_name_entity'] = "No Hotel name"
    
    try:
        responder.slots['checkin_entity_role'] = checkin_entity_role['value'][0]['value']
    except:
        responder.slots['checkin_entity_role'] = "No checkin"
    
    try:
        responder.slots['checkout_entity_role'] = checkout_entity_role['value'][0]['value']
    except:
        responder.slots['checkout_entity_role'] = "No checkout"

    responder.reply("Location - {location}\n"
                    "room_type - {room_type}\n"
                    "no_of_ppl - {no_of_ppl}\n"
                    "hotel_name_entity - {hotel_name_entity}\n"
                    "checkin_entity_role - {checkin_entity_role}\n"
                    "checkout_entity_role - {checkout_entity_role}")

