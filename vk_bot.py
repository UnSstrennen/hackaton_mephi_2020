 # -*- coding: UTF-8 -*-
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint
from datetime import datetime
from json import load, dump
from get_places import api


TOKEN = 'd4e710f906b7ab1725a4e8ac4c65b34d848369a68fad3aadf6af8d216b56a51c7d61522a9d315b7b5070f'
start_msg = {'1': ['Привет! Наш бот поможет тебе подобрать спортивную школу. Давай для начала познакомимся.'],
             '2': ['Введи свой пол (Мужской/Женский)', '''{
"one_time": false,
   "buttons": [
     [{
       "action": {
         "type": "text",
         "payload": "{\"button\": \"1\"}",
         "label": "Red"
       },
       "color": "negative"
     },
    {
       "action": {
         "type": "text",
         "payload": "{\"button\": \"2\"}",
         "label": "Green"
       },
       "color": "positive"
     }]']''',
             '3': ['Отлично! Теперь введи свой возраст (0-99)', '{"buttons":[{"action": {"type": "text", "label": "test"}, "color": "positive"}],"one_time":true}'],
             '4': ['Наш бот может тебе помочь с подбором вида спорта, который будет тебе по нраву, но, может, ты уже определился с тем, каким спортом ты хочешь заниматься?'],
             '5': ['Давай я попробую найти тебе что-нибудь неподалёку. В каком районе ты живёшь?'],
             '6': ['И ещё один вопрос. Расскажи нам, какую группу мышц ты хотел бы "прокачать". (Спина, грудь, живот, руки, ноги). Чтобы я смог тебе помочь, попрошу вводить группы мышц через пробел.']}


def json_read():
    with open('json/users.json', encoding='utf-8-sig') as json_file:
        return load(json_file)

def json_load(data, user=None):
    if user is not None:
        data[str(user[0])] = user[-1]
    with open('json/users.json', 'w', encoding='utf-8-sig') as json_file:
        dump(data, json_file, ensure_ascii=False)

def write_msg(message, usid, keyboard=None):
    VK.messages.send(user_id=usid,
                     message=message,
                     random_id=randint(100000, 999999),
                     keyboard=keyboard)
    return message

def parser_message(usid, msg):
    if user['Статус'] == '1':
        func_1(usid, msg)
    elif user['Статус'] == '2':
        func_2(usid, msg)
    elif user['Статус'] == '3':
        func_3(usid, msg)
    elif user['Статус'] == '4':
        func_4(usid, msg)
    elif user['Статус'] == '5':
        func_5(usid, msg)
    elif user['Статус'] == '6':
        func_6(usid, msg)
    json_load(json_read(), user=(usid, user))


def func_1(usid, msg):
    global user
    if user['Пол'] is None:
        #write_msg('Введите свой пол(Мужской, Женский)', usid = usid)
        user['Статус'] = '2'
    elif user['Возраст'] is None:
        #write_msg('Введите свой возраст (числом)', usid = usid)
        user['Статус'] = '3'
    else:
        user['Статус'] = '4'

def func_2(usid, msg):
    if msg in ['Мужской', 'Женский']:
        # write_msg('Мы сохранили ваш пол', usid)
        user['Пол'] = msg
        user['Статус'] = '1'
        func_1(usid, msg)
    else:
        write_msg('Наш бот всё ещё не разобрался в множестве придуманных людьми полов. Наш бот пока что умеет работать с обычными мужчинами и женщинами.', usid)

def func_3(usid, msg):
    if msg.isdigit():
        write_msg('Мы сохранили ваш Djp', usid)
        user['Возраст'] = msg
        user['Статус'] = '1'
        func_1(usid, msg)
    else:
        write_msg('Введи норм djp', usid)

def func_4(usid, msg):
    if msg.lower() == 'да':
        user['Статус'] = '5'
    elif msg.lower() == 'нет':
        user['Статус'] = '6'

def func_5():
    pass

def func_6(usid, msg):
    if msg.lower() in ['руки', 'ноги', 'спина', 'живот', 'грудь']:
        sports = api.get_sports_names(user['Пол'], user['Возраст'], [msg])
        write_msg(sports, usid)
        user['Статус'] = '4'
    else:
        write_msg('Введи Мышцы одекватна, конч', usid)


def new_user(usid):
    user = VK.users.get(user_ids=usid, fields='sex')[0]
    users[str(usid)] = {'Имя': user['first_name'],
                                'Пол': {1: 'Женский',
                                        2: 'Мужской',
                                        0: None}[user['sex']],
                                'Возраст': None,
                                'Статус': '1'}
    write_msg(start_msg['1'], usid)
    json_load(users)


vk_session = VkApi(token=TOKEN)
VK = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            usid = event.user_id
            users = json_read()
            if str(usid) not in users:
                new_user(usid)
            user = json_read()[str(usid)]
            parser_message(usid, event.message)
            start = start_msg[json_read()[str(usid)]['Статус']]
            write_msg(start[0], usid, keyboard=start[-1])
