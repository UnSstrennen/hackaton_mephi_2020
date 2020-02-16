import requests
import json
from os import remove


TRAINERS_ID = 61321
SPORT_PLACES_ID = 629

MAX_SPORTS = 25
CACHING = True  # without caching it works much slower

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

    def get_rows(self, dataset_id, *params, from_cache=False):
        # получение всех записей датасета, работает очень долго!
        if from_cache:
            if dataset_id == TRAINERS_ID:
                return json.loads(open('json/trainers.json', encoding="utf-8-sig", mode='r').read())
            elif dataset_id == SPORT_PLACES_ID:
                return json.loads(open('json/sport_places.json', encoding="utf-8-sig", mode='r').read())
            return
        url = 'https://apidata.mos.ru/v1/datasets/{}/rows'.format(dataset_id)
        url = self.add_params(url, params)
        print(url)
        return requests.get(url).json()


class Api:
    def __init__(self):
        #  подключение служебного класса
        self.req = Requester()
        # download actual json for make it working faster
        sample = self.req.get_rows(SPORT_PLACES_ID, '')
        # clean users.json
        with open('json/users.json', 'w', encoding='utf-8-sig') as fp:
                json.dump({}, fp)
        with open('json/sport_places.json', 'w', encoding='utf-8-sig') as fp:
                json.dump(sample, fp)
        # download actual json for make it working faster
        sample = self.req.get_rows(TRAINERS_ID, '')
        with open('json/trainers.json', 'w', encoding='utf-8-sig') as fp:
                json.dump(sample, fp)
        print('starting vk bot...')

    def combine(self, names_with_emails, sport):
        res = []
        sport = sport.capitalize()
        x = self.req.get_rows(TRAINERS_ID, '', from_cache=CACHING)
        #make all emails
        emails = []
        [emails.append(i['email']) for i in names_with_emails]
        for i in range(self.get_count(TRAINERS_ID)):
            this_email = x[i]['Cells']['Email'][0]['Email']
            if this_email in emails:
                this_sport = x[i]['Cells']['Sport'][0]['SportName'].capitalize()
                if sport == this_sport:
                    this_name = names_with_emails[emails.index(this_email)]['name']
                    if this_name not in res:
                        res.append(this_name)
        return res

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

    def get_places_names_by_districts(self, district, with_email=False):
        # получить названия учреждений по районам
        district = district.capitalize()
        res = []
        districts = self.find_nearest_districts(district)
        if districts == 'error':
            return 'error'
        x = self.req.get_rows(SPORT_PLACES_ID, '', from_cache=CACHING)
        for i in range(self.get_count(SPORT_PLACES_ID)):
            obj = x[i]['Cells']
            obj_email = obj['Email'][0]['Email']
            obj_name = obj['FullName']
            obj_district = obj['ObjectAddress'][0]['District']
            if obj_district is None:
                continue
            obj_district = obj_district.replace('район', '').replace('поселение', '').strip()
            if obj_district in districts:
                if not with_email:
                    res.append(obj_name)
                else:
                    res.append({'name': obj_name, 'email': obj_email})
        return res

    def get_sports_names(self, gender, age, muscles):
        # получить рекомендуемые виды спорта
        res = []
        gender = gender.lower()
        if gender in ['м', 'мужской']:
            gender = 'm'
        elif gender in ['ж', 'женский']:
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
        return res[:MAX_SPORTS]

    def make_links(self, names):
        # создание ссылок на карты по названиям учреждений
        res = []
        for name in names:
            res.append([name, 'https://yandex.ru/maps/213/moscow/?text={}&z=16'.format(name.replace(' ', '%20'))])
        return res

    def get_all_data(self, district, sport):
        # конечно определяет подкходящие школы по району и выбранному спорту
        places = self.get_places_names_by_districts(district, with_email=True)
        # combine places with trainers
        print(places)
        if places == 'error':
            return 'not'
        correct_schools = self.combine(places, sport)
        print(correct_schools)
        schools_with_links = self.make_links(correct_schools)
        count = len(schools_with_links)
        out = 'По вашему спорту найдено {} организаций поблизости к вам.\n\n'.format(count)
        for i in schools_with_links:
            # 0 - name 1 - link
            out += '{}\n{}\n\n'.format(i[0], i[1])
        return out


api = Api()
