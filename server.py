# simple chat

from flask import Flask, request, render_template
from datetime import datetime
import time
import json

app = Flask(__name__)  # создание приложения

messages_file = open('./data/messages.json', 'r', encoding='utf-8')
data = json.load(messages_file)
messages_file.close()

if 'all_messages' not in data:
    print(f'Cant find all_messages in {messages_file}')
    exit(1)

all_messages = data['all_messages']  # загружаем json-данные и берем список "all_messages"
print(all_messages)


def save_messages():
    """Функция перезаписи файла json с новыми сообщениями"""
    data_messages = {'all_messages': all_messages}
    json_f = open('./data/messages.json', 'w', encoding='utf-8')  # открываем файл для записи
    json.dump(data_messages, json_f)  # пишем стуктуру в файл


def time_format(t):  # вместо этой функции можно использовать стандартную datetime.now()
    """Функция конвертирует нечитаемый формат времени в привычный"""
    return str(datetime.fromtimestamp(t))


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/get_messages")  # GET — запрос на чтение данных
def get_messages():
    return {"messages": all_messages}


@app.route("/")
def root():
    return "Hello everyone! Please print in address bar: - '/get_messages' - to get all messages from our chat; - " \
           "'/chat' - to join to our chat."


@app.route("/send")
def send_message():
    text = request.args["text"]
    name = request.args["name"]

    if 3 <= len(name) <= 100 and 1 <= len(text) <= 100:
        message = {
            "text": text,
            "name": name,
            # 'time': str(datetime.now())
            "time": time_format(time.time()),
        }
        all_messages.append(message)
        save_messages()
        # или вместо функции save_messages() использовать код сразу в этом месте:
        # all_messages.append(message)
        # data_messages = {'all_messages': all_messages}
        # new_messages_file = open('./data/messages.json', 'w', encoding='utf-8')
        # json.dump(data_messages, new_messages_file)
        return 'OK'

    else:
        return 'ERROR'


app.run()  # запуск приложения
