import telebot
from telebot import types
import sqlite3
from random import randint

# токен бота
bot = telebot.TeleBot('5211894904:AAFbuovu8W1VefPHBOffusDFwSppYqjB_0Q')
# count_button, для того чтобы обрабатывать 1 нажатие кнопки
count_button = 0

# случайное id  для будущего
rand_id1 = randint(1, 10)

# случайное id для прошлого
rand_id2 = randint(1, 10)
try:
    con = sqlite3.connect("base 3.db")
    cur = con.cursor()
    # запросы нужных переменных для кто убил Марка из бд
    name1 = (cur.execute(f'SELECT name FROM user WHERE id={rand_id1}').fetchall()[0][0])
    luck1 = (cur.execute(f'SELECT luck FROM user WHERE id={rand_id1}').fetchall()[0][0])
    authority1 = (cur.execute(f'SELECT authority FROM user WHERE id={rand_id1}').fetchall()[0][0])
    health1 = (cur.execute(f'SELECT health FROM user WHERE id={rand_id1}').fetchall()[0][0])
    # запросы нужных переменных для прошлого из бд
    name2 = (cur.execute(f'SELECT name FROM user WHERE id={rand_id2}').fetchall()[0][0])
    luck2 = (cur.execute(f'SELECT luck FROM user WHERE id={rand_id2}').fetchall()[0][0])
    authority2 = (cur.execute(f'SELECT authority FROM user WHERE id={rand_id2}').fetchall()[0][0])
    health2 = (cur.execute(f'SELECT health FROM user WHERE id={rand_id2}').fetchall()[0][0])
except:
    name1 = 'Никита'
    luck1 = 1
    authority1 = 1
    health1 = 4
    # запросы нужных переменных для прошлого из бд
    name2 = 'Бобрыня'
    luck2 = 3
    authority2 = 3
    health2 = 5

# наличие заточки
weapon = 0

# правильные ответы
well = 0

# наличие или отсутствие друга попугая
friend_parrot = 0
# Наличие или отсутствие ножа
knife = 0
# отношения с остальными жертвами
friends = 0

@bot.message_handler(content_types=['audio', 'document', 'sticker', 'video', 'voice', 'contact', 'first_name', 'last_name'
                                    'id', 'username', 'forward_from', 'video_note', 'game', 'photo', 'dice', 'poll', 'location'
                                    'venue', 'forward_from_chat', 'forward_from_message_id', 'forward_signature', 'forward_date'
                                    'is_automatic_forward', 'reply_to_message', 'animation'])
def fefefe(message):
    bot.send_message(message.from_user.id, 'Некорректные действия. Используйте бота по назначению!')


# функция для вступления
@bot.message_handler(content_types=['text'])
def start(message):
    global count_button
    global well
    if message.text == '/start':
        count_button = 0
        well = 0
        bot.send_message(message.from_user.id, "Приветствую! Вы попали в квест-лабиринт. "
                                               "Используя бота, вы можете погрузиться в "
                                               "мир удивительных историй и загадок."
                                               "От каждого вашего выбора, зависит судьба персонажа и исход игры."
                                               )
        # клавиатура
        keyboard = types.InlineKeyboardMarkup()
        # кнопка «Да»
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        # добавление кнопки в клавиатуру
        keyboard.add(key_yes)
        # кнопка «Нет»
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = "Начнем?"
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

    if message.text == '/help':
        bot.send_message(message.from_user.id, 'Функция помощник. Я не могу обработать ваши сообщения. '
                                               'Пожалуйста нажимайте только на те кнопки,'
                                               'которые вам выводит приложение')
    # карточка с данными о персонаже для первого сеттинга
    if message.text == '/futCard':
        global luck1
        global authority1
        global health1
        bot.send_message(message.from_user.id, f'''Ваша удача - {luck1}, 
Ваш авторитет- {authority1}, 
Ваше здоровье - {health1}.''')
    # карточка с данными о персонаже для прошлого
    if message.text == '/me':
        global luck2
        global authority2
        global health2
        bot.send_message(message.from_user.id, f''' Ваше имя - {name2},
Ваша удача - {luck2}, 
Ваш авторитет- {authority2}, 
Ваше здоровье - {health2}.''')

    if message.text == '/ready' and count_button == 1:
        ask(message)

    if message.text == '/school' and count_button == 2:
        first_ask_future(message)

    if message.text == '/protest' and count_button == 3:
        protest_ask_future(message)

        # ПРОШЛОЕ эпизод с попугаем
    if message.text == '/save' and count_button == 2:
        last_friend_parrot(message)

    # ПРОШЛОЕ эпизод с кораблем
    if message.text == '/continue' and count_button == 3:
        last_korabl(message)

     # ПРОШЛОЕ эпизод с отравлением
    if message.text == '/drink' and count_button == 3:
        rom(message)

    # ПРОШЛОЕ Высадка на остров Мао
    if message.text == '/bereg' and count_button == 4:
        count_button += 1
        kvest1(message)

     # Прошлое первое испытание, загадки
    if message.text == '/first' and count_button == 6:
        count_button += 1
        maze(message)
    # Прошлое второе испытание, физ.способности
    if message.text == '/second' and count_button == 8:
        count_button += 1
        cheleng(message)
    # Прошлое третье испытание, души
    if message.text == '/third' and count_button == 10:
        count_button += 1
        lasted(message)
    if message.text == '/rezult' and count_button == 13:
        try:
            bot.send_message(message.from_user.id, 'Спасибо за прохождение наших квестов. Ждем вас еще :)'
                                                   ' Просто хорошая песня, для настроения "Bones" Imagine Dragons.')
            audio = open('Bones.mp3', 'rb')
            bot.send_audio(message.chat.id, audio)
        except:
            bot.send_message(message.from_user.id, 'Спасибо за прохождение наших квестов. Ждем вас еще :)')
    if message.text != '/help' and message.text != '/start' and message.text != '/futCard' and message.text != '/ready'\
            and message.text != '/school' and message.text != '/me'\
            and message.text != '/protest' and message.text != '/save' and message.text != '/continue'\
            and message.text != '/drink' and message.text != '/bereg' and message.text != '/first'\
            and message.text != '/second' and message.text != '/third' and message.text != '/rezult'\
            or (message.text == '/ready' and count_button != 1)\
            or (message.text == '/school' and count_button != 2) \
            or (message.text == '/protest' and count_button != 3)\
            or (message.text == '/save' and count_button != 2) \
            or (message.text == '/continue' and count_button != 3)\
            or (message.text == '/drink' and count_button != 3)\
            or (message.text == '/bereg' and count_button != 5)\
            or (message.text == '/first' and count_button != 7)\
            or (message.text == '/second' and count_button != 10)\
            or (message.text == '/third' and count_button != 12)\
            or (message.text == '/rezult' and count_button != 13):
        bot.send_message(message.from_user.id, 'Я вас не понимаю( Напишите /help')


