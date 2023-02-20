import telebot
from telebot import types
import ast
import os

bot = telebot.TeleBot('') #Приватная информация
event = []
ID = []
chat = []
total = 0
replace_event = ''
replace = 0
checking_events_in_one_date = ''
adding = ''
dot = 0
ban_list = []
password = #Приватная информация
password_in_message = 0
admin = 0
stop_ham = 0
number = 0
zumber = 0
idc = 0
sending = ''

data_events = ''

link_events = os.path.abspath("Events.txt")
link_id = os.path.abspath("Chat.txt")

@bot.message_handler(commands = ['start'])

def start_message(message):    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = types.KeyboardButton("Команды")
    second_button = types.KeyboardButton("События")
    keyboard.add(first_button, second_button)
    third_button = types.KeyboardButton("Помощь")
    fourth_button = types.KeyboardButton("Обновление")
    keyboard.add(third_button, fourth_button)
    bot.send_message(message.chat.id, 'Привет, я бот-календарь! Список команд можно получить, написав Команды', reply_markup = keyboard)
    
@bot.message_handler(content_types = ['text'])

def work(message):
    global total
    global dot
    global admin
    global stop_ham
    global number
    global zumber
    global idc
      
    data = open(link_events) 
    data_events = data.read()
    event = ast.literal_eval(data_events)
    data.close()
    total = len(event)
    data = open(link_id) 
    data_events = data.read()
    chat = ast.literal_eval(data_events)
    data.close()
    
    number = 0
    stop_ham = 0
    for number in range (len(ID)):
        adding = str(message.from_user.id) + message.from_user.username
        if (adding != ID[number]):
            idc += 1
    if (idc == len(ID)):        
        adding = str(message.from_user.id) + message.from_user.username
        ID.append(adding)
        idc = 0
    number = 0
    for ban in range(len(ban_list)):
        text = ban_list[ban]
        while (stop_ham == 0):            
            if (text[number] == ' '):
                banning = int(text[:number])
                stop_ham = 1                        
            number += 1
        if (banning == message.from_user.id):
            bot.send_message(message.chat.id,"Вы забанены из-за %s" % text[number+1:])
            text = ' '
    number = 0
    stop_ham = 0
    text = message.text
    
##------------------------------Проверка на вызов бота и последующее добавление в список------------------------------
    
    if (text[:2] == '+ ' and text[3] == '.' and len(text)>11 or text[:2] == '+ ' and text[4] == '.' and len(text)>11):            
        text = text[2:]           
        for number in range(len(text)):
            if (text[number] == ' ' and dot == 2):
                year = text[:number]
                year = year[dotan+1:]
                dot += 1
                year = int(year)
            if (text[number] == '.' and dot == 1):
                month = text[:number]
                month = month[dotka+1:]
                dotan = number
                dot += 1
                month = int(month)
            if (text[number] == '.' and dot == 0):
                date = text[:number]
                dotka = number
                dot += 1
                date = int(date)
        dot = 0
        dotka = 0
        dotan = 0
        number = 0
        if (year >= 0):
            if (0 < month <= 12):
                if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
                    if (0 < date <= 31):
                        event.append(text)
                        event[total] = event[total] + ' ' + (message.from_user.username)
                        total += 1
                        chat.append(message.chat.id)
                        data = open(link_events, 'w')
                        data_events = str(event)
                        data.write(data_events)
                        data.close()
                        data = open(link_id, 'w')
                        data_events = str(chat)
                        data.write(data_events)
                        data.close()
                    else:
                        bot.send_message(message.chat.id, 'Некорректная дата')
                        text = ' '
                elif (month == 4 or month == 6 or month == 9 or month == 11):
                    if (0 < date <= 30):
                        event.append(text)
                        event[total] = event[total] + ' ' + (message.from_user.username)
                        total += 1
                        chat.append(message.chat.id)
                        data = open(link_events, 'w')
                        data_events = str(event)
                        data.write(data_events)
                        data.close()
                        data = open(link_id, 'w')
                        data_events = str(chat)
                        data.write(data_events)
                        data.close()
                    else:
                        bot.send_message(message.chat.id, 'Некорректная дата')
                        text = ' '
                elif (month == 2):
                    if (0 < date <= 28):
                        event.append(text)
                        event[total] = event[total] + ' ' + (message.from_user.username)
                        total += 1
                        chat.append(message.chat.id)
                        data = open(link_events, 'w')
                        data_events = str(event)
                        data.write(data_events)
                        data.close()
                        data = open(link_id, 'w')
                        data_events = str(chat)
                        data.write(data_events)
                        data.close()
                    else:
                        bot.send_message(message.chat.id, 'Некорректная дата')
                        text = ' '
            else:
                bot.send_message(message.chat.id, 'Некорректная дата')
                text = ' '
        else:
            bot.send_message(message.chat.id, 'Некорректная дата')
            text = ' '       

