import Datetime
import Message

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
def remove_user(event, session_api, peer_id, msg_command, dict_of_users):
    getConversationMembers(session_api, event, dict_of_users)
    try:
        value = int(msg_command[5:])
        if value in dict_of_users.keys():
            Message.remove_user(peer_id, value)
        else:
            Message.send_message(session_api, peer_id, 'User is not in conversation!')
    except ValueError:
        Message.send_message(session_api, peer_id, 'User is not in conversation!')