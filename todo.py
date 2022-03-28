import telebot
from telebot import types
# токен бота
bot = telebot.TeleBot('5104497543:AAEs0LWgdR7L4Ji48tjXIYiNDEAEjBhG7Cg')

# функция для вступления
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Приветствую! Вы попали в квест-лабиринт. "
                                               "Используя бота, вы можете погрузиться в "
                                               "мир удивительных историй и загадок."
                                               " От каждого вашего выбора, зависит судьба персонажа и исход игры.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # клавиатура
        keyboard = types.InlineKeyboardMarkup()
        # кнопка «Да»
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        # добавление кнопки в клавиатуру
        keyboard.add(key_yes)
        markup.add(key_yes)
        # кнопка «Нет»
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        markup.add(key_no)
        question = "Хотите начать?"
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    if message.text != '/help' and message.text != '/start':
        bot.send_message(message.from_user.id, 'Я вас не понимаю( Напишите /help')
    if message.text == '/help':
        bot.send_message(message.from_user.id, 'Функция помощник. Я не могу обработать ваши сообщения. '
                                               'Пожалуйста нажимайте только на те кнопки,'
                                               ' которые вам выводит приложение')

# обработка выбора пользователя
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # call.data это callback_data, которую мы указали при объявлении кнопки
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Поехали')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Пока-пока! Заглядывайте к нам еще)')
    bot.send_message(call.message.chat.id, reply_markup=telebot.types.ReplyKeyboardRemove())

bot.polling()