##------------------------------Полный вывод событий с сортировкой по дате------------------------------
    
    if (text == 'События' or text == 'события'):
        for i in range(total - 1):
            for i in range(total - 1):
                first_event_to_change = event[i]                
                second_event_to_change = event[i+1]
                
                for z in range(len(first_event_to_change)):
                    if (first_event_to_change[z] == ' ' and dot == 2):
                        first_year_to_change = first_event_to_change[:z]
                        first_year_to_change = first_year_to_change[dotan+1:]
                        dot += 1
                        first_year_to_change = int(first_year_to_change)
                    if (first_event_to_change[z] == '.' and dot == 1):
                        first_month_to_change = first_event_to_change[:z]
                        first_month_to_change = first_month_to_change[dotka+1:]
                        dotan = z
                        dot += 1
                        first_month_to_change = int(first_month_to_change)
                    if (first_event_to_change[z] == '.' and dot == 0):
                        first_date_to_change = first_event_to_change[:z]
                        dotka = z
                        dot += 1
                        first_date_to_change = int(first_date_to_change)
                    
                z = 0
                dot = 0
                dotka = 0
                dotan = 0

                for z in range(len(second_event_to_change)):
                    if (second_event_to_change[z] == ' ' and dot == 2):
                        second_year_to_change = second_event_to_change[:z]
                        second_year_to_change = second_year_to_change[dotan+1:]
                        dot += 1
                        second_year_to_change = int(second_year_to_change)
                    if (second_event_to_change[z] == '.' and dot == 1):
                        second_month_to_change = second_event_to_change[:z]
                        second_month_to_change = second_month_to_change[dotka+1:]
                        dotan = z
                        dot += 1
                        second_month_to_change = int(second_month_to_change)
                    if (second_event_to_change[z] == '.' and dot == 0):
                        second_date_to_change = second_event_to_change[:z]
                        dotka = z
                        dot += 1
                        second_date_to_change = int(second_date_to_change)

                z = 0
                dot = 0
                dotka = 0
                dotan = 0
                        
                if (first_year_to_change > second_year_to_change):
                    replace_event = event[i]
                    event[i] = event[i+1]
                    event[i+1] = replace_event
                    replace = chat[i]
                    chat[i] = chat[i+1]
                    chat[i+1] = replace
                elif (first_month_to_change > second_month_to_change and first_year_to_change == second_year_to_change):
                    replace_event = event[i]
                    event[i] = event[i+1]
                    event[i+1] = replace_event
                    replace = chat[i]
                    chat[i] = chat[i+1]
                    chat[i+1] = replace
                elif (first_date_to_change > second_date_to_change and first_month_to_change == second_month_to_change and first_year_to_change == second_year_to_change):
                    replace_event = event[i]
                    event[i] = event[i+1]
                    event[i+1] = replace_event
                    replace = chat[i]
                    chat[i] = chat[i+1]
                    chat[i+1] = replace
        for i in range(total):
            if (message.chat.id == chat[i] and admin == 0):
                while (stop_ham == 0):
                    sending = event[i]
                    number += 1
                    if (sending[len(sending)-number] == ' '):
                        stop_ham = 1
                        sending = sending[:len(sending) - number]                        
                bot.send_message(message.chat.id, sending)
                stop_ham = 0
                number = 0
            elif (admin == 1):
                bot.send_message(message.chat.id, event[i])

