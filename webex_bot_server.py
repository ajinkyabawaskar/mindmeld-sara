from mindmeld.components import NaturalLanguageProcessor
from mindmeld.bot import WebexBotServer
from mindmeld import configure_logs
import json
import logging
from ciscosparkapi import CiscoSparkAPI
from flask import Flask, request
import requests

CISCO_API_URL = "https://api.ciscospark.com/v1"
ACCESS_TOKEN_WITH_BEARER = "NTk4N2Q2ZjUtZjkwMi00YzU4LTlmYWItMjJjZWFmZDZmODc4YWZhYzUyYzEtMjdi_PF84_consumer"
BAD_REQUEST_NAME = "BAD REQUEST"
BAD_REQUEST_CODE = 400
APPROVED_REQUEST_NAME = "OK"
APPROVED_REQUEST_CODE = 200

class WebexBotServerException(Exception):
    pass

if __name__ == '__main__':
        self.webhook_id = 'Y2lzY29zcGFyazovL3VzL1dFQkhPT0svYWRhMDI5YzYtNzE3Ni00MTc2LTlmMGUtNDhlN2RiOWI1Mjll'
        self.access_token = 'NGRjZGY1ZDktMTQxZi00OWFkLWI2ZjAtYzg1MDE0ZjFmMjUwOTQxNTQ2MzYtNmY2_PF84_consumer'
        nlp = NaturalLanguageProcessor('.')
        if not nlp:
            self.nlp = NaturalLanguageProcessor(app_path)
            self.nlp.load()
        else:
            self.nlp = nlp
        self.conv = Conversation(nlp=self.nlp, app_path=app_path)

        self.logger = logging.getLogger(__name__)

        if not self.webhook_id:
            raise WebexBotServerException("WEBHOOK_ID not set")
        if not self.access_token:
            raise WebexBotServerException("BOT_ACCESS_TOKEN not set")
        self.spark_api = CiscoSparkAPI(self.access_token)
        self.access_token_with_bearer = ACCESS_TOKEN_WITH_BEARER + self.access_token
        configure_logs()
        

   server = WebexBotServer(name=__name__, app_path='.', nlp=nlp, webhook_id=WEBHOOK_ID, access_token=ACCESS_TOKEN)

        port_number = 8080
        print('Running server on port {}...'.format(port_number))

        server.run(host='localhost', port=port_number)
        