# обработка выбора пользователя
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # call.data это callback_data, которую мы указали при объявлении кнопки
    global count_button
    global health1
    global authority1
    global luck1
    global luck2
    global health2
    global authority2
    # предметы и отношения для ПРОШЛОГО
    global friend_parrot
    global knife
    global well
    # начало
    if call.data == "yes" and count_button == 0:
        count_button += 1
        bot.send_message(call.message.chat.id, 'Поехали',
                         reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')
        bot.send_message(call.message.chat.id, 'О! Вижу вы решили попытаться пройти квест. Удачи. Для начала выберите '
                                               'время действий. Напишите /ready.')

    # завершение
    if call.data == "no" and count_button == 0:
        count_button += 1
        bot.send_message(call.message.chat.id, 'Пока-пока! Заглядывайте к нам еще)',
                         reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')

    # ПРОШЛОЕ
    if call.data == "past" and count_button == 1:
        # характеристики для прошлого
        count_button += 1
        bot.send_message(call.message.chat.id, '''Лучи палящего солнца неприятно светят вам в глаза.
Шум голосов становится все громче. Вы жмуритесь сильнее, в попытках вернуться в сладкое царство морфея.
Но тщетно. Злобная старуха Сафо - хозяйка гостиницы, под чьими окнами вы уснули- окатывает вас ледяной водой. 
Не успев, прийти в себя, вы сталкиваетесь с возмущением хозяйки. "А ка зараза ко мне повадилась!
Проку от тебя ноль. Запомни уже, я тебя давно уволила. Не смей, больше сюда приходить, только портишь вид
моему заведению!!! В следующий раз вылью кипящую смолу!!!" - прокричала вам карга Сафо. Мда...
Судьба у вас не завидная. Хотя кому щас легко? На дворе 675 г. до н.э., Греция, остров Крит. Сильная засуха,
голод, нехватка работы из-за большого количество захваченных рабов. Конечно же, им то платить не надо: 
дал кувшин воды, да яблок штук 7 и ходят себе счастливые.... Ну да ладно, начался новый день, 
а значит надо снова отправляться на поиски новый работы!.''')
        # из бд выводим имя и остальные параметры, соответствующие id
        bot.send_message(call.message.chat.id, f''' Ваша краткая биография.
Имя - {name2}, 
Уровень удачи - {luck2}, 
Авторитет- {authority2}, 
Уровень здоровья - {health2}.
Если хотите посмотреть информацию о себе, то напишите: /me''')
        bot.send_message(call.message.chat.id, '''Вы скитаетесь в поисках работы вот уже несколько часов.
Самая выгодная работа, которую вам предложили, это уборка местной конюшни. 
Однако, по какой-то причине вам она не понравилась... 
Продолжая бродить, вы замечаете попугайчика, который вывихнул 
крыло и запутался в ветках дерева. Напишите /save''')
    try:
        bot.send_photo(call.message.chat.id, open('parot.jpg', 'rb'))
    except:
        pass

    # ПРОШЛОЕ, выбор спасти попугая
    if call.data == "save_parrot" and count_button == 2:
        count_button += 1
        bot.send_message(call.message.chat.id, '''Вы очень добрый человек! Вы спасли попугайчику жизнь. 
Теперь у вас появился верный друг и прибавилось уважение остальных! Однако во время спасения, вы грохнулись с дерева.
Повезло, что отделались только ушибами. Напишите /continue''')
        friend_parrot = 1
        if health2 >= 1:
            health2-= 1
            authority2 += 1
        bot.send_message(call.message.chat.id, f'''Ваши статы на данный момент:
Здоровье - {health2} (-1),
Авторитет - {authority2} (+1)''')

    # ПРОШЛОЕ, выбор съесть попугая
    if call.data == "eat_parrot" and count_button == 2:
        count_button += 1
        bot.send_message(call.message.chat.id, '''"Ну, сейчас тяжелые времена" - подумали вы. 
Свернув попугаю шею, вы отпраляетесь на поиски ночлега. 
Теперь у вас есть ужин, а также запятнанная совесть и осуждение окружающих. Напишите /continue''')
        if authority2 >= 1:
            authority2 -= 1
        bot.send_message(call.message.chat.id, f'''Ваши статы на данный момент:
Авторитет - {authority2} (-1)''')

    # ПРОШЛОЕ выбор выпить
    if call.data == "drink_da" and count_button == 3:
        count_button += 1
        bot.send_message(call.message.chat.id, "Джо понравился ваш выбор!")
        # Если спасли попугая, то он нас спасет и мы не умрем
        if friend_parrot == 1:
            bot.send_message(call.message.chat.id, "Вы тянетесь к стакану с ромом. Вас сильно измучила жажда и голод."
                                                   " Но что за невезенье, вдруг ни с того, ни с сего ваш попугай"
                                                   " опрокидывает стакан и его содержимое растекается по всему"
                                                   " полу в трюме. Вы удивлены такому поведению вашего пернатого друга."
                                                   " 'Ха-ха-ха, да... Попугай у тебя то что надо. Быстро смекнул, что "
                                                   "ром отравлен. Ладно, ты мне понравился. Больше не буду пытаться "
                                                   "тебя убить' - с восторгом сказал Джо. Капитан окончательно потерял"
                                                   "ваше доверие. Ваша жизнь в опасности, но ничего нельзя поделать."
                                                   " Сейчас вы плывете черт знает куда, черт знает зачем и черт знает"
                                                   " с кем. ")
            bot.send_message(call.message.chat.id, " 'Куда и зачем вы меня везете?' - спрашиваете вы требовательно,"
                                                   " но осторожно. Без лишних фокусов и никому ненужных историй "
                                                   "вы узнаете, что вас везут в 'Мао'. Еще с детства вам рассказывали "
                                                   "легенду об этом таинственном месте. Каждые пять лет туда привозят"
                                                   "троих юношей и троих девушек для жертвоприношения. По легенде"
                                                   " Они должны пройти опасный лабиринт, избежать всех "
                                                   "ловушек и выжить. Победитель получает все: силу, деньги, рабов,"
                                                   " вино и многое другое. Конечно, почетно быть участником этого"
                                                   " процесса, правда шансы выжить там близки к нулю...."
                                                   " Но, вам нечего терять. Вы сирота, у вас нет друзей, денег и "
                                                   "положения в обществе. Если вас не станет, то никто этого не "
                                                   "заметит. Ваше существования ничего не значит...")
            bot.send_message(call.message.chat.id, " От печальных раздумий вас спасает голос Джо."
                                                   " Отдохни, скоро причалим.")
            if health2 < 3:
                health2 += 1
                bot.send_message(call.message.chat.id, "Сразу же после этих слов, вы снова теряете сознание."
                                                       " Похоже так сказывается недостаток сна, еды, воды и моральное "
                                                       "истощение. Отдыхайте пока можете!")
                bot.send_message(call.message.chat.id, f"Ваши статы на данный момент: Здоровье - {health2} (+1)."
                                                       f" Напишите /bereg")
            else:
                bot.send_message(call.message.chat.id, " 'Я не хочу отдыхать' - решительно произносите вы. "
                                                       "Какой нормальный человек сможет уснуть рядом с его похитителем,"
                                                       " который пытался его убить несколько раз? Однако ваши страданья"
                                                       " были не напрасны, Джо проникся к вам и подарил маленький, "
                                                       "но острый ножик. 'Держи салага, вдруг выживешь' - прогоготал"
                                                       " капитан корабля. Напишите /bereg")
                knife += 1

        # не спасли попугая, теперь мы обречены
        if friend_parrot == 0:
            count_button += 10000
            bot.send_message(call.message.chat.id, "Вы тянетесь к стакану с ромом. Вас сильно измучила жажда и голод."
                                                   " Вы сделали глоток, затем еще и еще... Уталив жажду, вы чувствуете"
                                                   " себя намного лучше, правда длится это недолго. Все вокруг плывет"
                                                   " и кружится. Вас пробивает сильная дрожь, но в тоже время вы"
                                                   " обильно потеете, словно прочистили 5 конюшен. Слейдующие минуты "
                                                   "для вас словно в Аду. Ваше тело ломит, такое чувство что в один "
                                                   "момент все кости и связки разрушились. К вам приходит осознание"
                                                   " что этот старый черт Джо вас отравил. Увы, но это последняя "
                                                   "ваша мысль( Вы погибли, так и не узнав, зачем вас похитили")

    # ПРОШЛОЕ, решили не пить == Смерть
    if call.data == "drink_no" and count_button == 3:
        count_button += 1
        bot.send_message(call.message.chat.id, "Джо не оценил ваш выбор. 'Если для тебя это мерзость, то больше ты"
                                               " ничего не выпьешь.' - процедил Джо. Вы схватили пулю прямо в горло. "
                                               "Вы погибли, так и не узнав, зачем вас похитили.")

    # ПРОШЛОЕ выбор познакомиться с другими
    if call.data == "privet_da" and count_button == 5:
        count_button += 1
        bot.send_message(call.message.chat.id, "Вы решили познакомиться с ребятами) Это похвально, надо ж как-то"
                                               " заводить союзников.")
        # путь высокого авторитета
        if authority2 >= 4:
            global friends
            friends += 1
            bot.send_message(call.message.chat.id, "Вот это да! Вы сразу понравились ребятам. Теперь вы можете "
                                                   "рассчитывать на их помощь в трудную минуту. К сожелению, вы"
                                                   " запомнили имя только одного человека: Иней. Когда-то у вас была "
                                                   "собака с такой кличкой)")
        # путь низкого авторитета
        else:
            bot.send_message(call.message.chat.id, "Вот это да! Вы сразу не понравились ребятам. "
                                                    "Удивительное везенье). Хотя один рыжий паренек решил заговорить "
                                                   "с вами. Его зовут Иней. Кто знает возможно, когда-нибудь он вам "
                                                   "поможет")

        bot.send_message(call.message.chat.id, "Вместе вы отправляетесь исследовать остров. Во время исследования, вы"
                                               " встречаете много опасностей. Но вы не один! С вами ребята. Помогая "
                                               "друг другу, вы все остаетесь в целости и сохраности. Вы дошли к"
                                               " середине острова и обнаружили огромный лабиринт. Каждому предназначен"
                                               " свой вход и свои испытания. Да начнется первый этап! Напишите /first")

    # ПРОШЛОЕ отказ от знакомства
    if call.data == "privet_no" and count_button == 5:
        count_button += 10000
        bot.send_message(call.message.chat.id, "Вы предпочли остаться в одиночестве. Ну в конце концов у всех разные"
                                               " уровни общительности. Вы отправились самостоятельно исследовать 'Мао'."
                                               " Кто ж знал, что тут так опасно!? На вас нападает и жестоко заваливает"
                                               " камнями стая диких попуасов. Ваша история на этом окончена. "
                                               "Как печально")

    if call.data == "uxo" and count_button == 7:
        count_button += 1
        bot.send_message(call.message.chat.id, "И это правильный ответ! Поразительно, вы просто гений)"
                                               "Вы отгадали загадку и теперь можете двигаться дальше. Вперед!"
                                               " к новым испытаниям. Напишите /second")
    if call.data == "ling" and count_button == 7:
        count_button += 1
        bot.send_message(call.message.chat.id, "И это неправильный ответ! Ой-ой-ой, с потолка упала тяжелая сеть"
                                               " и придавила вас. Стены, пол и потолок начали двигаться навстречу "
                                               "друг другу. Похоже вас сейчас расплющит...")
        if knife == 1:
            health2 -= 1
            bot.send_message(call.message.chat.id, "'А вот фигушки' - изрекаете вы. Как хорошо, что вы вовремя"
                                                   " вспомнили про нож, подаренный Джо. Им вы ловко разрезаете сеть"
                                                   " и после вылетаете из комнаты в самый последний момент."
                                                   " Вам удалось выжить !!! Правда вы потеряли нож и нехило расцарапали "
                                                   "себе правую руку. Пора к новым испытаниям."
                                                   f"Ваше здоровье - {health2} (-1)"
                                                   " Напишите /second")

        else:
            bot.send_message(call.message.chat.id, " К сожалению вас расплющило. Сетка, стены, остутсвие воздуха и "
                                                   "пространства, дикий страх - вот ваши последнии воспоминания. "
                                                   "Эх, вот было бы у вас что-нибудь маленькое и острое...."
                                                   " Вы погибли, ваша история окончена. ")

    if call.data == "kill" and count_button == 12:
        bot.send_message(call.message.chat.id, "Вы готовы бороться за свою жизнь до последнего и пойти на все."
                                               " Даже на убийство товарища.")
        if health2 >= 3 and luck2 >= 3 and authority2 > 3:
            count_button += 1
            bot.send_message(call.message.chat.id, "Вы сильнее, быстрее и ловче Инея. К тому же, этот добродушный"
                                                   " юноша никак не ожидал, что вы на него нападете...."
                                                   " Хладнокровно вы прыгаете на Инея и сворачиваете ему шею."
                                                   " Он даже не стал сопротивляться вам. Его опустошенный взгляд "
                                                   "полный боли навсегда останется в вашей памяти..."
                                                   " Вы идете дальше, ожидая увидеть испытания. Но как оказалось, оно"
                                                   " только что и было. Хоть вы и выжили, но совершили непростительный "
                                                   "грех предательство и убийство друга. Вместо обещанной силы, боги"
                                                   " наделяют вас безумием. Вы перестаете понимать кто вы? Что с вами "
                                                   "произошло? Что есть правда, а что есть вымысел? В голове у вас "
                                                   "только крики остальных ребят, которые погибли здесь."
                                                   " Кое как вы нашли выход из лабиринта. Потеряв рассудок и смысл"
                                                   " жизни, вы принимаете решение остаться на острове."
                                                   " ПОЗДРАВЛЯЕМ вы прошли эту историю и открыли одну из концовок !!!"
                                                   " Вы стали сумасшедшим аборигеном на острове Мао. Хорошая "
                                                   "или плохая эта концовка решать вам. Напишите /rezult")
        else:
            bot.send_message(call.message.chat.id, "Весьма опрометчивое решение. Вы слабее и медленнее Инея. "
                                                   "Хоть этот добродушный юноша не ожидал от вас атаки, он быстро "
                                                   "среагировав, ломает вам шею. Мда неприятно... Но его нельзя винить."
                                                   " Иней лишь защищал себя. К тому же он не совершил самый страшный "
                                                   "грех - предательство, в отличии от вас. Ваша игра на этом окончена."
                                                   " Вы не смогли ее пройти. Если вас интересует судьба Инея, то он смог"
                                                   " выбраться с острова, получил обещанную силу, богатство и славу."
                                                   " Семьям погибшим здесь ребятам он оказал помощь, а после собрав"
                                                   " свои последние вещи уехал в неизвестном направлении, в поисках "
                                                   "новой жизни.")
    if call.data == "die" and count_button == 12:
        count_button += 1
        bot.send_message(call.message.chat.id, "Весьма опрометчивое решение. Вы слабее и медленнее Инея. "
                                               " убивать и предавать вашего товарища. Иней тоже не желает этого.")
        if authority2 > 4:
            bot.send_message(call.message.chat.id, "Боги оценили ваш поступок. Они благосклонны к вам. С их помощью"
                                                   " вам вдвоем удалось выйти из лабиринта и покинуть остров."
                                                   " Конечно же силу, славу и золото вы не получили, но зато"
                                                   " вы нашли другое богатство. Вы обрели настоящего и надежного друга"
                                                   " на всю жизнь, а это дорогого стоит. После этой истории с островом,"
                                                   " вы решаете поднакопить денег и уехать далеко-далеко, на поиски"
                                                   " лучшей жизни. "
                                                   " ПОЗДРАВЛЯЕМ вы прошли эту историю и открыли одну из концовок !!!"
                                                   "Хорошая или плохая эта концовка решать вам. Напишите /rezult")
        else:
            bot.send_message(call.message.chat.id, "Боги оценили ваш поступок. Правила есть правила, покинуть "
                                                   "комнату должен только один. Но правила существуют для того"
                                                   " чтобы их нарушать! Вы решили пойти против богов и спастись "
                                                   "из лабиринта, своими людскими силами. Вы продолжили исследовать"
                                                   " лабиринт и нашли место, где очень хлипкие стены. Это не "
                                                   "удивительно ведь постройка очень древняя. Вы принялись ломать эту"
                                                   " стену. И О ЧУДО! У ВАС ПОЛУЧИЛОСЬ! Выбравшись самостоятельно и "
                                                   "наплевав на волю богов, вы оба получаете необыкновенную силу."
                                                   " Теперь вы стали новыми богами этого мира. Вы всемогущи."
                                                   " Только от вас двоих зависит судьба всего человечества. Что с ним"
                                                   " делать решать только вам, но это уже совсем другая история."
                                                   " ПОЗДРАВЛЯЕМ вы прошли эту историю и открыли одну из концовок !!!"
                                                   "Хорошая или плохая эта концовка решать вам. Напишите /rezult")
    # БУДУЩЕЕ
    if call.data == "future" and count_button == 1:
        # характеристики для будущего
        count_button += 1
        bot.send_message(call.message.chat.id, '''2100 год. Москва - процветающая столициа России. Каждый пятый
здесь миллионер. Проблема с пробками кажется вечной, что заставляет людей либо переезжать, либо привыкать.''')
        bot.send_message(call.message.chat.id, f'''Сегодня день Вашего рождения.
Ваше имя - {name1}, 
Ваша удача - {luck1}, 
Ваш авторитет- {authority1}, 
Ваше здоровье - {health1}.''')
        bot.send_message(call.message.chat.id, '''Чтобы в дальнейшем смотреть свои статусы пишите /futCard''')
        bot.send_message(call.message.chat.id, '''Первые 7 лет жизни были не особо захватывающими,
Вы обретали навыки ходьбы, общения, чтения, счета. В 7 лет Вы пошли в школу. Напишите /school. ''')

    # поздороваться с Кевином
    if call.data == "hi" and count_button == 2:
        count_button += 1
        # повышение авторитета
        authority1 += 1
        bot.send_message(call.message.chat.id, ''' + АВТОРИТЕТ
С Кевином вы стали сидеть за одной партой и довольно сильно сдружились.''')
        bot.send_message(call.message.chat.id, '''Так из года в год (все 10 лет) проходит каждый Ваш день:
школа, домашнее задание, сон.''')
        bot.send_message(call.message.chat.id, '''3 апреля 3116 года. Этот день вы запомните на всю жизнь.
Тогда учитель попросил Вас принести из другой аудитории несколько пар микроскопов для лабораторной работы и дал Вам ключ. 
Вы открыли лаборантскую и увидели на полу человека с пробитой головой. Кажется это был ваш учитель по биологии Марк.
Рана была свежая, и 10 минут не было. Рядом лежал 
микроскоп весь в крови. Вы взяли его и тут же поняли какую ошибку совершили...''')
        bot.send_message(call.message.chat.id, '''Вот вбегают учителя..
Полиция..
Вот вы сидите на допросе..''')
        bot.send_message(call.message.chat.id, '''Вот как все было:
- Я зашел в лаборантскую и увидел труп.
- Вы видели кого-то выходящего?
- Нет.
- А дверь была закрыта, когда Вы заходили?
- Да, на ключ.
- Напомните мне для чего вы туда пошли?
- Мой учитель химии, попросил  меня сходить за микроскопами для лабораторной работы.
- В зал суда приглашается Фрэнсис Фишер.''')
        bot.send_message(call.message.chat.id, '''Учитель сказал, что правда отдал ключ от аудитории и отправил за микроскопами, 
однако ключ от лаборантской был только у Галлагера. Преподаватель отрицал свое нахождение в лаборантской в тот день, 
также по его словам в тот кабинет в тот день заходили лишь Вы.''')
        bot.send_message(call.message.chat.id, '''Суд выносит Вам приговор - 60 суток в исправительной колонии для несовершеннолетних
до полного расскрытия дела, которым будет заниматься детектив - Джордж Пуаро. 
Если согласны или не согласны с приговором напишите /protest''')

    # промолчать
    if call.data == "molchat" and count_button == 2:
        count_button += 1
        # понижение авторитета
        authority1 -= 1
        bot.send_message(call.message.chat.id, ''' - АВТОРИТЕТ
Кевин обиделся и всем сказал, что с Вами нельзя дружить. 
Теперь вы сидите в одиночестве.''')
        bot.send_message(call.message.chat.id, '''Так из года в год (все 10 лет) проходит каждый Ваш день:
школа, домашнее задание, сон.''')
        bot.send_message(call.message.chat.id, '''3 апреля 3116 года. Этот день вы запомните на всю жизнь.
Тогда учитель попросил Вас принести из другой аудитории несколько пар микроскопов для лабораторной работы и дал Вам ключ. 
Вы открыли лаборантскую и увидели на полу человека с пробитой головой. Рана была свежая, и 10 минут не было. Рядом лежал 
микроскоп весь в крови. Вы взяли его и тут же поняли какую ошибку совершили...''')
        bot.send_message(call.message.chat.id, '''Вот вбегают учителя..
Полиция..
Вот вы сидите на допросе..''')
        bot.send_message(call.message.chat.id, '''Вот как все было:
- Я зашел в лаборантскую и увидел труп.
- Вы видели кого-то выходящего?
- Нет.
- А дверь была закрыта, когда Вы заходили?
- Да, на ключ.
- Напомните мне для чего вы туда пошли?
- Мой учитель химии, попросил  меня сходить за микроскопами для лабораторной работы.
- В зал суда приглашается Фрэнк Галлагер.''')
        bot.send_message(call.message.chat.id, '''Учитель сказал, что правда отдал ключ от аудитории и отправил за микроскопами, 
однако ключ от лаборантской был только у Галлагера. Преподаватель отрицал свое нахождение в лаборантской в тот день, 
также по его словам в тот кабинет в тот день заходили лишь Вы.''')
        bot.send_message(call.message.chat.id, '''Суд выносит Вам приговор - 60 суток в исправительной колонии для несовершеннолетних
до полного расскрытия дела, которым будет заниматься детектив - Джордж Пуаро. 
Если согласны или не согласны с приговором напишите /protest''')

    if call.data == "ploh" and count_button == 3:
        count_button += 1
        bot.send_message(call.message.chat.id, '''Вы согласились, а значит завтра
Вы отправитесь в исправительную колонию для несовершеннолетних''')
        to_turma(call)

    if call.data == "norm" and count_button == 3:
        count_button += 1
        bot.send_message(call.message.chat.id, f'''Вы начали возмущаться:
- Почему я целых 2 месяца должен отбывать наказание за тот поступок, который не совершал?!
Пусть сначала следователи разберутся! Мне нельзя в тюрьму!
- Успокойтесь мистер {name1},пока ведется следствие Вы будете находится под присмотром, 
когда следователи скажут точно, то мы либо отпустим Вас, либо будет еще одно заседание суда.''')
        to_turma(call)

    # взять заточку себе
    if call.data == "only_me" and count_button == 4:
        count_button += 1
        global weapon
        weapon = 1
        bot.send_message(call.message.chat.id, ''' + ЗАТОЧКА''')
        do_time(call)

    if call.data == "good_man" and count_button == 4:
        count_button += 1
        authority1 += 1
        bot.send_message(call.message.chat.id, ''' + АВТОРИТЕТ
Теперь за вас смогут поручиться в случае чего.''')
        do_time(call)

    if call.data == "ban" and count_button == 4:
        count_button += 1
        bot.send_message(call.message.chat.id, '''Теперь вы находитесь под защитой охраны, возможно из-за 
данного поступка дело раскроется быстрее(детектив поймет, что у вас есть желание сотрудничать)''')
        do_time(call)

    if call.data == "need" and count_button == 5:
        count_button += 1
        weapon = 0
        bot.send_message(call.message.chat.id, '''Значит есть. ХА ну ты и лох!
Вас прижали к стене и обыскали''')
        bot.send_message(call.message.chat.id, '''У ВАС ЗАБРАЛИ ЗАТОЧКУ''')
        into_maze_or_viktorina(call)

    if call.data == "no_need" and count_button == 5:
        count_button += 1
        bot.send_message(call.message.chat.id, '''Да без проблем, бро.''')
        into_maze_or_viktorina(call)

    if call.data == 'help' and count_button == 5:
        count_button += 1
        bot.send_message(call.message.chat.id, '''-Отвали от него
- Кто там пискнул! Тоже хочешь по зубам получить!''')
        if luck1 >= 4:
            bot.send_message(call.message.chat.id, '''ВЫСОКИЙ УРОВЕНЬ УДАЧИ
- Смешной ты, я сказал отвали от него! - Вы вмазали парню кулоком в солнечное сплетение. 
Минуты не прошло, как его уже не было''')
            health1 += 1
            bot.send_message(call.message.chat.id, '''+ ЗДОРОВЬЕ''')
            into_maze_or_viktorina(call)
        else:
            bot.send_message(call.message.chat.id, ''' НИЗКИЙ УРОВЕНЬ УДАЧИ
Из-за драки вас отправили в карцер''')
            into_maze_or_viktorina(call)

    if call.data == 'not_help' and count_button == 5:
        count_button += 1
        health1 -= 1
        bot.send_message(call.message.chat.id, ''' - ЗДОРОВЬЕ
- Эй ты! Куда пошел! Я еще тебя не потряс.''')
        bot.send_message(call.message.chat.id, '''У ВАС ЗАБРАЛИ ЗАТОЧКУ''')
        into_maze_or_viktorina(call)

    if call.data == 'mark' and count_button == 6:
        count_button += 1
        well += 1
        question2(call)

    if call.data == 'fren' and count_button == 6:
        count_button += 1
        question2(call)

    if call.data == 'tom' and count_button == 6:
        count_button += 1
        question2(call)

    if call.data == 'mickr' and count_button == 7:
        count_button += 1
        well += 1
        question3(call)

    if call.data == 'bonk' and count_button == 7:
        count_button += 1
        question3(call)

    if call.data == 'ten' and count_button == 8:
        count_button += 1
        bot.send_message(call.message.chat.id, '''Как вы сделали это заключение?
На сколько я помню результаты от патологоанатома вам не сообщались.''')
        bot.send_message(call.message.chat.id, '''Позвольте я расскажу как все было.
Во-первых, я узнал у ваших одноклассников, что в последнее время вы себя очень странно ведете, 
как оказалось по результатам вашего анализа крови, вы принимали наркотические препараты.
А именно те от которых сносит крышу так, что ничего не помнишь. Очень похоже на ваш случай.''')
        bot.send_message(call.message.chat.id, '''Во-вторых, отпечатки везде только ваши, что опять же подтверждает, 
что вы убийца.''')
        bot.send_message(call.message.chat.id, '''И в-третьих, вы сейчас мне назвали точное время убийства, значит итог очевиден..''')
        bot.send_message(call.message.chat.id, '''ВЫ И ПРАВДА УБИЙЦА И НИКАК ЭТО ОПРОВЕРГНУТЬ НЕ СМОЖЕТЕ''')
        bot.send_message(call.message.chat.id, '''Квест окончен! Надеюсь вам понравилась наша история''')

    if call.data == 'twen' and count_button == 8:
        count_button += 1
        bot.send_message(call.message.chat.id, '''Как вы сделали это заключение?
На сколько я помню результаты от патологоанатома вам не сообщались.''')
        bot.send_message(call.message.chat.id, '''Позвольте я расскажу как все было.
Во-первых, я узнал у ваших одноклассников, что в последнее время вы себя очень странно ведете, 
как оказалось по результатам вашего анализа крови, вы принимали наркотические препараты.
А именно те от которых сносит крышу так, что ничего не помнишь. Очень похоже на ваш случай.''')
        bot.send_message(call.message.chat.id, '''Во-вторых, отпечатки везде только ваши, что опять же подтверждает, 
что вы убийца.''')
        bot.send_message(call.message.chat.id, '''И в-третьих, вы сейчас мне назвали точное время убийства, значит итог очевиден..''')
        bot.send_message(call.message.chat.id, '''ВЫ И ПРАВДА УБИЙЦА И НИКАК ЭТО ОПРОВЕРГНУТЬ НЕ СМОЖЕТЕ''')
        bot.send_message(call.message.chat.id, '''Квест окончен! Надеюсь вам понравилась наша история''')

    if call.data == 'win' and count_button == 8:
        count_button += 1
        if well == 3:
            bot.send_message(call.message.chat.id, '''ВЫ И ПРАВДА УБИЙЦА И НИКАК ЭТО ОПРОВЕРГНУТЬ НЕ СМОЖЕТЕ''')
        else:
            bot.send_message(call.message.chat.id, '''Мда.. В своих показаниях и в том, что было на самом деле вы путаетесь, 
однако последний вопрос все разрешил. ВЫС ОСВОБОДИЛИ, ВЫ НЕ ВИНОВНЫ''')
            bot.send_message(call.message.chat.id, '''Квест окончен! Надеюсь вам понравилась наша история''')


# БУДУЩЕЕ
def first_ask_future(message):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка 1
    key_hi = types.InlineKeyboardButton(text=f'"Привет, я {name1}"', callback_data='hi')
    keyboard.add(key_hi)
    # кнопка 2
    key_molchat = types.InlineKeyboardButton(text='промолчать*', callback_data='molchat')
    keyboard.add(key_molchat)
    question = "Одноклассник: Привет, я Кевин, как тебя зовут?"
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard)


# БУДУЩЕЕ
def protest_ask_future(message):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка 1
    key_ploh = types.InlineKeyboardButton(text=f'да', callback_data='ploh')
    keyboard.add(key_ploh)
    # кнопка 2
    key_norm = types.InlineKeyboardButton(text='нет', callback_data='norm')
    keyboard.add(key_norm)
    # вопрос
    question = f"{name1}, Вы согласны с решением суда?"
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard)


