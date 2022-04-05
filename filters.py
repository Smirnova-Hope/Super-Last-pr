import telebot
from telebot import types
import sqlite3
from random import randint

# токен бота
bot = telebot.TeleBot('5211894904:AAFbuovu8W1VefPHBOffusDFwSppYqjB_0Q')
# count_button, для того чтобы обрабатывать только один выбор и только один раз
count_button = 0
rand_id = randint(1, 10)

con = sqlite3.connect("base 3.db")
cur = con.cursor()

# функция для вступления
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/ready':
        bot.register_next_step_handler(message, time)
    if message.text == '/start':
        global count_button
        count_button = 0
        bot.send_message(message.from_user.id, "Приветствую! Вы попали в квест-лабиринт. "
                                               "Используя бота, вы можете погрузиться в "
                                               "мир удивительных историй и загадок."
                                               " От каждого вашего выбора, зависит судьба персонажа и исход игры.")
        # клавиатура
        keyboard = types.InlineKeyboardMarkup()
        # кнопка «Да»
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        # добавление кнопки в клавиатуру
        keyboard.add(key_yes)
        # кнопка «Нет»
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = "Хотите начать?"
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    if message.text == '/ready':
        message = bot.send_message(message.chat.id,'Поехали')
        bot.register_next_step_handler(message, time)
    if message.text != '/help' and message.text != '/start' and message.text != '/ready':
        bot.send_message(message.from_user.id, 'Я вас не понимаю( Напишите /help')
    if message.text == '/help':
        bot.send_message(message.from_user.id, 'Функция помощник. Я не могу обработать ваши сообщения. '
                                               'Пожалуйста нажимайте только на те кнопки,'
                                               ' которые вам выводит приложение')


# обработка выбора пользователя
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # call.data это callback_data, которую мы указали при объявлении кнопки
    global count_button
    if call.data == "yes" and count_button == 0:
        count_button += 1
        bot.send_message(call.message.chat.id, 'Поехали',
                         reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')
        message = bot.send_message(call.message.chat.id, 'О! Вижу вы решили попытаться пройти квест. Удачи. Для начала выберите'
                                   'время действий. Напишите /ready.')
        bot.register_next_step_handler(message, time)

    if call.data == "no" and count_button == 0:
        count_button += 1
        bot.send_message(call.message.chat.id, 'Пока-пока! Заглядывайте к нам еще)',
                         reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')

    if call.data == "y" and count_button == 1:
        count_button += 1
        bot.send_message(call.message.chat.id, '''3100 год от Рождества Христово. Галактика Андромеды.
Планета «NL-31» - ближайшая планета с климатом пригодным для жизни. Человеческая раса перебралась
жить на эту планету из-за разрушения ядра планеты Земля. Время на планете «NL-31» течет в 2 раза
медленнее земного, а вместо Солнца – звезда «Мабу».''')
        bot.send_message(call.message.chat.id, f'''Сегодня день Вашего рождения. 
Ваше имя - {cur.execute(f'SELECT name FROM user WHERE id={rand_id}')}, Ваша удача - {cur.execute(f'SELECT luck FROM user WHERE id={rand_id}')}, 
Ваш авторитет- {cur.execute(f'SELECT authority FROM user WHERE id={rand_id}')}, 
Ваше здоровье - {cur.execute(f'SELECT health FROM user WHERE id={rand_id}')}''')


def time(message):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка «Будущее»
    key_future = types.InlineKeyboardButton(text='Будущее!', callback_data='y')
    # добавление кнопки в клавиатуру
    keyboard.add(key_future)
    # кнопка «Прошлое»
    key_ancient = types.InlineKeyboardButton(text='Прошлое!', callback_data='n')
    keyboard.add(key_ancient)
    question = "Сетинг квеста:"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)




bot.polling()
