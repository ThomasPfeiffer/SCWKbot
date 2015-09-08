# -*- coding: utf-8 -*-
from datetime import datetime
import re
import Entity.User as User


def getOrCreate(senderID, senderFirstName, chat_id):
	user = User.get(senderID)
	if not user:
		user = User.create(senderID, senderFirstName, chat_id)
	return user