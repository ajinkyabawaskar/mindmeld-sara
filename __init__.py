# -*- coding: utf-8 -*-
"""This module contains a template MindMeld application"""
from sara.root import app
# import modules containing dialogue handlers
import sara.d_general
import sara.d_travel
import sara.d_accommodation
import sara.d_recommendation

__all__ = ['app']

@app.handle(default=True)
def default(request, responder):
    """
    This is a default handler.
    """
    replies = ["Could you please be more clear?",
    "Didn't get you there, maybe say it a bit differently?"]
    responder.reply(replies)
