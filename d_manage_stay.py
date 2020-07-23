from .root import app 

@app.handle(intent='get_accomodation')
def send_accomodation(request, responder):
    at_location = ""
    for e in request.entities:
        if(e['type']=='location'):
            at_location = e['text']
            responder.frame['target_destination'] = at_location
            
            import requests, json
            get_hotels_query = "https://careers.growpartner.in/hotels.php?location=" + at_location
            get_hotels = requests.get(get_hotels_query)
            hotels = get_hotels.json()
    try:
        responder.reply("I found 3 hotels " + hotels["1"] + ", "+ hotels["2"] + ", "+ hotels["3"] +".")
    except UnboundLocalError:
        responder.reply("COuldn't find hotels")

@app.handle(intent='send_notification')
def notify_user(request, responder):
    hotels = {"name": "Bhakt Niwas", "Person" : "3"}
    responder.frame['hotels'] = hotels
    responder.slots['details']  = responder.frame['hotels']
    responder.reply("Notification:  {details}")