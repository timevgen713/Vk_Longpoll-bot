import Datetime
import Messages
import Connector
import random
import time


# Return chat members. And cutting json to get needful data
def getConversationMembers(session_api, event, dict_of_users):
    print("IN GET_CONVERSATION_MEMBERS EVENT=", event)
    clearList(dict_of_users)
    members_json = session_api.messages.getConversationMembers(peer_id=event.object.message['peer_id'])
    print("MEMBERS JSON: ", members_json)
    member_list = members_json['profiles']

    user_id = event.object.message['from_id']
    chat_id = event.object.message['peer_id']
    # iterate to cut data and add to dict
    for person in member_list:
        id = person['id']
        first_name = person['first_name']
        last_name = person['last_name']
        sex = person['sex']
        online = person['online']
        last_message_time = Connector.db_get_msg_last_time(chat_id, user_id)
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
            for temp in event.object.message['fwd_messages']:
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
                    Connector.db_warn(chat_id, int(user_id))
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
                    Connector.db_unwarn(chat_id, int(user_id))
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
            Messages.send_message(session_api, chat_id, 'Date is incorrect!')
    else:
        Messages.send_message(session_api, chat_id, 'Permission denied! You is not admin!')


def get_owner(session_api, event, dict_of_users):
    clearList(dict_of_users)
    members_json = session_api.messages.getConversationMembers(peer_id=event.object.message['peer_id'])
    print("MEMBERS JSON: ", members_json)

    admin = ''
    temp = 0
    for user in members_json['items']:
        try:
            if members_json['items'][temp]['is_owner'] is not None:
                if members_json['items'][temp]['is_owner']:
                    admin = members_json['items'][temp]['member_id']
                    break
        except KeyError:
            pass
        temp += 1
    print("GOT ADMINS: ", admin)
    return admin


def try_give_admin(event, session_api):
    try:
        chat_id = event.object.message['peer_id']
        Messages.send_message(session_api, chat_id,
                              "Hello! \n Give me admin role to work with chat. "
                              "\n1) Bot will start work after 20 seconds if you gave him an admin role"
                              "\n2) Bot will not work if you give not an admin role"
                              "\n\nP.s. If 2) was, try kick and invite again")
        time.sleep(20)
    except KeyError:
        pass


def get_chat_members(session_api, event):
    new_dict = session_api.messages.getConversationMembers(peer_id=event.object.message['peer_id'])['profiles']
    print("NEW DICT:::::::", new_dict)
    list_of_users = list()

    for user in new_dict:
        list_of_users.append(user['id'])
    print(list_of_users)
    return list_of_users


def simple_kick(chat_id, user_id):
    Messages.remove_user(chat_id, user_id)


def promote_user(event, session_api, chat_id, msg_command, dict_of_users):
    if Connector.isAdmin(chat_id, event.object.message['from_id']):
        getConversationMembers(session_api, event, dict_of_users)
        # check forward messages
        if len(event.object.message['fwd_messages']) != 0:
            for temp in event.object.message['fwd_messages']:
                Messages.send_message(session_api, chat_id,
                                      'User with id: \'' + str(int(temp['from_id'])) + '\' promoted successfully!')
                Connector.db_promote(chat_id, int(temp['from_id']))

        # check id in msg_command
        try:
            msg_ids = msg_command.split()[1:]
            for user_idd in msg_ids:
                user_id = (str(user_idd[3:]).split('|'))[0]
                if int(user_id) in dict_of_users.keys():
                    Messages.send_message(session_api, chat_id,
                                          'User with id: \'' + str(user_id) + '\' promoted successfully!')
                    Connector.db_promote(chat_id, int(user_id))
                else:
                    Messages.send_message(session_api, chat_id,
                                          'User with id: \'' + str(user_id) + '\' is not in chat!')
        except ValueError:
            Messages.send_message(session_api, chat_id, 'Id is incorrect!')
    else:
        Messages.send_message(session_api, chat_id, 'Permission denied! You is not admin!')


def drop_user(event, session_api, chat_id, msg_command, dict_of_users):
    if Connector.isAdmin(chat_id, event.object.message['from_id']):
        getConversationMembers(session_api, event, dict_of_users)
        # check forward messages
        if len(event.object.message['fwd_messages']) != 0:
            for temp in event.object.message['fwd_messages']:
                Messages.send_message(session_api, chat_id,
                                      'User with id: \'' + str(int(temp['from_id'])) + '\' dropped successfully!')
                Connector.db_drop(chat_id, int(temp['from_id']))

        # check id in msg_command
        try:
            msg_ids = msg_command.split()[1:]
            for user_idd in msg_ids:
                user_id = (str(user_idd[3:]).split('|'))[0]
                if int(user_id) in dict_of_users.keys():
                    Messages.send_message(session_api, chat_id,
                                          'User with id: \'' + str(user_id) + '\' dropped successfully!')
                    Connector.db_drop(chat_id, int(user_id))
                else:
                    Messages.send_message(session_api, chat_id,
                                          'User with id: \'' + str(user_id) + '\' is not in chat!')
        except ValueError:
            Messages.send_message(session_api, chat_id, 'Id is incorrect!')
    else:
        Messages.send_message(session_api, chat_id, 'Permission denied! You is not admin!')


def online_list(event, session_api, chat_id, msg_command, dict_of_users):
    members = getConversationMembers(session_api, event, dict_of_users)
    print('\n\n\n', members)

    temp = 1
    message = 'Online list:\n'
    for k, v in members.items():
        for k2 in v.keys():
            if k2 == 'online' and v[k2] == 1:
                message += str(temp) + '. vk.com/id' + str(k) + '\n'
                temp += 1
    Messages.send_message(session_api, chat_id, message)

def is_online(user_id, event, session_api, dict_of_users):
    members = getConversationMembers(session_api, event, dict_of_users)

    try:
        for k, v in members.items():
            for k2 in v.keys():
                if k2 == 'online' and v[k2] == 1 and str(k) == str(user_id):
                    return True;
                else:
                    return False
    except KeyError:
        pass