# БУДУЩЕЕ
def to_turma(call):
    bot.send_message(call.message.chat.id, '''Вот вы уже едите в автобусе с заключенными. Вы думаете, что нужно с кем-то познакомиться,
чтобы быть под защитой другого.''')
    global authority1
    if authority1 >= 3:
        bot.send_message(call.message.chat.id, '''ВЫСОКИЙ УРОВЕНЬ АВТОРИТЕТА
Вы познакомились с Томом. Его посадили за незаконную перевозку запрещенных препаратов заграницу.
Вообще он оказался довольно хорошим человеком и сам предложил держаться вместе.''')
        turma(call)

    else:
        bot.send_message(call.message.chat.id, '''НИЗКИЙ УРОВЕНЬ АВТОРИТЕТА
Оказывается заключенные не особо добрые люди.''')
        turma(call)


def turma(call):
    global luck1
    if luck1 >= 3:
        bot.send_message(call.message.chat.id, '''ВЫСОКИЙ УРОВЕНЬ УДАЧИ
Вам повезло, у вас в камере есть сосед и мотать срок будет не так скучно.''')
        zatochka(call)
    else:
        bot.send_message(call.message.chat.id, '''НИЗКИЙ УРОВЕНЬ УДАЧИ
Вы в камере одни, мотать срок будет невозможно скучно''')
        zatochka(call)


