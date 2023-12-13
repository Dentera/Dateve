from telebot import types

command_button = types.InlineKeyboardButton('Команды', callback_data='commands')
add_button = types.InlineKeyboardButton('Добавить событие', callback_data='add_event')
main_button = types.InlineKeyboardButton('Dateve', callback_data='main')

keyboard_main = types.InlineKeyboardMarkup(row_width=2)
keyboard_call = types.InlineKeyboardMarkup(row_width=2)
keyboard_start = types.InlineKeyboardMarkup(row_width=2)
keyboard_days = types.InlineKeyboardMarkup(row_width=3)
keyboard_months = types.InlineKeyboardMarkup(row_width=3)

for month in range(1, 12, 3):
    keyboard_months.add(types.InlineKeyboardButton(month, callback_data=month),
                        types.InlineKeyboardButton(month + 1, callback_data=month + 1),
                        types.InlineKeyboardButton(month + 2, callback_data=month + 2))

for day in range(1, 30, 3):
    keyboard_days.add(types.InlineKeyboardButton(day, callback_data=day),
                      types.InlineKeyboardButton(day + 1, callback_data=day + 1),
                      types.InlineKeyboardButton(day + 2, callback_data=day + 2))
    if day == 28:
        keyboard_days.add(types.InlineKeyboardButton(31, callback_data=31))

keyboard_main.add(add_button, command_button)
keyboard_call.add(main_button)
keyboard_start.add(command_button)
