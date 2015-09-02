# -*- coding: utf-8 -*-

import StringIO
import json
import logging
import random
import urllib
import urllib2
import Test.UserTest

# for sending images
from PIL import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

TOKEN = '134894567:AAGupjHqgmPczG3d6iWe6jCjAxWXV06YiL0'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'


# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)

class CurrentUpdate(ndb.Model):
    # key name: str(chat_id)
    updateID = ndb.IntegerProperty()


# ================================

def setCurrentUpdate(chatID, updateID):
    logging.info('Setting current update for ' + str(chatID) + " to " + str(updateID))
    update = CurrentUpdate.get_or_insert(str(chatID))
    update.updateID = updateID
    update.put()

def getCurrentUpdate(chatID):
    update = CurrentUpdate.get_by_id(str(chatID))
    if update:
        return update.updateID
    return -1

def setEnabled(yes):
    es = EnableStatus.get_or_insert(str(1))
    es.enabled = yes
    es.put()

def getEnabled():
    es = EnableStatus.get_by_id(str(1))
    if es:
        return es.enabled
    return False


# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            return

        def reply(msg=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode("utf-8"),
                    'disable_web_page_preview': 'true',
                })).read()
            else:
                logging.error('no msg specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)

        lastUpdate = getCurrentUpdate(chat_id)
        if lastUpdate >= update_id:
            logging.info('Already at update ' + str(lastUpdate))
            return
        else:
            setCurrentUpdate(chat_id, update_id)

        # COMMANDS
        if text.startswith('/'):
            if text == '/start':
                reply('Bot enabled')
                setEnabled(True)
            elif text == '/stop':
                reply('Bot disabled')
                setEnabled(False)
            else:
                reply('What command?')

        # END COMMANDS
        if not getEnabled():
            return

        # CUSTOMIZE FROM HERE
        rep = Test.UserTest.respondTo(message, chat_id)
        if rep:
            reply(rep)


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
