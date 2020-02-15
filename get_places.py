#ТВОЙ КЛАСС - Api


import requests
import json


TRAINERS_ID = 61321
SPORT_PLACES_ID = 629

class Requester:
    def __init__(self):
        # ключ
        self.key = '2f7bb5a558cdb753684c8781084863ed'

    def add_params(self, url, params):
        # служебный класс
        url += "?api_key={}&".format(self.key)
        for param in params:
            print(param)
            url += param + '&'
        return url

    def get_count(self, dataset_id):
        # получение количества записей в датасете
        url = 'https://apidata.mos.ru/v1/datasets/{}/count'.format(dataset_id)
        url = self.add_params(url, '')
        count = requests.get(url).text
        return int(count)

    def get_rows(self, dataset_id, *params):
        # получение всех записей датасета, работает очень долго!
        url = 'https://apidata.mos.ru/v1/datasets/{}/rows'.format(dataset_id)
        url = self.add_params(url, params)
        print(url)
        return requests.get(url).json()


class Api:
    def __init__(self):
        #  подключение служебного класса
        self.req = Requester()

    def get_count(self, id):
        # получить число записей в датасете по айди
        return self.req.get_count(id)

    def find_nearest_districts(self, district):
        # поиск районов поблизости заданного района
        json_data = json.loads(open('json/districts.json', encoding='utf-8-sig').read())
        for key in json_data.keys():
            if district in json_data[key]:
                return json_data[key]
        return 'error'

    def get_places_names_by_districts(self, district):
        # получить названия учреждений по районам БЕЗ УЧЕТА СПОРТА
        res = []
        districts = self.find_nearest_districts(self, district)
        if districts == 'error':
            return 'error'
        x = self.req.get_rows(SPORT_PLACES_ID, '')
        for i in range(self.get_count(SPORT_PLACES_ID)):
            obj = x[i]['Cells']
            obj_name = obj['FullName']
            obj_district = obj['ObjectAddress'][0]['District'].replace('район', '').replace('поселение', '').strip()
            if x[i]['Cells']['ObjectAddress'][0]['District'] in districts:
                res.append(obj_name)
            return res

    def get_sports_names(self, gender, age, muscles):
        # получить рекомеендуемые виды спорта
        res = []
        gender = gender.lower()
        if gender == 'м':
            gender = 'm'
        elif gender == 'ж':
            gender = 'f'
        if gender not in ['m', 'f']:
            return 'error'

        json_data = json.loads(open('json/sports.json', encoding='utf-8-sig').read())

        for key in json_data.keys():
            sport = json_data[key]
            min_age, max_age = sport['age']
            gender_ok = gender in sport['genders']
            age_ok = int(min_age) <= int(age) <= int(max_age)
            sport_muscles = sport['muscles']
            muscles_ok = True
            for muscle in muscles:
                if muscle not in sport_muscles:
                    muscles_ok = False
            if muscles_ok and gender_ok and age_ok:
                res.append(key)
        return res

    def make_links(self, names):
        # создание ссылок на карты по названиям учреждений
        res = []
        for name in names:
            res.append([name, 'https://yandex.ru/maps/213/moscow/?text={}&z=16'.format(name)])
        return res

api = Api()
