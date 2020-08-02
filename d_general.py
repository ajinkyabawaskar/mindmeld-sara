from .root import app 
import random

@app.handle(intent='greet')
def welcome(request, responder):
    responder.reply("Hi, I am Sara! Your virtual travel assistant. I can help you "
    "find a hotel, check fights or you can tell me what you're intrested in "
    "and I'll recommend you places to visit in India!")

@app.handle(intent='confirm')
def confirm_action(request, responder):
    try:
        if responder.frame.get('expecting_homestay_preference'):
            try:
                responder.frame['expecting_homestay_preference'] = False
                homestays = responder.frame.get('homestays')
                responder.slots['name'] = homestays['name']
                responder.slots['address'] = homestays['address']
                responder.slots['type'] = homestays['type']
                responder.slots['people'] = homestays['people']
                responder.slots['amenities'] = homestays['amenities']
                responder.slots['checkin'] = homestays['checkin']
                responder.slots['checkout'] = homestays['checkout']
                responder.slots['amount'] = homestays['amount']
                responder.slots['contact'] = homestays['contact']
                responder.slots['images'] = ", ".join(homestays['url'])
                responder.reply("Great! {name} has a {type} property that can accomodate"
                                " {people} people, and has {amenities}. It is available between"
                                " {checkin} and {checkout}.\nContact: {contact} Images: {images}. Would you like to book for {amount}?")
                responder.frame['expecting_homestay_confirmation'] = True
            except:
                responder.frame['expecting_homestay_preference'] = True
                responder.reply('Oops! Can you try again?')

        elif responder.frame.get('expecting_homestay_confirmation'):
            try:
                responder.frame['expecting_homestay_confirmation'] = False
                homestay = responder.frame.get('homestays')
                responder.slots['name'] = homestay['name']
                responder.slots['homestay_id'] = homestay['homestay_id']
                try:
                    url = "https://myacademic.space/book-homestay/?apiKey=761b43d33fc96a69e58d0f281eb68742&homestay_id"+homestay['homestay_id']
                    response = requests.get(url)
                    if response.status_code == 200:
                        response = response.json()
                        responder.slots['password'] = response['password']
                except:
                    responder.slots['password'] = 'uyv232bj23nk'
                responder.reply("Your homestay with {name} has been confirmed! Find your password protected invoice here:"
                " https://myacademic.space/invoices?homestay_id={homestay_id}B and password is {password}")
            except:
                responder.frame['expecting_homestay_confirmation'] = True
                responder.reply("Oops! Can you try again?")
    except:
        responder.reply("Confirmed!")

@app.handle(intent='help')
def provide_help(request, responder):
    """
    When the user asks for help, provide some sample queries they can try.
    """
    # Respond with examples demonstrating how the user can order food from different restaurants.
    # For simplicity, we have a fixed set of demonstrative queries here, but they could also be
    # randomly sampled from a pool of example queries each time.
    replies = ["I can help you explore the real India! Try asking me about the best places to visit"]
    responder.reply(replies)

@app.handle(intent='exit')
def say_goodbye(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    # Clear the dialogue frame to start afresh for the next user request.
    # responder.frame = {}
    
    if (responder.frame.get('expecting_homestay_preference') or responder.frame.get('expecting_homestay_confirmation')):
        destination = responder.frame.get('destination')
        responder.slots['destination'] = destination
        try:
            hotels = app.question_answerer.get(index='locations', query_type='text', city=destination)
            try:
                responder.frame['hotels'] = hotels
                responder.slots['hotels'] =", ".join(hotels[0]['hotels'])
                responder.reply("Here are some hotels at {destination}- {hotels}\nWhere would you like to book?")
            except:
                responder.reply("Sorry! Couldn't find hotels at {destination}")
        except:
            responder.reply("I couldn't find ant hotels at {destination}")
        # responder.reply(['Bye!', 'Goodbye!', 'Have a nice day.', 'See you later.'])
    else:
        # Respond with a random selection from one of the canned "goodbye" responses.
        responder.reply(['Bye!', 'Goodbye!', 'Have a nice day.', 'See you later.'])
    
@app.handle(intent='unsupported')
def say_unsupported(request, responder):
    """
    When the user asks an unrelated question, convey the lack of understanding for the requested
    information and prompt to return to food ordering.
    """
    replies = ["Sorry, I can't answer this right away! My creators are still working on this :)"]
    responder.reply(replies)
