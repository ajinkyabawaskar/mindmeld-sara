from .root import app 
from .u_here_api import *

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
        source = source + " India"
        destination = destination + " India"
        source_c = _get_lat_lng(source)
        destination_c = _get_lat_lng(destination)
        # try:
            # seeing if we got the ll
            
        responder.slots['a'] = source_c
        responder.slots['b'] = destination_c
        responder.reply('{a}{b}')
    # else
        # responder.reply("API Error!")
    except:
        responder.reply("Source/Destination missing")

@app.handle(intent = 'get_ticket_status')
def send_ticket_status(request, responder):
    responder.reply("You are asking about your ticket")


