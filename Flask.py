from flask import Flask, render_template, request
from hh import Headhunter
from cachetools import cached, TTLCache

URL = 'https://api.hh.ru/vacancies'
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
    position = request.form.get('position worker')
    count_skills = int(request.form.get('skill'))
    skills = request_cash(position, city)[:count_skills]
    summa = sum([i for i,j in skills])
    skills_proc = [(i, j, round(i/summa*100, 1)) for i, j in skills]
    print(skills_proc)
    return render_template('result.html', skills=skills_proc)

if __name__ == '__main__':
    app.run(debug=True)