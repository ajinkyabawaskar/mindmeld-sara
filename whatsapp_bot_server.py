import logging
import os
import re 

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
# from twilio.rest import Client

from mindmeld.components import NaturalLanguageProcessor
from mindmeld.components.dialogue import Conversation
from mindmeld import configure_logs

# client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
class WhatsappBotServer:
    """
    A sample server class for Whatsapp integration with any MindMeld application
    """

    def __init__(self, name, app_path, nlp=None):
        """
        Args:
            name (str): The name of the server.
            app_path (str): The path of the MindMeld application.
            nlp (NaturalLanguageProcessor): MindMeld NLP component, will try to load from app path
              if None.
        """
        self.app = Flask(name)
        if not nlp:
            self.nlp = NaturalLanguageProcessor(app_path)
            self.nlp.load()
        else:
            self.nlp = nlp
        self.conv = Conversation(nlp=self.nlp, app_path=app_path)
        self.logger = logging.getLogger(__name__)

        # if not client:
        #     self.client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
        # else:
        #     self.client = client


        @self.app.route("/", methods=["POST"])
        def handle_message():  # pylint: disable=unused-variable
            incoming_msg = request.values.get('Body', '').lower()
            resp = MessagingResponse()
            msg = resp.message()

            # doing just to skip training dataset later remove and just implement on response_text functionality
            # if incoming_msg == "test media":
            #     # creating rest client instance
            #     try:
            #         # this is the Twilio sandbox testing number
            #         from_whatsapp_number='whatsapp:+14155238886'
            #         # replace this number with your personal WhatsApp Messaging number
            #         to_whatsapp_number='whatsapp:+919977216617'
            #         # the below image_url will be extracted from responnse_text
            #         image_url = 'https://cdn.pixabay.com/photo/2015/03/15/11/34/house-674244_960_720.jpg'

            #         try:
            #             message = client.messages.create(body='check out this beautiful penthouse',
            #                     media_url= image_url,
            #                     from_=from_whatsapp_number,
            #                     to=to_whatsapp_number)
            #         except:
            #             msg.body("msg me dikkat hai kuch toh!")                            
            #             return str(resp)                     

            #         msg.body("did everything but no reply")                            
            #         msg.media("https://pbs.twimg.com/profile_images/1274045729170808833/2vT239Ac_400x400.jpg")
            #         return str(resp)                                                           
            #     except:
            #         msg.body("We understood test media but error aa gaya")                    
            #         return str(resp)
            # else:
            # getting 
            response_text = self.conv.say(incoming_msg)[0]
            def extract_URL(response_text): 
                # defining regular expression to extract url
                regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

                url = re.findall(regex,response_text)       
                return [URL_List[0] for URL_List in url] 

            url_list = extract_URL(response_text)
            for i in range(len(url_list)):
                # print(url_list[i][-3:])
                if url_list[i][-3:] == "png" or url_list[i][-3:] == "jpg":
                    extracted_image_url = url_list[i]
            
            msg.body(response_text) 
            msg.media(extracted_image_url)
            return str(resp)

    def run(self, host="localhost", port=7150):
        self.app.run(host=host, port=port)


if __name__ == '__main__':
    app = Flask(__name__)
    configure_logs()
    server = WhatsappBotServer(name='whatsapp', app_path='.')
    port_number = 8080
    print('Running server on port {}...'.format(port_number))
    server.run(host='localhost', port=port_number)