from flask import Flask, render_template, request
from hh import Headhunter
from cachetools import cached, TTLCache
from sqlite import create_sql, insert_to_bd, insert_to_requests

URL = 'https://api.hh.ru/vacancies'
path_bd = 'bd_sql'
hh = Headhunter(URL)
app = Flask(__name__)

# Настройка кеша
cache = TTLCache(maxsize=10, ttl=300)  # Кеш с временем жизни 5 минут

@cached(cache)
def request_cash(find_vacation, city):
    return hh.find(find_vacation, city)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/input/')
def input_page():
    return render_template('input.html')

@app.route('/result/')
def result():
    return render_template('result.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/submit/', methods=['POST'])
def submit():
    # Получаем данные из формы
    city = request.form.get('city')
    insert_to_bd(path_bd, 'town', city)
    print(city, type(city))
    position = request.form.get('position worker')
    insert_to_bd(path_bd, 'vacancy', position)
    print(position, type(position))


    count_skills = int(request.form.get('skill'))
    print(count_skills, type(count_skills))
    skills = request_cash(position, city)[:count_skills]
    for skill in skills:
        print(skill[1], type(skill[1]))
        insert_to_bd(path_bd, 'skill', value=skill[1])
        insert_to_requests(path_bd, (path_bd, (city, position, skill[1], count_skills)))

    summa = sum([i for i,j in skills])
    skills_proc = [(i, j, round(i/summa*100, 1)) for i, j in skills]
    print(skills_proc)
    return render_template('result.html', skills=skills_proc)

if __name__ == '__main__':
    create_sql(path_bd)
    app.run(debug=True)