from .root import app 

@app.handle(intent='get_accomodation')
def send_accomodation(request, responder):
    at_location = ""
    for e in request.entities:
        if(e['type']=='location'):
            at_location = e['text']
            responder.frame['target_destination'] = at_location
            

@app.handle(intent='send_notification')
def notify_user(request, responder):
    hotels = {"name": "Bhakt Niwas", "Person" : "3"}
    responder.frame['hotels'] = hotels
    responder.slots['details']  = responder.frame['hotels']
    responder.reply("Notification:  {details}")