from .root import app 
import random

@app.handle(intent='greet')
def welcome(request, responder):
    responder.reply("Hi, I am Sara!")

@app.handle(intent='confirm')
def confirm_action(request, responder):
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
