from .root import app 

@app.handle(intent='get_hotels')
def send_flights(request, responder):
    responder.reply("Sending hotels!")