# че делать с заточкой
def zatochka(call):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка 1
    key_only_me = types.InlineKeyboardButton(text=f'Оставите себе', callback_data='only_me')
    keyboard.add(key_only_me)
    # кнопка 2
    key_good_man = types.InlineKeyboardButton(text='Отнесете блатным', callback_data='good_man')
    keyboard.add(key_good_man)
    # кнопка 3
    key_good_man = types.InlineKeyboardButton(text='Отнесете охране', callback_data='ban')
    keyboard.add(key_good_man)
    # вопрос
    question = "Во время прогулки вы нашли заточку, что будете с не делать?"
    bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)


# либо чел1 либо чел2
def do_time(call):
    bot.send_message(call.message.chat.id, '''Прошел уже месяц отсидки, а про расследование все тихо. Как оказалось в 
тюрьме не так уж и много развлечений. Можно читать книги либо ходить в качалку, куда вы сейчас и направились.''')
    if weapon != 1:
        bot.send_message(call.message.chat.id, '''Вас осанавливает парень''')
        no_name(call)
    else:
        bot.send_message(call.message.chat.id, '''В углу вы видите как какой-то здоровяк прижал паренька''')
        no_name2(call)


# чел предложит заточку
def no_name(call):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка 1
    key_need = types.InlineKeyboardButton(text='У меня есть.', callback_data='need')
    keyboard.add(key_need)
    # кнопка 2
    key_no_need = types.InlineKeyboardButton(text='Я пацифист', callback_data='no_need')
    keyboard.add(key_no_need)
    # вопрос
    question = "Эй! Парень, нужна заточка?"
    bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)


