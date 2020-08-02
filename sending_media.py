import os
from twilio.rest import Client

client = Client(os.environ['ACcb01857d9cd7f574f2f89d687d938380'], os.environ['b5594abd6509f5275206d4b284ea30c4'])

# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:+14155238886'
# replace this number with your personal WhatsApp Messaging number
to_whatsapp_number='whatsapp:+919977216617'

message = client.messages.create(body='Check out this owl!',
                       media_url='https://demo.twilio.com/owl.png',
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)

print(message.sid)