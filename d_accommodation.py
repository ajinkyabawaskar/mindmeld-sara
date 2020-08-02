from .root import app
from mindmeld.core import FormEntity
import requests

hotel_form = {
    "entities": [
        # FormEntity(
        #    entity = 'location',
        #    responses=['Where will you be visiting?']),
        FormEntity(
           entity="hotel",
           responses=["Where would you like to book?"]),
        FormEntity(
           entity="room_type",
           responses=["Sure. What kind of rooms are you looking for? Like single room, suite, studio or villa"]),
        FormEntity(
           entity="sys_number",
           role="room_count",
           responses=["Cool. How many rooms do you want to book?"]),
        FormEntity(
           entity="sys_number",
           role="headcount",
           responses=["Awesome. How many people?"]),
        FormEntity(
           entity="sys_time",
           role="checkin",
           responses=["Okay. When will you be checking in the hotel?"]),
        FormEntity(
           entity = 'sys_time',
           role = 'checkout',
           responses=['And when will you be checking out?'])
        ],
     #keys to specify if you want to break out of the slot filling logic
    'exit_keys' : ['cancel', 'restart', 'exit', 'reset', 'no', 'nevermind', 'stop', 'back', 'help', 'stop it', 'go back'
            'new task', 'nothing', 'other', 'return'],
    #a message to prompt the user after exit
    'exit_msg' : 'A few other sara tasks you can try are, booking hotels, checking ticket status',
    #the number of max tries for the user to specify the entity
    'max_retries' : 2
}

@app.handle(intent='get_hotels')
def get_hotels(request, responder):
    for entity in request.entities:
        if entity['type'] == 'location':
            location_entity = entity
        if entity['type']  == 'homestay_filters':
            homestay_entity = entity
        # partial entities
        # frame
    try:
        responder.slots['filter'] = ' '+homestay_entity['value'][0]['cname']+' '
        responder.frame['filter'] = ' '+homestay_entity['value'][0]['cname']+' '
    except:
        responder.slots['filter'] = ' '
        responder.frame['filter'] = ' '
    try:
        if len(location_entity['value'])>0:   
            location = location_entity['value'][0]['cname']
            responder.frame['destination'] = location
            responder.slots['destination'] = location
            homestays_url = 'https://myacademic.space/homestays/?apiKey=761b43d33fc96a69e58d0f281eb68742&location='+location
            response = requests.get(homestays_url)
            if(response.status_code == 200):
                homestays = response.json()
                if homestays['status']:
                    responder.frame['homestays'] = homestays['response'][0]
                    responder.frame['homestays'] = homestays['response'][0]
                    responder.reply('Cool. We have partnered with some folks from {destination} who would like to host tourists like you so you get the closest local experience. Would you like to know more?')
                    responder.frame['expecting_homestay_preference'] = True
                    # request.allowed_intents=['confirm','exit']
                else:
                    hotels = app.question_answerer.get(index='locations', query_type='text', city=location)
                    try:
                        responder.frame['hotels'] = hotels
                        responder.slots['hotels'] =", ".join(hotels[0]['hotels'])
                        responder.reply("Here are some{filter}hotels at {destination}- {hotels}\nWhere would you like to book?")
                        # request.target_dialogue_state = 'get_availability'
                    except:
                        responder.reply("Sorry! Couldn't find hotels at {destination}")
            else:
                hotels = app.question_answerer.get(index='locations', query_type='text', city=location)
                try:
                    responder.frame['hotels'] = hotels
                    responder.slots['hotels'] =", ".join(hotels[0]['hotels'])
                    responder.reply("Here are some{filter}hotels at {destination}- {hotels}\nWhere would you like to book?")
                    # request.target_dialogue_state = 'get_availability'
                except:
                    responder.reply("Sorry! Couldn't find hotels at {destination}")
        else:
            responder.reply("Couln't get that location. Maybe try a nearby city?")
    except:
        responder.reply('Sure. Where would you like to look for hotels?')
                
