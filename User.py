import Datetime
import Messages

# Return chat members. And cutting json to get needful data
def getConversationMembers(session_api, event, dict_of_users):
    members_json = session_api.messages.getConversationMembers(peer_id=event.object.message['peer_id'])
    member_list = members_json['profiles']

    # iterate to cut data and add to dict
    for person in member_list:
        id = person['id']
        first_name = person['first_name']
        last_name = person['last_name']
        sex = person['sex']
        online = person['online']
        last_message_time = Datetime.msg_last_time_format()
        dict_of_users[id] = {'last_name': last_name, 'first_name': first_name,
                                   'sex': sex, 'online': online, 'last_message_time': last_message_time}

    return dict_of_users

# Only clean dict
def clearList(dict_of_users):
    dict_of_users.clear()

# Remove user and check data validation( not null, it;s integer and user in chat) else send not found.
def remove_user(event, session_api, chat_id, msg_command, dict_of_users):
    getConversationMembers(session_api, event, dict_of_users)

    if len(event.object.message['fwd_messages']) != 0:
        for temp in event.object.message['fwd_messages']:
            Messages.remove_user(chat_id, int(temp['from_id']))

    try:
        msg_ids = msg_command.split()[1:]
        for user_idd in msg_ids:
            user_id = (str(user_idd[3:]).split('|'))[0]
            if int(user_id) in dict_of_users.keys():
                Messages.remove_user(chat_id, user_id)
            else:
                Messages.send_message(session_api, chat_id, 'User with id: \'' + str(user_id) + '\' is not in chat!')
    except ValueError:
        Messages.send_message(session_api, chat_id, 'Id is incorrect!')
        
def ban_user(event, session_api, chat_id, peer_id, msg_command, dict_of_users):
    remove_user(event, session_api, peer_id, msg_command, dict_of_users)

def ban(chat_id, msg_command):
    ban_id = str(msg_command).split(' ')[1]
    ban_time = str(msg_command).split(' ')[2] # ADD THIS IN DB
    Messages.remove_user(chat_id, ban_id)
