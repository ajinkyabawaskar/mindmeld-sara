from .root import app 

@app.handle(intent='get_india_info')
def send_india_info(request, responder):
    query = request.text
    answers = app.question_answerer.get(index='india', question=query)
    if(len(answers)>0):
        responder.slots['answer'] = answers[0]['answer']
    else:
        responder.slots['answer'] = "I'm sorry, I couldn't find an answer to your question. Can we try rephrasing?"
    responder.reply('{answer}')

@app.handle(intent='get_location_info')
def send_location_info(request, responder):
    for entity in request.entities:
        if(entity['type'] == 'location'):
            queried_location = entity['text']
            responder = _fetch_from_kb(responder, queried_location)
            responder.frame['destination'] = queried_location
            responder.reply("{destination}, {country} is known for its {highlights}")
        else:
            responder.reply("Not sure about your location")
            responder.listen()

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
    
    
    
@app.dialogue_flow(domain='get_info', intent='get_location_info')
def send_location_info1(request, responder):
    active_loc = None
    loc_entity = next((e for e in request.entities if e['type'] == 'location'), None)
    if loc_entity:
        try:
            loc = app.question_answerer.get(index='loc', id=loc_entity['value']['id'])
        except TypeError:
            # failed to resolve entity
            loc = app.question_answerer.get(index='loc', loc_name=loc_entity['text'])
        try:
            active_loc = loc[0]
            responder.frame['target_loc'] = active_loc
        except IndexError:
            # No active store... continue
            pass
    elif 'target_loc' in responder.frame:
        active_loc = responder.frame['target_loc']

    if active_loc:
        responder.slots['loc_name'] = active_loc['loc_name']
        responder.reply('Would you like to stay in {loc_name} hotels')
        return

    #responder.frame['count'] = responder.frame.get('count', 0) + 1

   # if responder.frame['count'] <= 3:
        #responder.reply('Which store would you like to know about?')
       # responder.listen()
    #else:
        #responder.reply('Sorry I cannot help you. Please try again.')
        #responder.exit_flow()

