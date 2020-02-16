 # -*- coding: UTF-8 -*-
from vk_api import VkApi
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint
from json import load, dump, loads
from get_places import api


TOKEN = '7737940d04670de9953ad5b6ee5aafd8e94b5f96f40666d187f84893b96a8a19399e9b82f95b86a6aaa81'
start_msg = {'1': ['Заполним информацию о тебе.', '{"buttons":[],"one_time":true}'],
              '2': ['Выбери свой пол', '{"one_time": true, "buttons": [[{"action": {"type": "text", "label": "Мужской"}, "color": "positive"}, {"action": {"type": "text", "label": "Женский"}, "color": "positive"}]]}'],
              '3': ['Введи свой возраст (0-99)', '{"buttons":[],"one_time":true}'],
              '4': ['Ты уже определился с тем, каким спортом ты хочешь заниматься?', '{"one_time": true, "buttons": [[{"action": {"type": "text", "label": "Я определился"}, "color": "positive"}, {"action": {"type": "text", "label": "Я не определился"}, "color": "positive"}], [{"action": {"type": "text", "label": "Редактировать личные данные"}, "color": "positive"}]]}'],
              '5': ['Давай я попробую найти тебе что-нибудь неподалёку. В каком районе ты живёшь?', '{"buttons":[[{"action": {"type": "text", "label": "Меню"}, "color": "positive"}]],"one_time":true}'],
              '6': ['Выбери какую группу мышц ты хотел бы "прокачать". Чтобы я смог тебе помочь, попрошу вводить группы мышц через пробел.',
              '{"one_time": true, "buttons": [[{"action": {"type": "text", "label": "Спина"}, "color": "positive"}, {"action": {"type": "text", "label": "Грудь"}, "color": "positive"}, {"action": {"type": "text", "label": "Живот"}, "color": "positive"}], [{"action": {"type": "text", "label": "Руки"}, "color": "positive"}, {"action": {"type": "text", "label": "Ноги"}, "color": "positive"}, {"action": {"type": "text", "label": "Меню"}, "color": "positive"}]]}'],
              '7': ['Выбери какую личную информацию ты желаешь изменить',
              '{"one_time": true, "buttons": [[{"action": {"type": "text", "label": "Возраст"}, "color": "positive"}, {"action": {"type": "text", "label": "Пол"}, "color": "positive"}], [{"action": {"type": "text", "label": "Меню"}, "color": "positive"}]]}'],
              '8': ['Введите спорт, которым хотите заниматься', '{"buttons":[[{"action": {"type": "text", "label": "Меню"}, "color": "positive"}]],"one_time":true}']}

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
    if msg == 'Начало':
        write_msg('Привет! Наш бот поможет тебе подобрать спортивную школу.', usid)
    elif user['Статус'] == '1':
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
    elif user['Статус'] == '7':
        func_7(usid, msg)
    elif user['Статус'] == '8':
        func_8(usid, msg)
    json_load(json_read(), user=(usid, user))


def func_1(usid, msg):
    global user
    if user['Пол'] is None:
        user['Статус'] = '2'
    elif user['Возраст'] is None:
        user['Статус'] = '3'
    else:
        user['Статус'] = '4'

def func_2(usid, msg):
    if msg in ['Мужской', 'Женский']:
        write_msg('Мы сохранили ваш пол', usid)
        user['Пол'] = msg
        user['Статус'] = '1'
        func_1(usid, msg)
    else:
        write_msg('Наш бот всё ещё не разобрался в множестве придуманных людьми полов. Наш бот пока что умеет работать с обычными мужчинами и женщинами.', usid)

def func_3(usid, msg):
    if msg.isdigit() and '-' not in msg:
        write_msg('Мы сохранили ваш возраст', usid)
        user['Возраст'] = msg
        user['Статус'] = '1'
        func_1(usid, msg)
    else:
        write_msg('Вы ввели неверный формат', usid)

def func_4(usid, msg):
    if msg == 'Я определился':
        user['Статус'] = '8'
    elif msg == 'Я не определился':
        user['Статус'] = '6'
    elif msg == 'Редактировать личные данные':
        user['Статус'] = '7'
    else:
        write_msg('Ничего не понял, тыкай на кнопки', usid)

def func_5(usid, msg):
    if msg == 'Меню':
        user['Статус'] = '4'
    else:
        write_msg('Поиск...', usid)
        res = api.get_all_data(msg.lower().title(), user['Спорт'])
        if res not in ['error', 'not']:
            if res == '':
                res = 'Ничего не найденно'
            print('##->'+res)
            write_msg(res, usid)
            user['Спорт'] = None
            user['Статус'] = '4'
        else:
            write_msg('Похоже в названии района допущена ошибка', usid)

def func_6(usid, msg):
    if msg.lower() in ['руки', 'ноги', 'спина', 'живот', 'грудь']:
        sports = '\n'.join(api.get_sports_names(user['Пол'], user['Возраст'], [msg.lower()]))
        write_msg(sports, usid)
        user['Статус'] = '8'
    elif msg == 'Меню':
        user['Статус'] = '4'
    else:
        write_msg('Ничего не понял, тыкайте на кнопочки', usid, keyboard=start_msg['4'][-1])

def func_7(usid, msg):
    if msg == 'Возраст':
        user['Возраст'] = None
        user['Статус'] = '3'
    elif msg == 'Пол':
        user['Пол'] = None
        user['Статус'] = '2'
    elif msg == 'Меню':
        user['Статус'] = '4'
    else:
        write_msg('Что-то я ничего не понял', usid)

def func_8(usid, msg):
    json_data = loads(open('json/sports.json', encoding='utf-8-sig').read())
    print(list(json_data.keys()))
    if msg.lower().title() in list(json_data.keys()):
        user['Статус'] = '5'
        user['Спорт'] = msg.lower().title()
    elif msg == 'Меню':
        user['Статус'] = '4'
    else:
        write_msg('Мы не знаем о таком спорте', usid)

def new_user(usid):
    user = VK.users.get(user_ids=usid, fields='sex')[0]
    users[str(usid)] = {'Имя': user['first_name'],
                        'Пол': {1: 'Женский',
                                2: 'Мужской',
                                0: None}[user['sex']],
                                 'Возраст': None,
                                 'Статус': '1',
                                 'Спорт': None,
                                 'Сон': False}
    write_msg(start_msg['1'][0], usid)
    json_load(users)


vk_session = VkApi(token=TOKEN)
VK = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.user_id in [254346684, 396474534, 261847568, 452865637]:
                write_msg('Вы были забанены по причине: \n Не патриот', event.user_id)
            else:
                usid = event.user_id
                users = json_read()
                if str(usid) not in users:
                    new_user(usid)
                user = json_read()[str(usid)]
                parser_message(usid, event.message)
                if not user['Сон']:
                    start = start_msg[json_read()[str(usid)]['Статус']]
                    write_msg(start[0], usid, keyboard=start[-1])