@app.auto_fill(intent='get_hotels', form = hotel_form, has_entity='hotel')
def get_availability(request, responder):
    for entity in request.entities:
        
        if entity['type'] == 'room_type':
            room_type_entity = entity
        if entity['type'] == 'sys_number' and entity['role'] == 'headcount':
            no_of_ppl = entity
        if entity['type'] == 'sys_number' and entity['role'] == 'room_count':
            no_of_rooms = entity
        if entity['type'] == 'hotel':
            hotel_name_entity = entity
        if entity['type'] == 'sys_time' and entity['role'] == 'checkin':
            checkin_entity_role = entity
        if entity['type'] == 'sys_time' and entity['role'] == 'checkout':
            checkout_entity_role = entity

    try:
        hotel_name = hotel_name_entity['value'][0]['cname']
        room_type = room_type_entity['value'][0]['cname']
        try:
            rooms = no_of_rooms['value'][0]['value']
        except:
            rooms = 1
        try:
            headcount = no_of_ppl['value'][0]['value']
        except:
            headcount = 1
        try:
            checkin = checkin_entity_role['value'][0]['value']
        except:
            from datetime import datetime
            date = datetime.now().isoformat()
            checkin = str(date)
        try:
            checkout = checkout_entity_role['value'][0]['value']
        except:
            from datetime import datetime
            date = datetime.now().isoformat()
            checkout = str(date)
        try:
            hotel = app.question_answerer.get(index='hotels', query_type='text', title=hotel_name)[0]
            location = hotel['address']['label']
        except:
            location = "India"

        responder.slots['location'] = location
        responder.slots['room_type'] = room_type
        responder.slots['rooms'] = rooms
        responder.slots['headcount'] = headcount
        responder.slots['hotel_name'] = hotel_name
        responder.slots['checkin'] = checkin
        responder.slots['checkout'] = checkout

        url1 = 'https://myacademic.space/availability/?apiKey=761b43d33fc96a69e58d0f281eb68742'
        url2 = '&location='+location+'&hotel='+hotel_name+'&type='+room_type+'&people='+str(headcount)
        url3 = '&checkin='+checkin+'&checkout='+checkout
        availability_url = url1+url2+url3

        response = requests.get(availability_url)
        if response.status_code == 200:
            availability = response.json()['status']
            if availability:
                available_rooms = response.json()['response']
                display = ''
                for a_room in available_rooms:
                    display= display+'\n'+str(a_room['available'])+ ' ' +a_room['room_type']+'s for ₹ '+str(a_room['amount'])+ ' each'
                responder.slots['available_rooms'] = display
                responder.reply('Sure. {hotel_name} has {available_rooms}\nWould you like to know anything else?')
            else:
                responder.reply("I couldn't proceed with your booking. Please try again with differnt hotel")
        else:
            responder.reply("I couldn't fetch availability. Try again later!")
    except:
        responder.reply('Something went wrong while fetching availability. Try again.')

@app.handle(intent='get_hotels', has_entity='tourist_attraction')
def hotels_near_ta(request, responder):
    for entity in request.entities:
        if entity['type'] == 'tourist_attraction':
            tattraction = entity['value'][0]['cname']
    location = app.question_answerer.get(index='tourist-attractions', query_type="text", name=tattraction)[0]
    responder.slots['tatt'] = tattraction
    responder.slots['url'] = location['url']
    location_name = location['city']
    responder.slots['location_name'] = location_name
    hotels = app.question_answerer.get(index='locations', query_type='text', city=location_name)
    try:
        try:
            responder.frame['hotels'] = hotels
            responder.slots['hotels'] =", ".join(hotels[0]['hotels'])
            responder.reply('Read more about {tatt}\n')
            responder.reply("Here are some hotels near {tatt} in {location_name}- {hotels}\nWhere would you like to book?")
            # request.target_dialogue_state = 'get_availability'
        except:
            responder.reply("Sorry! Couldn't find hotels at {location_name}")
    except:
        responder.reply("I am not aware of that tourit attraction yet, maybe try with name of the city?")