# чел бьет парня
def no_name2(call):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка 1
    key_help = types.InlineKeyboardButton(text='Помочь парню', callback_data='help')
    keyboard.add(key_help)
    # кнопка 2
    key_not_help = types.InlineKeyboardButton(text='Пройти мимо', callback_data='not_help')
    keyboard.add(key_not_help)
    # вопрос
    question = "Хотите вмешаться?"
    bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)


# ЕСЛИ ПОЛЬЗОВАТЕЛЬ С КОМПА, ТО ЛАБИРИНТ, ИНАЧЕ СРАЗУ ВИКТОРИНА
def into_maze_or_viktorina(call):
    bot.send_message(call.message.chat.id, '''-Эй! Нужна помощь. В долгу не останусь - окликнул вас какой-то мужик.
- Что нужно делать?
- Всего лишь проползти по вентиляции к комнате охраны и отключить одну из камер.
- Ха, а если меня поймают, мне же тогда точно не признают не виновным.
- Не поймают, у нас все схвачено.
- Почему именно я?
- Ты худощавого телосложения и маленького роста.
- Ладно.. Когда заход?
- Сегодня в 2:00
- Ладно''')
    try:
        bot.send_photo(call.message.chat.id, open('vent.png', 'rb'))
    except:
        pass
    bot.send_message(call.message.chat.id, '''- Это карта вентиляции. Тебе нужно допозти до этой комнаты.
- Ок, сколько у меня времени?
- Минут 20, не больше, иначе всем будет не очень весело.
- Понял, если что-то пойдет не так стучим 3 раза.
- Лезь давай!''')
    bot.send_message(call.message.chat.id, '''Наверное это было самое пыльное, узкое и пауками кишащее место на планете.
Вам казалось что вы просто ползаете по кругу, что до этой комнаты никогда не доползти.''')
    if weapon == 1:
        bot.send_message(call.message.chat.id, '''Тут вы услышали голоса.. Прямо под собой.. так вы поняли, что стояли над решеткой,
которая в свою очередь была прямо над комнатой охраны. Там было 2 человека: охранник и еще кто-то, но очень знакомой внешности.
Спустя пару минут они вышли. Пришло ваше время действовать. Вы сняли решетку заранее заготовленной заточкой. Спустившись, 
вы отключаете нужную камеру и ползете обратно в вентиляцию. 
Как только вы поставили решетку на место в комнату резко вошла охрана, отключенную камеру они не заметили.''')
    else:
        bot.send_message(call.message.chat.id, '''Тут вы услышали голоса.. Прямо под собой.. так вы поняли, что стояли над решеткой,
которая в свою очередь была прямо над комнатой охраны. Там было 2 человека: охранник и еще кто-то, но очень знакомой внешности.
Спустя пару минут они вышли. Пришло ваше время действовать. О, нет!.. У вас нет ни заточки, ни отвертки. 
ВЫ НЕ СМОГЛИ ОТКРЫТЬ РЕШЕТКУ''')
    bot.send_message(call.message.chat.id, '''Когда вы приползли обратно, вас ждал маленький surprise...''')

    bot.send_message(call.message.chat.id, '''Человек, расследовавший ваше дела все ходил по комнате и что-то
бубнил себе под нос. Резко остановившись, он сел перед вами и сказал:
- Если ты правильно ответишь на 3 мои вопроса, то ты свободен и государство выплачивает тебе конпенсацию, 
как никак почти 2 месяца тут. Если не ответишь, то мои предположения подтвердятся и ты - преступник.''')
    question1(call)


