import logging
import os
import re 

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
# from twilio.rest import Client

from mindmeld.components import NaturalLanguageProcessor
from mindmeld.components.dialogue import Conversation
from mindmeld import configure_logs

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

        @self.app.route("/", methods=["POST"])
        def handle_message():  # pylint: disable=unused-variable
            incoming_msg = request.values.get('Body', '').lower()
            resp = MessagingResponse()
            msg = resp.message()

            response_text = self.conv.say(incoming_msg)[0]
            def extract_URL(response_text): 
                # defining regular expression to extract url
                regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

                url = re.findall(regex,response_text)       
                return [URL_List[0] for URL_List in url] 

            url_list = extract_URL(response_text)
            extracted_image_url = ""
            for i in range(len(url_list)):
                # print(url_list[i][-3:])
                if url_list[i][-3:] == "png" or url_list[i][-3:] == "jpg":                
                    extracted_image_url = url_list[i]                

            # setting msg body 
            try:            
                for l in url_list:
                    if url_list[i][-3:] == "png" or url_list[i][-3:] == "jpg":
                        response_text = response_text.replace(l,"")      
            except:
                pass
                
            msg.body(response_text)                                       
            # cheking for media availability
            try:
                if extracted_image_url != "":
                    msg.media(extracted_image_url)                
            except:
                msg.body("URL issues")                    
            # returning response ti whatsapp
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