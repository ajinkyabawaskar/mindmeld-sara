import os
from twilio.rest import Client

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])

# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:+14155238886'
# replace this number with your personal WhatsApp Messaging number
to_whatsapp_number='whatsapp:+919977216617'

message = client.messages.create(body='Check out this owl!',
                       media_url='https://demo.twilio.com/owl.png',
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)

print(message.sid)