def question1(call):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка 1
    key_mark = types.InlineKeyboardButton(text='Марк', callback_data='mark')
    keyboard.add(key_mark)
    # кнопка 2
    key_tom = types.InlineKeyboardButton(text='Том', callback_data='tom')
    keyboard.add(key_tom)
    # кнопка 3
    key_fren = types.InlineKeyboardButton(text='Френсис', callback_data='fren')
    keyboard.add(key_fren)
    # вопрос
    question = "Как звали убитого человека?"
    bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)


def question2(call):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка 1
    key_mickr = types.InlineKeyboardButton(text='Микроскоп', callback_data='mickr')
    keyboard.add(key_mickr)
    # кнопка 2
    key_bonk = types.InlineKeyboardButton(text='Дубинка', callback_data='bonk')
    keyboard.add(key_bonk)
    # вопрос
    question = "Как был убит человек?"
    bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)


def question3(call):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка 1
    key_ten = types.InlineKeyboardButton(text='10 минут', callback_data='ten')
    keyboard.add(key_ten)
    # кнопка 2
    key_twen = types.InlineKeyboardButton(text='20 минут', callback_data='twen')
    keyboard.add(key_twen)
    # кнопка 2
    key_win = types.InlineKeyboardButton(text='Я не помню...', callback_data='win')
    keyboard.add(key_win)
    # вопрос
    question = "Сколько человек пролежал без сознания?"
    bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)

