# -*- coding: utf-8 -*-

import Entity.User

def respondTo(message, chat_id):

	message_id = message.get('message_id')
	date = message.get('date')
	text = message.get('text')
	sender = message.get('from')
	senderID = str(sender['id'])
	senderFirstName = sender['first_name']
	chat = message['chat']
	chat_id = str(chat['id'])

	if "an" in text:
		user = Entity.User.create(senderID, senderFirstName, chat_id)
		return "Benutzer erstellt: " + user.toString()
	if "del" in text:
		return "Gelöscht:" + senderID
	user = Entity.User.getUser(senderID)
	return "Hallo " + user.toString()