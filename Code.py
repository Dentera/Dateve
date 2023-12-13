import telebot  # Подключение библиотеки pyTelegramBotAPI.
import datetime  # Подключение библиотеки DateTime.
import sqlite3  # Подключение библиотеки SQLite3.
from code_separation.UI import *  # Подключение всех модулей из файла UI, который в папке code_separation.
from code_separation.Datachecker import data_check \
    # Подключение функции data_check из файла, который в папке code_separation.

bot = telebot.TeleBot("5205782024:AAHX0lbe_qQttERiBl3Wx4otcSnqCQMHW4k")  \
    # Подключение токена телеграм-бота для работы самим ботом.

adding_year = adding_month = adding_day = adding_event = delete_message = False \
    # Создание переменных типа bool, для ввода даты.
adding_event_year = adding_event_month = adding_event_day = int() \
    # Создание переменных типа integer, для сохранения числовых значений года/месяца/дня.
out = list()

db = sqlite3.connect("database/Data.db", check_same_thread=False)  \
    # Создание переменной db, содержащей в себе ссылку на базу данных Data с включённой многопоточностью.
cursor = db.cursor()  # Создание переменной cursor для работы с базой данных.


def db_add(chat_id, event_day, event):  # Создание функции db_add, принимающей значения chat_id, event_day и event.
    cursor.execute(""" INSERT INTO events(chatID, event_day, event)
    VALUES(?, ?, ?)""", (chat_id, event_day, event))  # Запись значений chat_id, event_day и event в базу данных.


@bot.message_handler(commands=["start"])  # Реакция бота на сообщение /start.
def start(message):  # Создание функции start, принимающей сообщение пользователя в чате.
    bot.send_message(message.chat.id, "Здравствуйте, я прототип календарь бота Dateve.")  \
        # Отправление приветственного сообщения бота в чат.
    bot.send_message(message.chat.id, "Для получения руководства пользования мной нажмите на кнопку <Команды>",
                     reply_markup=keyboard_start)  # Отправление координирующего сообщения бота в чат.


@bot.message_handler(content_types=["text"])  # Реакция бота на текст в чате.
def work(message):  # Создание функции work, принимающей сообщение пользователя в чате.
    global adding_year, adding_month, adding_event, adding_event_year, adding_event_month, adding_event_day, \
        delete_message  # Объявление вышеописанных переменных глобальными.
    text = message.text  # Создаётся переменная text, обрабатывающая каждое сообщение в чате.
    if text == "Dateve":  # Если в чате появляется сообщение Dateve, то выполняется условие.
        bot.send_message(message.chat.id, "Готов к работе.", reply_markup=keyboard_call)  \
            # При выполнении условия бот отправляет сообщение с прикреплённой клавиатурой взаимодействия.
    if adding_year is True:
        adding_event_year = int(text)
        adding_year = False
        adding_month = True
        bot.send_message(message.chat.id, "Теперь выберите месяц:", reply_markup=keyboard_months)
    if adding_event is True:
        adding_event = False
        event_to_db = str(text)
        date = str(datetime.date(adding_event_year, adding_event_month, adding_event_day)).replace('-', '.')
        db_add(message.chat.id, date, event_to_db)
        db.commit()
        bot.send_message(message.chat.id, "Событие сохранено.", reply_markup=keyboard_call)
    if delete_message is True:
        delete_message = False
        correct_message = int(text)
        for i in range(len(out)):
            if correct_message == (i+1):
                cursor.execute("""DELETE FROM events WHERE chatID = ? AND event = ? AND event_day = ?""",
                               (message.chat.id, out[i][0], out[i][1]))
                db.commit()
                bot.send_message(message.chat.id, "Событие удалено.", reply_markup=keyboard_call)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global adding_year, adding_month, adding_day, adding_event, adding_event_month, adding_event_year, \
        adding_event_day, out, delete_message
    if call.data == "commands":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Dateve - предоставляет пользователю полный комплект команд бота.\n"
                                               "Добавить событие - начинает цепочку действий для добавления нового "
                                               "события.\n"
                                               "Вывести события - выводит в чат все события, добавленные в этом чате.\n"
                                               "Команды - выводит в чат список команд бота.\n"
                                               "Удалить событие можно после вывода всех событий.\n"
                                               "Год события может быть от 1 до 9999.\n"
                                               "Приятного использования!",
                         reply_markup=keyboard_call)
    if call.data == "main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Выберите команду:", reply_markup=keyboard_main)
    if call.data == "add_event":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Введите год события, которое вы добавляете:")
        adding_year = True
    if adding_day is True and 0 < int(call.data) <= 31:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        adding_event_day = int(call.data)
        adding_day = False
        if data_check(adding_event_year, adding_event_month, adding_event_day) is True:
            bot.send_message(call.message.chat.id, "Дата корректна. Нажмите <Записать событие> и введите событие.",
                             reply_markup=keyboard_add_event)
        else:
            bot.send_message(call.message.chat.id, "Дата некорректна. Попробуйте заново.", reply_markup=keyboard_call)
    if adding_month is True and 0 < int(call.data) <= 12:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        adding_event_month = int(call.data)
        adding_month = False
        adding_day = True
        bot.send_message(call.message.chat.id, "Теперь выберите день:", reply_markup=keyboard_days)
    if call.data == "event":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Теперь введите событие:")
        adding_event = True
    if call.data == "output":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        out = cursor.execute("""SELECT event,event_day FROM events WHERE chatID = (?)""",
                             (call.message.chat.id,)).fetchall()
        if len(out) > 0:
            bot.send_message(call.message.chat.id, "Вывод событий:", reply_markup=keyboard_delete)
            for x in range(len(out) - 1):
                for y in range(len(out) - x - 1):
                    if out[y][1] > out[y + 1][1]:
                        out[y], out[y + 1] = out[y + 1], out[y]
            for i in range(len(out)):
                send = ' '.join(out[i])
                bot.send_message(call.message.chat.id, send)
        else:
            bot.send_message(call.message.chat.id, "Сохранённых событий в этом чате нет.", reply_markup=keyboard_call)
    if call.data == "delete":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Какое событие вы хотите удалить?")
        for i in range(len(out)):
            send = ' '.join(out[i])
            bot.send_message(call.message.chat.id, "[" + str(i+1) + "]" + " " + send)
        delete_message = True


if __name__ == "__main__":  # Запуск нижеописанного кода при запуске программы.
    bot.polling()  # Проверяет бота на получение запросов.
