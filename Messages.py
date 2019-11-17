import random
import requests as request
from NO_GIT import advanced_data

# Send message with needful params( required: session_api, peer_id, message)
def send_message(session_api, peer_id, message=None, attachment=None, keyboard=None, payload=None):
    session_api.messages.send(peer_id=peer_id, message=message, random_id=random.randint(-2147483648, +2147483648),
                              attachment=attachment, keyboard=keyboard, payload=payload)

# remove user from chat (required params: access_token, group_id, v, chat_id, user_id)
def remove_user(chat_id, user_id):
    params = {'access_token': advanced_data.token, 'group_id': 188541150, 'v': 5.103,
                                                    'chat_id': int(chat_id - 2000000000), 'user_id': user_id}
    request.get('https://api.vk.com/method/messages.removeChatUser', params=params)