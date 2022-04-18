import telebot
from jjj import get_map_cell

bot = telebot.TeleBot('zzzzzzzzzzzzz')
cols, rows = 8, 8
maps = {}

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row( telebot.types.InlineKeyboardButton('←', callback_data='left'),
              telebot.types.InlineKeyboardButton('↑', callback_data='up'),
              telebot.types.InlineKeyboardButton('↓', callback_data='down'),
              telebot.types.InlineKeyboardButton('→', callback_data='right'))

def get_map_str(map_cell, player):
    map_str = ''
    for y in range(rows * 2 - 1):
        for x in range(cols * 2 - 1):
            if map_cell[x + y * (cols * 2 - 1)]:
                map_str += "⬛"
            elif (x, y) == player:
                map_str += "🔴"
            else:
                map_str += "⬜"
        map_str += '\n'
    return map_str


@bot.message_handler(commands=['play'])
def play(message):
    map_cell = get_map_cell(cols, rows)
    user_data = {
        'map': map_cell,
        'x': 0,
        'y': 0
    }
    maps[message.chat.id] = user_data
    bot.send_message(message.from_user.id, get_map_str(map_cell, (0, 0)), reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    user_data = maps[query.message.chat.id]
    n_x, n_y = user_data['x'], user_data['y']
    if query.data == 'left':
        n_x -= 1
    if query.data == 'right':
        n_x += 1
    if query.data == 'up':
        n_y -= 1
    if query.data == 'down':
        n_y += 1

    if n_x < 0 or n_x > 2 * cols - 2 or n_y < 0 or n_y > rows * 2 - 2:
        return None
    if user_data['map'][n_x + n_y * (cols * 2 - 1)]:
        return None

    if n_x == cols * 2 - 2 and n_y == rows * 2 - 2:
        bot.edit_message_text(chat_id=query.message.chat.id,
                              message_id=query.chat.id,
                              text="Вы выиграли",
                              reply_markup=keyboard)
        return None
    user_data['x'], user_data['y'] = n_x, n_y
    bot.edit_message_text(chat_id=query.message.chat.id,
                          message_id=query.chat.id,
                          text=get_map_str(user_data['map'], (n_x, n_y)),
                          reply_markup=keyboard)

bot.polling(none_stop=False, interval=0)
