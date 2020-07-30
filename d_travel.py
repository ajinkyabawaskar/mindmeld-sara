from .root import app 

@app.handle(intent='get_flights')
def send_flights(request, responder):
    responder.reply("Sending flights!")


@app.handle(intent='get_recommendations')
def send_recommendations(request, responder):
    responder.reply("Recommending..")