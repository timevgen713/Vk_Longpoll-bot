import Datetime
import Messages
import Connector
import random


# Return chat members. And cutting json to get needful data
def getConversationMembers(session_api, event, dict_of_users):
    clearList(dict_of_users)
    members_json = session_api.messages.getConversationMembers(peer_id=event.object.message['peer_id'])
    print("MEMBERS JSON: ", members_json)
    member_list = members_json['profiles']

    # iterate to cut data and add to dict
    for person in member_list:
        id = person['id']
        first_name = person['first_name']
        last_name = person['last_name']
        sex = person['sex']
        online = person['online']
        last_message_time = Datetime.datetime_now()
        dict_of_users[id] = {'last_name': last_name, 'first_name': first_name,
                             'sex': sex, 'online': online, 'last_message_time': last_message_time}
    print(dict_of_users)
    return dict_of_users


# Only clean dict
def clearList(dict_of_users):
    dict_of_users.clear()


# Remove user and check data validation( not null, it;s integer and user in chat) else send not found.
def remove_user(event, session_api, chat_id, msg_command, dict_of_users):
    if Connector.isAdmin(chat_id, event.object.message['from_id']):
        getConversationMembers(session_api, event, dict_of_users)
        # check forward messages
        if len(event.object.message['fwd_messages']) != 0:
            for temp in event.object.message['fwd_messages']: \
                    Messages.remove_user(chat_id, int(temp['from_id']))

        # check id in msg_command
        try:
            msg_ids = msg_command.split()[1:]
            for user_idd in msg_ids:
                user_id = (str(user_idd[3:]).split('|'))[0]
                if int(user_id) in dict_of_users.keys():
                    Messages.remove_user(chat_id, user_id)
                else:
                    Messages.send_message(session_api, chat_id,
                                          'User with id: \'' + str(user_id) + '\' is not in chat!')
        except ValueError:
            Messages.send_message(session_api, chat_id, 'Id is incorrect!')
    else:
        Messages.send_message(session_api, chat_id, 'Permission denied! You is not admin!')


def warn_user(event, session_api, chat_id, msg_command, dict_of_users):
    if Connector.isAdmin(chat_id, event.object.message['from_id']):
        getConversationMembers(session_api, event, dict_of_users)
        # check forward messages
        if len(event.object.message['fwd_messages']) != 0:
            for temp in event.object.message['fwd_messages']:
                Messages.send_message(session_api, chat_id,
                                      'User with id: \'' + str(int(temp['from_id'])) + '\' warned successful!')
                Connector.db_warn(chat_id, int(temp['from_id']))

        # check id in msg_command
        try:
            msg_ids = msg_command.split()[1:]
            for user_idd in msg_ids:
                user_id = (str(user_idd[3:]).split('|'))[0]
                if int(user_id) in dict_of_users.keys():
                    Messages.send_message(session_api, chat_id,
                                          'User with id: \'' + str(user_id) + '\' warned successful!')
                    Connector.db_warn(chat_id, int(temp['from_id']))
                else:
                    Messages.send_message(session_api, chat_id,
                                          'User with id: \'' + str(user_id) + '\' is not in chat!')
        except ValueError:
            Messages.send_message(session_api, chat_id, 'Id is incorrect!')
    else:
        Messages.send_message(session_api, chat_id, 'Permission denied! You is not admin!')


def unwarn_user(event, session_api, chat_id, msg_command, dict_of_users):
    if Connector.isAdmin(chat_id, event.object.message['from_id']):
        getConversationMembers(session_api, event, dict_of_users)
        # check forward messages
        if len(event.object.message['fwd_messages']) != 0:
            for temp in event.object.message['fwd_messages']:
                Messages.send_message(session_api, chat_id,
                                      'User with id: \'' + str(int(temp['from_id'])) + '\' unwarned successful!')
                Connector.db_unwarn(chat_id, int(temp['from_id']))

        # check id in msg_command
        try:
            msg_ids = msg_command.split()[1:]
            for user_idd in msg_ids:
                user_id = (str(user_idd[3:]).split('|'))[0]
                if int(user_id) in dict_of_users.keys():
                    Messages.send_message(session_api, chat_id,
                                          'User with id: \'' + str(user_id) + '\' unwarned successful!')
                    Connector.db_unwarn(chat_id, int(temp['from_id']))
                else:
                    Messages.send_message(session_api, chat_id,
                                          'User with id: \'' + str(user_id) + '\' is not in chat!')
        except ValueError:
            Messages.send_message(session_api, chat_id, 'Id is incorrect!')
    else:
        Messages.send_message(session_api, chat_id, 'Permission denied! You is not admin!')


def kickfrom_user(event, session_api, chat_id, msg_command):
    if Connector.isAdmin(chat_id, event.object.message['from_id']):
        try:
            time = msg_command.split(' ')[1]
            Connector.db_kickfrom(chat_id, time)
        except ValueError:
            Messages.send_message(session_api, chat_id, 'Time is incorrect!')
    else:
        Messages.send_message(session_api, chat_id, 'Permission denied! You is not admin!')


def get_state(event, session_api, chat_id, msg_command, dict_of_users):
    getConversationMembers(session_api, event, dict_of_users)

    user_id = msg_command.split(" ")[1]
    from_id = event.object.message['from_id']

    if Connector.isAdmin(chat_id, from_id):
        try:
            if msg_command.split(" ")[2] == "details":
                msg_amount = Connector.db_get_msg_amount(chat_id, user_id)
                online = False
                if dict(dict_of_users).get(user_id)['online'] == 1:
                    online = True
                else:
                    online = False
                last_msg_time = Connector.db_get_msg_last_time(chat_id, user_id)
                activeTop = random.randint(1, len(dict_of_users))

                role = ""
                warns = 0
                if Connector.isAdmin(chat_id, user_id):
                    role = "Admin"
                else:
                    role = "User"
                warns = Connector.db_getWarns(chat_id, user_id)

                Messages.send_message(session_api, chat_id, 'Statistic for vk.com/id' + str(user_id) + "\n" +
                                      "Amount of messages: " + str(msg_amount) +
                                      "Online: " + str(online) +
                                      "Last message time: " + str(last_msg_time) +
                                      "Place in active top: " + str(activeTop) +
                                      "Role: " + str(role) +
                                      "Warns: " + str(warns))
            else:
                msg_amount = Connector.db_get_msg_amount(chat_id, user_id)
                online = False
                if dict(dict_of_users).get(user_id)['online'] == 1:
                    online = True
                else:
                    online = False
                last_msg_time = Connector.db_get_msg_last_time(chat_id, user_id)
                activeTop = random.randint(1, len(dict_of_users))

                Messages.send_message(session_api, chat_id, 'Statistic for vk.com/id' + str(user_id) + "\n" +
                                      "Amount of messages: " + str(msg_amount) +
                                      "Online: " + str(online) +
                                      "Last message time: " + str(last_msg_time) +
                                      "Place in active top: " + str(activeTop))
        except ValueError:
            Messages.send_message(session_api, chat_id, 'Params are incorrect!')
    else:
        Messages.send_message(session_api, chat_id, 'Permission denied. You are not admin!')
