from .root import app 
import random

@app.handle(intent='greet')
def welcome(request, responder):
    responder.frame['state'] = "get_destination_or_preferences"
    welcomes = random.choice(["Hi!", "Hello!", "Hey There!", "Yo!", "Namaste!", "Namaskar!"])
    # can_ask = random.choice(["more about some places to visit.", "about food and cuisine.", "directions.", "about the best places to visit"])
    can_ask = " You can tell me where you want to go or what you want to experience, and I'll find something for you!"
    prefix = " I am Sara, your virtual travel assistant! I'm here to help you plan your next visit to India."
    responder.reply(welcomes+prefix+can_ask)

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

@app.handle(intent='start_over')
def start_over(request, responder):
    """
    When the user wants to start over, clear the dialogue frame and reply for the next request.
    """
    # Clear the dialogue frame and respond with a variation of the welcome message.
    responder.frame = {}
    replies = ["Ok, let's start over!"]
    responder.reply(replies)
    responder.listen()

@app.handle(intent='exit')
def say_goodbye(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}

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