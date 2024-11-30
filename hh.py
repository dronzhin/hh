import requests
import pprint

URL = 'https://api.hh.ru/vacancies'

class Headhunter:
    def __init__(self, url, name_file):
        self._url = url
        self._array_request = []
        self.name = name_file


    def find(self, request, town):
        params = {'text': request + ' AND area: ' + town}

        result = requests.get(self._url, params = params).json() # Делаем GET запрос и берем его json сожержимое
        self._array_request.append(result)
        text = f'Найдено {result['found']} вакансий'
        print(text)
        with open(self.name, 'w') as f:
            f.write(text + '\n\n')


    def responsibility(self, array):
        # Создаем пустой словарь из неоходимых требований
        count = 0
        self.dict = {name: 0 for name in array}
        for reqs in self._array_request:
            for name in array:
                for req in reqs['items']:
                    if name in req['snippet']['responsibility']:
                        self.dict[name] = 1 + self.dict[name]
                        count += 1
        f = open(self.name, 'a')
        for key, value in self.dict.items():
            text = f'{key} : {value} --  {value/count*100}%'
            print(text)
            f.write(text + '\n')
        f.close()




    @property
    def array_request(self):
        return self._array_request


hh = Headhunter(URL, 'log.txt')
find_facation = 'Python разработчик'
city = 'Москва'
hh.find(find_facation, city)
print()

find_responsibility = ['Python', 'SQL', 'Excel', 'Power BI', 'IaaS']
hh.responsibility(find_responsibility)
