from .root import app 

@app.handle(intent='get_india_info')
def send_india_info(request, responder):
    query = request.text
    answers = app.question_answerer.get(index='india', query_type='text', question=query, answer = query)
    if answers:
        reply = ['Here is the top result:', answers[0]['question'], answers[0]['answer']]
        responder.reply('\n'.join(reply))
    else:
        responder.reply("I'm sorry, I couldn't find an answer to your question")
    # if(len(answers)>0):
    #     responder.slots['answer'] = answers[0]['answer']
    # else:
    #     responder.slots['answer'] = "I'm sorry, I couldn't find an answer to your question. Can we try rephrasing?"
    # responder.reply('{answer}')
    # responder.reply(request.text)

@app.handle(intent='get_location_info')
def send_location_info(request, responder):
    for entity in request.entities:
        if(entity['type'] == 'location'):
            queried_location = entity['text']
        if(entity['type'] == 'point_of_interest'):
            poi = entity['text']
            # responder = _fetch_from_kb(responder, queried_location)
            # responder.frame['destination'] = queried_location
            # responder.reply("{destination}, {country} is known for its {highlights}")
        else:
            responder.reply()
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