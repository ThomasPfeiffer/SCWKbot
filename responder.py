# -*- coding: utf-8 -*-
from datetime import datetime
import re
import random
import Entity.User as User
import Entity.Event as Event
import Logic.UserController as UserController
import main
from google.appengine.ext import ndb



def respondTo(message, sender):

	message_id = message.get('message_id')
	date = message.get('date')
	text = message.get('text')
	sender = message.get('from')
	senderID = str(sender['id'])
	senderFirstName = sender['first_name']
	chat = message['chat']
	chat_id = str(chat['id'])

	# For dev
	if '/setName' in text:
		split = text.split()
		senderFirstName = split[split.index('/setName')+1]
		del split[split.index('/setName')+1]
		split.remove('/setName')
		text = ' '.join(split)

	if '/setUser' in text:
		split = text.split()
		senderID = split[split.index('/setUser')+1]
		del split[split.index('/setUser')+1]
		split.remove('/setUser')
		text = ' '.join(split)

	user = UserController.createOrUpdate(senderID, senderFirstName, chat_id)
	textLower = text.lower()
	textLowerSplit = textLower.split(' ' , 2)
	command = textLowerSplit[0]
	additional = None
	if len(textLowerSplit) > 1:
		additional = textLowerSplit[1]

	if command.startswith('an'):
		return UserController.registerForEvent(user, additional)

	if command.startswith('ab'):
		return UserController.cancelForEvent(user, additional)

	
	return u'Folgende befehle sind möglich: \n\t an -> anmelden \n\t ab -> abmelden \n\t info -> Informationen zu einem Event \n Zusätzlich kann ein bestimmter Tag (z.B. "Montag") oder ein Datum (TT.MM.JJJJ) angegeben werden.'

