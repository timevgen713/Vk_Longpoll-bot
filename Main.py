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
        chat_id = event.object.message['peer_id']
        # FOR MESSAGES FROM CHAT
        try:
            if event.object.message['action']['type'] == 'chat_invite_user' and event.object.message['action']['member_id'] == -188541150:
                Connector.delete_chat(chat_id)

                User.try_give_admin(event, session_api)
                owner = User.get_owner(session_api, event, dict_of_users)
                chat_members = User.get_chat_members(session_api, event)

                Connector.new_chat(chat_id, owner, chat_members)
                Messages.send_message(session_api, chat_id,
                                      "Admin given success.\n\nCreate chat with id = " + str(chat_id) +
                                      "\nAdmin: " + str(owner) +
                                      "\nUsers: " + str(chat_members))
        except KeyError:
            pass
    try:
        if event.object.message['action']['type'] == 'chat_invite_user' and -188541150 != \
                event.object.message['action']['member_id']:
            chat_id = event.object.message['peer_id']
            Connector.db_invite_user(chat_id, event.object.message['action']['member_id'])
    except KeyError:
        pass

    try:
        if event.object.message['action']['type'] == 'chat_kick_user' and -188541150 != \
                event.object.message['action']['member_id']:
            chat_id = event.object.message['peer_id']
            Connector.db_delete_user(chat_id, event.object.message['action']['member_id'])
    except KeyError:
        pass
    # if it's chat (peer_id != from_id) and it's a message( not invite or kick)
    if event.object.message['peer_id'] != event.object.message['from_id'] and event.object.message['text'] != '':
        # --------------------------Variables--------------------------------------------------
        chat_id = event.object.message['peer_id']  # chat id
        message_id = event.object.message['conversation_message_id']  # message , to write last user msg in DB
        from_id = event.object.message['from_id']  # who send message (user)
        message = event.object.message['text']  # message text
        user_id = event.object.message['from_id']  # sender id

        msg_symbol = message[0]  # if command-symbol ($)
        msg_command = message[1:]  # command body ( without $)

        # --------------------------Variables--------------------------------------------------
        Messages.increment_msg_amount(chat_id, user_id)
        Connector.db_msg_last_time_add(chat_id, user_id)

        if msg_symbol == '$':
            if msg_command == 'commands':
                Util.all_commands(session_api, chat_id)
            # User management
            elif msg_command == 'members':
                Util.dict_iterator_and_send(dict_of_users, session_api, chat_id, event)
            elif msg_command[0:8] == 'kickfrom':
                User.kickfrom_user(event, session_api, chat_id, msg_command)
            elif msg_command[0:4] == 'kick':
                User.remove_user(event, session_api, chat_id, msg_command, dict_of_users)
            elif msg_command[0:4] == 'warn':
                User.warn_user(event, session_api, chat_id, msg_command, dict_of_users)
            elif msg_command[0:6] == 'unwarn':
                User.unwarn_user(event, session_api, chat_id, msg_command, dict_of_users)
            elif msg_command[0:7] == 'promote':
                User.promote_user(event, session_api, chat_id, msg_command, dict_of_users)
            elif msg_command[0:4] == 'drop':
                User.drop_user(event, session_api, chat_id, msg_command, dict_of_users)
            elif msg_command[0:6] == 'online':
                User.online_list(event, session_api, chat_id, msg_command, dict_of_users)
            # /User management
            # Statistic
            elif msg_command[0:5] == 'state':
                pass
            # /Statistic
            # Time
            elif msg_command == 'time':
                Messages.send_message(session_api, chat_id, Datetime.time_now_for_user())
            elif msg_command == 'date':
                Messages.send_message(session_api, chat_id, Datetime.date_now())
            elif msg_command == 'datetime':
                Messages.send_message(session_api, chat_id, Datetime.datetime_now_for_user())
            # /Time
            # Fan
            elif msg_command[0:6] == 'random':
                Util.random_band(session_api, chat_id, msg_command)
            elif msg_command[0:9] == 'broadcast':
                Util.broadcast(session_api, chat_id, msg_command, event, dict_of_users)
            elif msg_command[0:7] == 'selfban':
                User.simple_kick(chat_id, from_id)
            # Fan

    # Not use. For personal messages
    if event.object.message['peer_id'] == event.object.message['from_id']:
        print(event.type)
        print(event)
        print(event.obj)
        #   something...