# ПРОШЛОЕ
def last_friend_parrot(message):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка «Будущее»
    key_future = types.InlineKeyboardButton(text=f'Спасти попугайчика!', callback_data='save_parrot')
    # добавление кнопки в клавиатуру
    keyboard.add(key_future)
    # кнопка «Прошлое»
    key_ancient = types.InlineKeyboardButton(text='Забрать попугайчика и поужинать им', callback_data='eat_parrot')
    keyboard.add(key_ancient)
    question = "Как вы поступите?"
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard)


# ПРОШЛОЕ
def last_korabl(message):
    bot.send_message(message.chat.id, "Так или иначе, сегодня вам опять не повезло с работой :(."
"Ища себе ночлег, вы бродите по улицам ночного острова."
"Неожиданно, на вас кто-то нападает со спины!")
    global luck2
    if luck2 < 3:
        bot.send_message(message.chat.id, " НИЗКИЙ УРОВЕНЬ УДАЧИ."
                                          "К сожалению, вы не успели увернуться от атаки."
                                          "Противник пронзает нож вам прямо в сердце."
                                          "Печально; ваша история закончилась, не успев начаться")
    else:
        bot.send_message(message.chat.id, "ВЫСОКИЙ УРОВЕНЬ УДАЧИ."
                                          "Вот это реакция! Вы мастерски увернулись от атаки и уже начали бежать в "
                                          "противоположную от маньяка сторону, но не тут то было. Человек хватает вас"
                                          " за плечо. Мысленно попрощавшись с жизнью, вы готовитесь к худшему. Однако"
                                          " нападавший больше не стремится навредить вам."
                                          " 'Неплохая реакция' - с удивлением произносит человек - "
                                          "'Именно такие люди нам нужны'. Не успев понять что происходит, вы ощущаете"
                                          " сильную боль в затылке и теряете сознание. " )
        bot.send_message(message.chat.id, "Вы резко открываете глаза. Все воспоминания о вчерашнем дне перемешаны. "
                                          "Пока вы преходите в себя, вы оглядываетесь по сторонам. "
                                          "Вы попали в трюм.")

        bot.send_message(message.chat.id," 'Что ж, меня зовут Джо. Я капитан этого коробля' - отвечает ваш похититель."
                                         " 'Прошу прощение за столь грубый прием и первую встречу' - прогоготал Джо-"
                                         " 'Не желаете ли осушить со мной, отменную бутылку рома?'."
                                         " Капитан корабля - неприятный, маленький человечешка. Выглядит он плохо:"
                                         " отсутствие настоящих зубов и шрам на глазу. Доверия у вас он не вызывает."
                                         " Как вы поступите? Напишите /drink")


# ПРОШЛОЕ эпизод с ромом
def rom(message):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка «Будущее»
    drink_da = types.InlineKeyboardButton(text='С радостью', callback_data='drink_da')
    # добавление кнопки в клавиатуру
    keyboard.add(drink_da)
    # кнопка «Прошлое»
    drink_no = types.InlineKeyboardButton(text='Я не пью такую мерзость', callback_data='drink_no')
    keyboard.add(drink_no)
    question = "Пить или не пить? Вот в чем вопрос...."
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


# Прошлое высадка на берег
# Прошлое высадка на берег
def kvest1(message):
    bot.send_message(message.chat.id, "Спустя пару часов вас высадили на берег. Джо и его команда сразу же отчалили."
                                      " Скорее всего вы больше не увидитесь. Но да ладно, все что не делается - все"
                                      " к лучшему. Вы оглядываете остров. Здесь довольно-таки красиво! Зеленые пальмы,"
                                      " необычные цветы, солнце, белые песок, шум моря, просто рай не земле!"
                                      " Но не стоит забывать, зачем вас сюда привезли. На острове также есть и другие"
                                      " люди. Может стоит с ними познакомиться?")
    keyboard = types.InlineKeyboardMarkup()
    # кнопка при выборе познакомиться
    privet_da = types.InlineKeyboardButton(text=f'Привет всем! Я {name2}', callback_data='privet_da')
    # добавление кнопки в клавиатуру
    keyboard.add(privet_da)
    # кнопка при выборе остаться одному
    privet_no = types.InlineKeyboardButton(text='Предпочитаю быть одному', callback_data='privet_no')
    keyboard.add(privet_no)
    question = "Познакомиться?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

