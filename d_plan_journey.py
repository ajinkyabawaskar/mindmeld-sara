from .root import app 
from .utilities.u_here_api import _get_transit_from_name

@app.handle(intent = 'confirm_destination')
def get_destination(request, responder):
    if(responder.frame.get('destination')):
        responder.reply("Would you like to know how to get there?")
    else:
        responder.reply("You haven't chose a destination yet. ")

@app.handle(intent = 'confirm_date')
def set_destination(request, responder):

    if((len(request.entities) == 1) and request.entities[0]['type']=='sys_time'):
        responder.slots['when'] = request.entities[0]['text']
    else:
        responder.slots['when'] = "Unable to get date"

    responder.reply("Confirming - {when}")

@app.handle(intent = 'plan_route')
def send_route(request, responder):
    
    for entity in request.entities:
        if(entity['type'] == 'location'):
            if(entity['role'] == 'source'):
                source = entity['text']
            if(entity['role']=='destination'):
                destination = entity['text']
    try:
        # seeing if source and destination are there in query
        route = _get_transit_from_name(source, destination)
        if(route != False):
            responder.slots['directions'] = "\n".join(route)
        else:
            responder.slots['directions'] = 'https://www.google.com/maps/dir/'+source+"/"+destination

        responder.reply("Here's what I found: \n{directions}")
    except:
        responder.reply("Oops! I can't find the locations :(\nCould you try again by including where you are and where you want to go?")

@app.handle(intent = 'get_ticket_status')
def send_ticket_status(request, responder):
    responder.reply("You are asking about your ticket")
