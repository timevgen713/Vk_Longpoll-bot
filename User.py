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
    forward_ids = list()

    if len(event.object.message['fwd_messages']) != 0:
        for temp in event.object.message['fwd_messages']:
            forward_ids.append(temp['from_id'])

    try:
        msg_ids = msg_command[5:].split()
        for user_id in msg_ids:
            if int(user_id) in dict_of_users.keys():
                Message.remove_user(peer_id, user_id)
            else:
                Message.send_message(session_api, peer_id, 'User with id: \'' + str(user_id) + '\' is not in chat!')
    except ValueError:
        Message.send_message(session_api, peer_id, 'Id is incorrect!')