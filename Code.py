import telebot  # Подключение библиотеки pyTelegramBotAPI.
import datetime  # Подключение библиотеки DateTime.
import sqlite3  # Подключение библиотеки SQLite3.
from code_separation.UI import *  # Подключение всех модулей из файла UI, который в папке code_separation.
from code_separation.Datachecker import data_check \
    # Подключение функции data_check из файла, который в папке code_separation.

bot = telebot.TeleBot("")  \
    # Подключение токена телеграм-бота для работы самим ботом.

adding_year = adding_month = adding_day = adding_event = False \
    # Создание переменных типа bool, для ввода даты.
adding_event_year = adding_event_month = adding_event_day = int() \
    # Создание переменных типа integer, для сохранения числовых значений года/месяца/дня.

db = sqlite3.connect("database/Data.db", check_same_thread=False)  \
    # Создание переменной db, содержащей в себе ссылку на базу данных Data с включённой многопоточностью.
cursor = db.cursor()  # Создание переменной cursor для работы с базой данных.


def db_add(chat_id, event_day, event):
    cursor.execute(""" INSERT INTO events(chatID, event_day, event)
    VALUES(?, ?, ?)""", (chat_id, event_day, event))


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Здравствуйте, я прототип календарь бота Dateve.")
    bot.send_message(message.chat.id, "Для получения руководства использования нажмите на кнопку 'Команды'",
                     reply_markup=keyboard_start)


@bot.message_handler(content_types=["text"])
def handler(message):
    global adding_year, adding_month, adding_event, adding_event_year, adding_event_month, adding_event_day
    text = message.text
    if text == "Dateve":
        bot.send_message(message.chat.id, "Готов к работе", reply_markup=keyboard_call)
    if adding_year is True:
        adding_event_year = int(text)
        adding_year = False
        adding_month = True
        bot.send_message(message.chat.id, "Теперь выберите месяц", reply_markup=keyboard_months)
    if adding_event is True:
        adding_event = False
        event_to_db = str(text)
        date = str(datetime.date(adding_event_year, adding_event_month, adding_event_day)).replace('-', '.')
        db_add(message.chat.id, date, event_to_db)
        db.commit()
        bot.send_message(message.chat.id, "Событие сохранено", reply_markup=keyboard_call)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global adding_year, adding_month, adding_day, adding_event, adding_event_month, adding_event_year, adding_event_day
    if call.data == "commands":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Ввести событие\nDateve",
                         reply_markup=keyboard_call)
    if call.data == "main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Выберите команду", reply_markup=keyboard_main)
    if call.data == "add_event":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Введите год")
        adding_year = True
    if adding_day is True and 0 < int(call.data) <= 31:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        adding_event_day = int(call.data)
        adding_day = False
        if data_check(adding_event_year, adding_event_month, adding_event_day) is True:
            bot.send_message(call.message.chat.id, "Дата корректна", reply_markup=keyboard_add_event)
        else:
            bot.send_message(call.message.chat.id, "Дата некорректна", reply_markup=keyboard_call)
    if adding_month is True and 0 < int(call.data) <= 12:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        adding_event_month = int(call.data)
        adding_month = False
        adding_day = True
        bot.send_message(call.message.chat.id, "Теперь выберите день", reply_markup=keyboard_days)
    if call.data == "event":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Теперь напишите событие")
        adding_event = True
    if call.data == "output":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        out = cursor.execute("""SELECT event,event_day FROM events WHERE chatID = (?)""",
                             (call.message.chat.id,)).fetchall()
        if len(out) > 0:
            bot.send_message(call.message.chat.id, "Вывод событий:", reply_markup=keyboard_call)
            for x in range(len(out) - 1):
                for y in range(len(out) - x - 1):
                    if out[y][1] > out[y + 1][1]:
                        out[y], out[y + 1] = out[y + 1], out[y]
            for i in range(len(out)):
                send = ' '.join(out[i])
                bot.send_message(call.message.chat.id, send)
        else:
            bot.send_message(call.message.chat.id, "Сохранённых событий в этом чате нет", reply_markup=keyboard_call)


if __name__ == "__main__":
    bot.polling()
