import requests
from pprint import pprint
import time

class Headhunter:
    def __init__(self, url):
        self._url = url


    def find(self, request, town):
        params = {'text': request + ' AND area: ' + town}
        skills = []
        # Полечение общего результата
        count = 0
        result = requests.get(self._url, params = params).json() # Делаем GET запрос и берем его json сожержимое
        for item in result['items']:
            url_vac = item['url']
            time.sleep(1)
            print(f'Адресс {url_vac} обработан')
            req = requests.get(url_vac).json()
            skill = req['key_skills']
            skills += skill
            count += 1
            if count == 20:
                break
        return self._dict_skills(skills)

    def _dict_skills(self, skills):
        array_skills = []
        count_skills = []
        for skill in skills:
            value = skill['name']
            print(f'{value=}')
            if value in array_skills:
                print('yes')
                index = array_skills.index(value)
                count_skills[index] += 1
            else:
                print('No')
                array_skills.append(value)
                count_skills.append(1)
        combined = list(zip(count_skills, array_skills))
        sorted_combined = sorted(combined, reverse=True)
        return sorted_combined
