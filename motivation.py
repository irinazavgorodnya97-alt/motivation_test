from flask import Flask, render_template_string, request, redirect, url_for
import csv
from datetime import datetime
import os

app = Flask(__name__)

# 12 вопросов
questions = [
    "Вопрос 1: Мне нравится учиться",
    "Вопрос 2: Я стараюсь выполнять все задания",
    "Вопрос 3: Я хочу получать хорошие оценки",
    "Вопрос 4: Мне интересно узнавать новое",
    "Вопрос 5: Я хочу участвовать в олимпиадах и конкурсах",
    "Вопрос 6: Я легко нахожу общий язык с учителем",
    "Вопрос 7: Мне нравится работать в группе",
    "Вопрос 8: Я люблю планировать своё время",
    "Вопрос 9: Я стараюсь помогать одноклассникам",
    "Вопрос 10: Я хочу получать новые знания и навыки",
    "Вопрос 11: Я стараюсь выполнять домашние задания вовремя",
    "Вопрос 12: Мне важно достигать поставленных целей"
]

# Шаблон выбора класса
class_template = '''
<h2 style="color: #2F4F4F;">Выберите ваш класс</h2>
<form method="post">
  <select name="class" style="font-size: 16px; padding: 5px;">
    <option value="5А">5А</option>
    <option value="5Б">5Б</option>
    <option value="6А">6А</option>
    <option value="6Б">6Б</option>
    <option value="7А">7А</option>
    <option value="7Б">7Б</option>
    <option value="8А">8А</option>
    <option value="8Б">8Б</option>
    <option value="9А">9А</option>
    <option value="9Б">9Б</option>
    <option value="10">10</option>
    <option value="11">11</option>
  </select>
  

  <input type="submit" value="Далее" style="padding: 5px 15px; font-size: 16px;">
</form>
'''

# Шаблон ввода ФИО
name_template = '''
<h2 style="color: #2F4F4F;">Введите свои данные</h2>
<form method="post">
  <input type="text" name="first_name" placeholder="Имя" required style="font-size:16px; padding:5px;">

  <input type="text" name="last_name" placeholder="Фамилия" required style="font-size:16px; padding:5px;">

  <input type="submit" value="Далее" style="padding: 5px 15px; font-size: 16px;">
</form>
'''

# Шаблон теста
test_template = '''
<h2 style="color: #2F4F4F;">Тест на мотивацию к учёбе</h2>
<form method="post">
  {% for i, q in enumerate(questions) %}
    <p style="font-size:16px;">{{q}}</p>
    <input type="radio" name="q{{i}}" value="Да" required>Да
    <input type="radio" name="q{{i}}" value="Иногда">Иногда
    <input type="radio" name="q{{i}}" value="Нет">Нет
    

  {% endfor %}
  <input type="submit" value="Отправить" style="padding:5px 15px; font-size:16px;">
</form>
'''

# Сообщение если тест уже пройден
already_done_template = '''
<h2 style="color:red;">Вы уже проходили этот тест!</h2>
'''

# Маршрут: выбор класса
@app.route("/", methods=["GET", "POST"])
def select_class():
    if request.method == "POST":
        selected_class = request.form["class"]
        return redirect(url_for("enter_name", selected_class=selected_class))
    return render_template_string(class_template)

# Маршрут: ввод ФИО
@app.route("/name", methods=["GET", "POST"])
def enter_name():
    selected_class = request.args.get("selected_class")
    if request.method == "POST":
        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        
        # Проверка, прошёл ли уже ученик тест
        if os.path.exists("results.csv"):
            with open("results.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["Класс"] == selected_class and row["Имя"] == first_name and row["Фамилия"] == last_name:
                        return render_template_string(already_done_template)
        
        return redirect(url_for("take_test", selected_class=selected_class,
                                first_name=first_name, last_name=last_name))
    return render_template_string(name_template)

# Маршрут: тест
@app.route("/test", methods=["GET", "POST"])
def take_test():
    selected_class = request.args.get("selected_class")
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name"


)
    if request.method == "POST":
        # собираем ответы
        answers = [request.form[f"q{i}"] for i in range(len(questions))]
        
        # сохраняем в CSV
        file_exists = os.path.exists("results.csv")
        with open("results.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # если файл новый, добавляем заголовки
            if not file_exists:
                header = ["Дата", "Класс", "Имя", "Фамилия"] + [f"Вопрос {i+1}" for i in range(len(questions))]
                writer.writerow(header)
            row = [datetime.now().strftime("%Y-%m-%d %H:%M"), selected_class, first_name, last_name] + answers
            writer.writerow(row)
        return "<h2 style='color:green;'>Спасибо! Ваши ответы сохранены.</h2>"
    
    return render_template_string(test_template, questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
)
    if request.method == "POST":
        # собираем ответы
        answers = [request.form[f"q{i}"] for i in range(len(questions))]
        
        # сохраняем в CSV
        file_exists = os.path.exists("results.csv")
        with open("results.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # если файл новый, добавляем заголовки
            if not file_exists:
                header = ["Дата", "Класс", "Имя", "Фамилия"] + [f"Вопрос {i+1}" for i in range(len(questions))]
                writer.writerow(header)
            row = [datetime.now().strftime("%Y-%m-%d %H:%M"), selected_class, first_name, last_name] + answers
            writer.writerow(row)
        return "<h2 style='color:green;'>Спасибо! Ваши ответы сохранены.</h2>"
    
    return render_template_string(test_template, questions=questions)

if __name__ == "__main__":
    app.run(debug=True)