#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import sys
#
# sys.path.insert(0, '../')

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api

# my classes
from NO_GIT import advanced_data
import Datetime
import User
from Utils import Util
import Messages
import Connector

# <CONFIG>
token = advanced_data.token
vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
poll = VkBotLongPoll(vk_session, 188541150)
# </CONFIG>

# My vars
dict_of_users = dict()
invite_msg = ''
# My vars

# main
for event in poll.listen():
    # clear list
    User.clearList(dict_of_users)
    if event.type == VkBotEventType.MESSAGE_NEW:
        # return json (event)
        print('EVENT:: ', event)
        # FOR MESSAGES FROM CHAT

        # if it's chat (peer_id != from_id) and it's a message( not invite or kick)
        if event.object.message['peer_id'] != event.object.message['from_id'] and event.object.message['text'] != '':
            # --------------------------Variables--------------------------------------------------
            chat_id = event.object.message['peer_id']  # chat id
            message_id = event.object.message['conversation_message_id']  # message , to write last user msg in DB
            from_id = event.object.message['from_id']  # who send message (user)
            message = event.object.message['text']  # message text
            user_id = event.object.message['from_id'] # sender id

            msg_symbol = message[0]  # if command-symbol (!)
            msg_command = message[1:]  # command body ( without !)


            # --------------------------Variables--------------------------------------------------
            Messages.increment_msg_amount(chat_id, user_id)

            if msg_symbol == '$':
                if msg_command == 'commands':
                    Util.all_commands(session_api, chat_id)
                # User management
                elif msg_command == 'members':
                    Util.dict_iterator_and_send(dict_of_users, session_api, chat_id, event)
                elif msg_command[0:8] == 'kickfrom':
                    User.kickfrom_user(session_api, chat_id, msg_command)
                elif msg_command[0:4] == 'kick':
                    User.remove_user(event, session_api, chat_id, msg_command, dict_of_users)
                elif msg_command[0:4] == 'warn':
                    User.warn_user(event, session_api, chat_id, msg_command, dict_of_users)
                elif msg_command[0:6] == 'unwarn':
                    User.unwarn_user(event, session_api, chat_id, msg_command, dict_of_users)
                # /User management
                # Statistic
                elif msg_command[0:5] == 'state':
                    User.get_state(event, session_api, chat_id, msg_command, dict_of_users)
                # /Statistic
                # Time
                elif msg_command == 'time':
                    Messages.send_message(session_api, chat_id, Datetime.time_now())
                elif msg_command == 'date':
                    Messages.send_message(session_api, chat_id, Datetime.date_now())
                elif msg_command == 'datetime':
                    Messages.send_message(session_api, chat_id, Datetime.datetime_now())
                # /Time
                # Fan
                elif msg_command[0:6] == 'random':
                    Util.random_band(session_api, chat_id, msg_command)
                # Fan

        # Not use. For personal messages
        if event.object.message['peer_id'] == event.object.message['from_id']:
            print(event.type)
            print(event)
            print(event.obj)
            #   something...