##------------------------------Вывод события за определённую дату------------------------------
    
    elif (text[:10] == 'События за'):
        for i in range(total):            
            checking_events_in_one_date = event[i]
            checking_events_in_one_date = str(checking_events_in_one_date)
            while (stop_ham == 0):
                number += 1
                if (checking_events_in_one_date[number] == ' ' and stop_ham == 0):
                    checking_events_in_one_date = checking_events_in_one_date[:number]
                    stop_ham = 1
            number = 0
            stop_ham = 0
            if (checking_events_in_one_date == text[11:] and admin == 0 and chat[i] == message.chat.id):
                checking_events_in_one_date = event[i]
                checking_events_in_one_date = str(checking_events_in_one_date)
                while (stop_ham == 0):
                    number += 1
                    if (checking_events_in_one_date[len(checking_events_in_one_date)-number] == ' '):
                        stop_ham = 1
                        checking_events_in_one_date = checking_events_in_one_date[:len(checking_events_in_one_date) - number] 
                bot.send_message(message.chat.id, checking_events_in_one_date)
            elif (checking_events_in_one_date == text[11:] and admin == 1):
                checking_events_in_one_date = event[i]
                checking_events_in_one_date = str(checking_events_in_one_date)               
                bot.send_message(message.chat.id, checking_events_in_one_date)

##------------------------------Команды------------------------------
    
    elif (text == 'Команды' and admin == 0 or text == 'команды' and admin == 0):
        bot.send_message(message.chat.id,'Чтобы добавить событие, надо ввести + затем дату и событие. Например + 01.01.2000 Поздравить всех с новым годом.')
        bot.send_message(message.chat.id,'Команда События выведет все существующие события сортируя их по датам.')
        bot.send_message(message.chat.id,'Чтобы узнать события в определённый день, введите команду События за и дату. Например События за 01.01.2000.')
        bot.send_message(message.chat.id,'Команда Обновление выдаст все изменения, введённые последним обновлением.')
    elif (text == 'Команды' and admin == 1 or text == 'команды' and admin == 1):
        bot.send_message(message.chat.id,'Панель админа и пароль включает или выключает полный доступ к базе данных.')
        bot.send_message(message.chat.id,'Бан + и айди пользователя позволяют забанить самого пользователя.')

##------------------------------Бан------------------------------
    
    elif (text[:5] == 'Бан +' and admin == 1):
        text = message.text[6:]
        while (stop_ham == 0):
            number += 1
            if(text[number] == ' '):
                stop_ham = 1
            
        ban_list.append(text[:number] + ' ' + text[number:])

##------------------------------Разбан------------------------------
    
    elif (text[:5] == 'Бан -' and admin == 1):
        number = 0
        for number in range(len(ban_list)):
            text = ban_list[number]
            zumber = 0
            stop_ham = 0
            while (stop_ham == 0):
                zumber += 1
                if (text[zumber] == ' '):
                    stop_ham = 1
            text = text[:zumber]
            if (message.text[6:] == text):
                del ban_list[number]
                
##------------------------------Айди------------------------------
    
    elif (text[:4] == 'Айди' and admin == 1):
        for i in range(len(ID)):            
            bot.send_message(message.chat.id, ID[i])
        
##------------------------------Панель админа------------------------------
    
    elif (text[:13] == 'Панель админа'):
        password_in_message = int(text[14:])        
        if (password_in_message == password):
            if (admin == 0):
                admin = 1
            else:
                admin = 0

##------------------------------Обновление------------------------------
    
    elif (text == 'Обновление' or text == 'обновление'):
        bot.send_message(message.chat.id,'Последняя дата обновления - 03.04.2022.')
        
##------------------------------Помощь------------------------------
    
    elif (text == 'Помощь' and text == 'помощь'):
        bot.send_message(message.chat.id,'В разработке.')
        
bot.polling()
