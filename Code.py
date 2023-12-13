import telebot
from code_separation.UI import *
from code_separation.Datachecker import data_check

bot = telebot.TeleBot("5205782024:AAGWRPiTpr-daEaeUYMNiVXFmdtPYtz98K8")

adding_year = adding_month = adding_day = False


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Здравствуйте, я прототип календарь бота Dateve.")
    bot.send_message(message.chat.id, "Для получения руководства использования нажмите на кнопку 'Команды'",
                     reply_markup=keyboard_start)


@bot.message_handler(content_types=['text'])
def handler(message):
    global adding_year, adding_month, adding_event_year
    text = message.text
    if text == 'Dateve':
        bot.send_message(message.chat.id, "Готов к работе", reply_markup=keyboard_call)
    if adding_year is True:
        adding_event_year = int(text)
        adding_year = False
        adding_month = True
        bot.send_message(message.chat.id, "Теперь выберите месяц", reply_markup=keyboard_months)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global adding_year, adding_month, adding_day, adding_event_month, adding_event_year
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
            bot.send_message(call.message.chat.id, "Дата корректна", reply_markup=keyboard_call)
        else:
            bot.send_message(call.message.chat.id, "Дата некорректна", reply_markup=keyboard_call)
    if adding_month is True and 0 < int(call.data) <= 12:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        adding_event_month = int(call.data)
        adding_month = False
        adding_day = True
        bot.send_message(call.message.chat.id, "Теперь выберите день", reply_markup=keyboard_days)


if __name__ == '__main__':
    bot.polling()
