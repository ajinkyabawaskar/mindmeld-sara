from .root import app 

@app.handle(intent='by_experiences')
def send_recommendations(request, responder):
    # try to extract entities
    for entity in request.entities:
        if entity['type'] == 'experiences':
            experiences_entity = entity
    try:
        if experiences_entity:
            experiences = experiences_entity['value'][0]['cname']
            responder.frame['experiences'] = experiences
            responder.slots['experiences'] = experiences
            try:
                locations = app.question_answerer.get(index='experiences', query_type='text', experiences=experiences)[0]
                responder.slots['desc'] = locations['description'].split(". ")[0]+"."
                display = ''
                for location in locations['locations']:
                    display = display + '\n'+location['name']+' in '+location['city']+'\nMore: '+location['url']
                responder.slots['display'] = display
                responder.frame['expecting_action_on_ta'] = True
                responder.reply('{desc}{display} Where would you like to visit?')
            except:
                responder.reply('Oops! I know of no locations for {experiences}. 🤧')
        else:
            responder.reply("Oops! Something went wrong. 🥵")
    except:
        responder.reply("There are lots of places worth a visit in India. Try including your interests like shopping, spirituality, yoga, culture or perhaps scuba diving! 🤿")