from mindmeld.components import NaturalLanguageProcessor
from mindmeld.bot import WebexBotServer
from mindmeld import configure_logs
from ..components import NaturalLanguageProcessor
from ..components.dialogue import Conversation
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
   # Create web hook here: https://developer.webex.com/docs/api/v1/webhooks/create-a-webhook
   WEBHOOK_ID = os.environ.get('WEBHOOK_ID')

   # Create bot access token here: https://developer.webex.com/my-apps/new
   ACCESS_TOKEN = os.environ.get('BOT_ACCESS_TOKEN')

   configure_logs()
   nlp = NaturalLanguageProcessor('.')

   server = WebexBotServer(name=__name__, app_path='.', nlp=nlp, webhook_id=WEBHOOK_ID,
                           access_token=ACCESS_TOKEN)

   port_number = 8080
   print('Running server on port {}...'.format(port_number))

   server.run(host='localhost', port=port_number)