# ПРОШЛОЕ лабиринт, первое испытание
def maze(message):
    bot.send_message(message.chat.id, ' Вы в лабиринте. Здесь темно и сыро, затхлый запах. Вы двигаетесь на ощупь, '
                                      'опираясь на стены лабиринта. Вы идете в кромешной темноте вот уже 15 минут, как '
                                      'вдруг вас ослепляет яркий свет. Вы нашли "узел познания". Это небольшая комната'
                                      ' с фонтаном по центру. Из него льется кристально чистая и красивая вода. Прохлада'
                                      ' и звон чистой воды, помогает вам прийти в себя. Но не надолго. Исследуя комнату'
                                      ', вы замечаете человеческие кости, а точнее их остатки...')
    global authority2
    global health2
    global knife
    if authority2 > 4:
        bot.send_message(message.chat.id, ' ПУТЬ ВЫСОКОГО АВТОРИТЕТА. '
                                          'К счастью, как оказалось, вы не из робкого десятка. Вам удалось сохранить'
                                          ' самообладание!')
    else:
        health2 -= 1
        bot.send_message(message.chat.id, ' ПУТЬ НИЗКОГО АВТОРИТЕТА. '
                                          'От такого зрелища, у вас кружится голова. К горлу подступает тошнота.'
                                          ' Чтобы восстановиться вам потребовалось не меньше 20 минут, к тому же'
                                          ' вы потеряли много жидкости и поцарапали руку.'
                                          f' Уровень вашего здоровья: {health2} (-1)')
    bot.send_message(message.chat.id, ' Чтобы выйти из комнаты и двигаться дальше, вам надо отгадать загадку.'
                                      ' Загадка: Кто говорит на всех языках мира? ')
    keyboard = types.InlineKeyboardMarkup()
    # кнопка ЭХО
    uxo = types.InlineKeyboardButton(text=f'Эхо', callback_data='uxo')
    # добавление кнопки в клавиатуру
    keyboard.add(uxo)
    # кнопка ЛИНГВИСТ
    ling = types.InlineKeyboardButton(text='Лингвист', callback_data='ling')
    keyboard.add(ling)
    question = "Ваш ответ:"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


def cheleng(message):
    global count_button
    count_button += 1
    global luck2
    global health2
    global friends
    bot.send_message(message.chat.id, " Идя дальше по лабиринту, вам слышатся голоса других ребят. Вы подумали,"
                                      " что уже начали сходить с ума от страха, боли и истощения. Но нет."
                                      " Вы действительно встретились с остальными. До второго испытания, дошли не все."
                                      " Погибло двое ребят: мальчик и девочка...."
                                      " Хорошо, что вас не настигла их учесть. Согласно пророчеству, первое испытание"
                                      " проверяет ваш ум, второе ваше тело, а третье вашу душу и сердце. В четвером"
                                      " вы входите в комнату...")
    if health2 >= 3:
        bot.send_message(message.chat.id, " ХОРОШЕЕ ЗДОРОВЬЕ. Несмотря на все трудности и проблемы, вы остались "
                                          " в хорошей физической форме. Вы с легкостью избегаете ловушек и проходите"
                                          " препятствия. Вам удалось выжить и пройти второе испытание, без потерь."
                                          "Напишите /third")
    elif health2 < 3 and friends == 1:
        bot.send_message(message.chat.id, "ПЛОХОЕ ЗДОРОВЬЕ. Недоедание, недостаток сна, нервы и усталость дали о "
                                          "себе знать. Вы попадаете в первую ловушку и. Ваша нога застряла в "
                                          "половом отсеке. На вас летит большой топор. Смерившись с судьбой,"
                                          " вы закрываете глаза. Однако, ничего не происходит. Ваш новоиспеченный друг -"
                                          " Иней, останавливает топор. Он спас вам жизнь. Хорошо все-таки иметь друзей."
                                          " Вам удалось выжить и пройти второе испытание, без потерь. Напишите /third")
    elif health2 < 3 and friends == 0 and luck2 >= 3:
        bot.send_message(message.chat.id, "ПЛОХОЕ ЗДОРОВЬЕ. Недоедание, недостаток сна, нервы и усталость дали о "
                                          "себе знать. Вы попадаете в первую ловушку и. Ваша нога застряла в "
                                          "половом отсеке. На вас летит большой топор. Вот он момент, когда вам"
                                          " пригодится ваша ловкость рук и удача. В своей обычной жизни, вам часто"
                                          " приходилось воровать, поэтому моторика рук у вас хорошо развита."
                                          " Вам удалось выжить и пройти второе испытание, без потерь."
                                          "Напишите /third")
    else:
        count_button += 1000000
        bot.send_message(message.chat.id, "ПЛОХОЕ ЗДОРОВЬЕ. Недоедание, недостаток сна, нервы и усталость дали о "
                                          "себе знать. Вы попадаете в первую ловушку и. Ваша нога застряла в "
                                          "половом отсеке. На вас летит большой топор.Смерившись с судьбой,"
                                          " вы закрываете глаза. Вы погибли. Очень жаль, ведь до финиша "
                                          "оставалось совсем немного")
def lasted(message):
    global count_button
    count_button += 1
    global friends
    bot.send_message(message.chat.id, " Вот и финал. Вас осталось только двое. Вы и Иней."
                                      " Вы стараетесь не вспоминать о ребятах, которые не добрались до финала."
                                      " Слишком тяжело..."
                                      " По легенде третье испытание самое тяжелое. В нем вам не помогут физические"
                                      " навыки или смекалка. Оно проверяет вашу душу, здесь нельзя будет соврать"
                                      " или понадеяться на другого."
                                      " Вы с Инеем входите в последнюю комнату. На ее стенах красуется надпись:"
                                      " 'Оставь надежду всяк сюда входящий. Только один покинет эту комнату"
                                      " и обретет неистовую силу'. В комнате повисло тяжелое молчание. Вы оба"
                                      " понимаете, что выберется только один. Но кто же это будет? Недолго думая вы:")
    keyboard = types.InlineKeyboardMarkup()
    # кнопка убийства
    kill = types.InlineKeyboardButton(text=f'Набрасываетесь на Инея', callback_data='kill')
    # добавление кнопки в клавиатуру
    keyboard.add(kill)
    # кнопка самопожертвования
    die = types.InlineKeyboardButton(text='Поднимаете руки вверх: "Я не могу так поступить"', callback_data='die')
    keyboard.add(die)
    question = "Ваш ответ:"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


def ask(message):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка «Будущее»
    key_future = types.InlineKeyboardButton(text='"Кто убил Марка?"', callback_data='future')
    # добавление кнопки в клавиатуру
    keyboard.add(key_future)
    # кнопка «Прошлое»
    key_ancient = types.InlineKeyboardButton(text='Остров Мао', callback_data='past')
    keyboard.add(key_ancient)
    question = "Сетинг квеста:"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


bot.polling()
