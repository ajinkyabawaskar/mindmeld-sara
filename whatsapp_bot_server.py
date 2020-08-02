import logging

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

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
            # creating rest client instance 
            client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
            msg = resp.message()
            response_text = self.conv.say(incoming_msg)[0]
            image_url = 'https://pbs.twimg.com/profile_images/1274045729170808833/2vT239Ac_400x400.jpg'
            msg.body(response_text)
            msg.media_url(image_url)  
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