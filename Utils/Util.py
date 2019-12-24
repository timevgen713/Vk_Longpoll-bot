import Messages
import User
import random

# Iterate dict with users and send msg in format '1. vk.com/{id} 'first_name' 'last_name'
def dict_iterator_and_send(dict_of_users, session_api, chat_id, event):
    User.getConversationMembers(session_api, event, dict_of_users)

    message = ''
    temp = 1
    for user in dict_of_users.keys():
        message += str(temp) + '. vk.com/id' + str(user) + ' ' + dict_of_users.get(user)['first_name'] \
                   + ' ' + dict_of_users.get(user)['last_name'] + '\n'
        temp += 1

    Messages.send_message(session_api, chat_id, message)

# All bot known commands
def all_commands(session_api, peer_id):
    message = 'List of commands: \n ' \
              '     Date & Time:\n' \
              '         1. !date (return current date)\n' \
              '         2. !time (return current Moscow time)\n' \
              '         3. !datetime (return !date + !time)\n' \
              '     Chat members:\n' \
              '         1. !members (return list of this chat members)\n' \
              '         2. !kick {id} (kick user from id. Example to kick (id=567123): !kick 567123\n'
    Messages.send_message(session_api, peer_id, message)

def random_band(session_api, chat_id, msg_command):
    try:
        min = int(str(msg_command).split(' ')[1])
        max = int(str(msg_command).split(' ')[2])
        result = random.randint(min, max)
        Messages.send_message(session_api, chat_id, 'Your random generated number is ' + str(result))
    except ValueError:
        Messages.send_message(session_api, chat_id, 'Input incorrect!')


def broadcast(session_api, chat_id, msg_command, event, dict_of_users):
    message = ''

    members = User.getConversationMembers(session_api, event, dict_of_users)
    for member in dict_of_users.keys():
        message += '@id' + str(member) + " "

    message += msg_command.split()[1]

    Messages.send_message(session_api, chat_id, message)
