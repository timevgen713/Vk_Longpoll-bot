import Message
import User

# Iterate dict with users and send msg in format '1. vk.com/{id} 'first_name' 'last_name'
def dict_iterator_and_send(dict_of_users, session_api, peer_id, event):
    User.getConversationMembers(session_api, event, dict_of_users)

    message = ''
    temp = 1
    for user in dict_of_users.keys():
        message += str(temp) + '. vk.com/id' + str(user) + ' ' + dict_of_users.get(user)['first_name'] \
                   + ' ' + dict_of_users.get(user)['last_name'] + '\n'
        temp += 1

    Message.send_message(session_api, peer_id, message)

# All bot known commands
def all_commands(session_api, peer_id):
    message = 'List of commands: \n ' \
              '____Date & Time:\n' \
              '________1. !date (return current date)\n' \
              '________2. !time (return current Moscow time)\n' \
              '________3. !datetime (return !date + !time)\n' \
              '____Chat members:\n' \
              '________1. !members (return list of this chat members)\n' \
              '________2. !kick {id} (kick user from id. Example to kick (id=567123): !kick 567123\n'
    Message.send_message(session_api, peer_id, message)