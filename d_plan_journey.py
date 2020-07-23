from .root import app 

@app.handle(intent = 'confirm_destination')
def get_destination(request, responder):
    state = responder.frame.get('destination')
    # if(state == "DESTINATION_CONFIRMED"):
    #     responder.slots['destination'] = responder.frame.get('destination')
    #     responder.reply("Hurrah! Your travel to {destination}, India is planned!")
    # else:       
    #     responder.reply("Please select a destination first!")
    responder.reply("Confirm "+ str(state))

@app.handle(intent = 'confirm_date')
def set_destination(request, responder):
    # state = responder.frame.get('destination')
    # responder.reply("SET "+ str(state))
    for entity in request.entities:
        if(entity['type'] == 'sys_time'):
    #         responder.frame['destination'] = entity['text']
    #         responder.frame['state'] = "DESTINATION_CONFIRMED"
            when = entity['text']
    try:
        responder.slots['when'] = when
        responder.reply("Planning journey on {when}!")
    except NameError:
        responder.reply("CAn not get when")  
    #     else:
    #         responder.frame['state'] = "INITIALISED"
    #         responder.reply("City not identified.")

@app.handle(intent = 'plan_route')
def send_route(request, responder):
    when = ""
    for entity in request.entities:
        if(entity['type'] == 'location'):
            if(entity['role'] == 'source'):
                source = entity['text']
            if(entity['role']=='destination'):
                destination = entity['text']
    try:
        responder.slots['source'] = source
        responder.slots['destination'] = destination
        responder.reply("Planning route from {source} to {destination}")
    except NameError:
        responder.reply("CAn not get route")  
