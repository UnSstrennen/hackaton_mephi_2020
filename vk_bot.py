# -*- coding: UTF-8 -*-
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint
from datetime import datetime
from json import load


TOKEN =
 vk_session = VkApi(token=TOKEN)
 VK = vk_session.get_api()
 longpoll = VkLongPoll(vk_session)
 print(time(), 'Бот запущен.', file=LOG_FILE)
 with open(NAME_USERS_FILE, 'w'):
     pass

 if __name__ == '__main__':
     for event in longpoll.listen():
         if event.type == VkEventType.MESSAGE_NEW and event.to_me:
             print('_'*20+'\n# Новое сообщение. ID:', str(event.user_id), file=LOG_FILE)
             print('Пользователь:', name_id(event.user_id))
             print(time(), 'Сообщение:\n'+event.text, file=LOG_FILE)
             print('_# Ответ бота:\n', new_message(event), file=LOG_FILE)
