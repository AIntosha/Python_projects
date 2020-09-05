import telebot
from datetime import datetime
import json
import random
import requests
import os

token = '--> TOKEN <--'
bot = telebot.TeleBot(token)
step = 0


def save_to_file(message, numb='xxx'):
    currenttime = datetime.fromtimestamp(int(message.date)).strftime('%d.%m.%y %H:%M')
    nameoffile = '@' + str(message.from_user.username) + '.txt'
    if numb == 'xxx':
        with open(nameoffile, 'a+') as file:
            file.write('@' + message.from_user.username + ' [' + currenttime + ']\n' + message.text + '\n')
    else:
        with open(nameoffile, 'a+') as file:
            file.write('@' + message.from_user.username + ' [' + currenttime + ']\n' + 'Пользователь прислал '+ numb + '\n')


@bot.message_handler(commands=['start'])
def start_message(message):
    global step
    step = 0
    output1 = "Добро пожаловать в ботика.\n" \
              "Присаживайтесь, сейчас я расскажу что умею."
    bot.send_message(message.chat.id, output1)

    output2 = "Давайте начнем, нажмите на /step1\n" \
              "Если вы хотите пропустить туториал и посмотреть все возможности, то наберите /menu"
    bot.send_message(message.chat.id, output2)

    save_to_file(message)


@bot.message_handler(commands=['step1'])
def step1_message(message):
    global step
    step = 1
    output = "Бот может отвечать на сообщение пользователя двумя способами:\n" \
             "1. Ответ на ваше сообщение\n" \
             "2. Просто сообщение\n" \
             "Ответы выбираются рандомно из любого заданного количества (например, 5)\n" \
             "Попробуйте отправить боту любое сообщение несколько раз"
    bot.send_message(message.chat.id, output)
    save_to_file(message)


@bot.message_handler(commands=['step2'])
def step2_message(message):
    global step
    step = 2
    output1 = "Бот может отвечать вам фотографией, аудио, видео, ссылкой, чем угодно\n" \
             "Например, вот таким стикером:"
    bot.send_message(message.chat.id, output1)
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAANqXqmdcv89K31nuptVsyhXaeSca5YAAjsDAAK1cdoGGEsG0lVTy0QZBA")
    output2 = "Если хотите увидеть другой стикер, напишите любое сообщение\n" \
             "Перейти дальше /step3"
    bot.send_message(message.chat.id, output2)

    save_to_file(message)

@bot.message_handler(commands=['step3'])
def step3_message(message):
    global step
    step = 3
    output1 = "Можно предложить пользователю согласиться с условиями предоставления услуг:"
    bot.send_message(message.chat.id, output1)
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Взять автора на работу', callback_data="Разумный выбор 😉"))
    bot.send_message(message.chat.id, text="Нажимая на кнопку ниже вы соглашаетесь с договором", reply_markup=markup)
    save_to_file(message)


@bot.message_handler(commands=['step4'])
def step4_message(message):
    global step
    step = 4
    output1 = "Можно предложить пользователю выбрать из нескольких вариантов:"
    bot.send_message(message.chat.id, output1)

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='...звезда?', callback_data="Хорошая попытка, но нет"),
               telebot.types.InlineKeyboardButton(text='Земля', callback_data="Давай попробуем еще раз"))
    markup.add(telebot.types.InlineKeyboardButton(text='Солнце', callback_data="Не совсем, попробуй еще раз"),
               telebot.types.InlineKeyboardButton(text='Пульсар', callback_data="А ты умён, правильно"))
    bot.send_message(message.chat.id, text="Как называется нейтронная звезда с магнитным полем, которое наклонено "
                                           "к оси вращения?", reply_markup=markup)
    save_to_file(message)


@bot.message_handler(commands=['step5'])
def step5_message(message):
    global step
    step = 5
    output1 = "Можно добавить кнопки быстрого доступа, которые будут всегда на виду\n" \
              "(нажмите /hide чтобы убрать кнопки)\n"
    bot.send_message(message.chat.id, output1)

    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True, one_time_keyboard=False)
    keyboard.row('/get_audio', '/get_video')
    keyboard.row('/hide')
    bot.send_message(message.chat.id, text="Чтобы продолжить дальше, нажмите -> /step6", reply_markup=keyboard)
    save_to_file(message)


@bot.message_handler(commands=['get_audio'])
def get_audio_message(message):
    bot.send_audio(message.chat.id, 'CQACAgIAAxkBAAPgXqqn99W73hTosqEDW1IIeAJM7XYAApIHAALJ41BJr1gEldG85vIZBA')
    save_to_file(message)

@bot.message_handler(commands=['get_video'])
def get_video_message(message):
    bot.send_video(message.chat.id, 'BAACAgIAAxkBAAPeXqqnZl6UNZADq2ZAzVUTtHYwSzAAApAHAALJ41BJdYLdSxq1a9sZBA')
    save_to_file(message)

@bot.message_handler(commands=['hide'])
def hide_message(message):
    global step
    bot.send_message(message.chat.id, text='Панелька быстрого доступа убрана', reply_markup=telebot.types.ReplyKeyboardRemove())
    if step == 5:
        bot.send_message(message.chat.id, 'Чтобы продолжить дальше, нажмите -> /step6')
    save_to_file(message)


@bot.message_handler(commands=['step6'])
def step6_message(message):
    global step
    step = 6
    output1 = "Бот может определить что именно послал пользователь и ответить нужным образом.\n" \
              "Например на стикер послать другой стикер, а на фото ответить комплиментом\n" \
              "Попробуйте послать стикер, либо любой другой формат сообщений"
    bot.send_message(message.chat.id, output1)
    bot.send_message(message.chat.id, "Для продолжения экскурсии -> /step7")


@bot.message_handler(commands=['step7'])
def step7_message(message):
    global step
    step = 7
    output1 = "И наконец бот может сохранять всю историю переписки с пользователем\n" \
              "(Чтобы получить весь лог сообщений -> /get_log\n" \
              "И сохранять все присланные пользователем фотографии\n" \
              "(Чтобы бот прислал все отправленные фотографии -> /get_photos"
    bot.send_message(message.chat.id, output1)
    bot.send_message(message.chat.id, "На этом наша маленькая экскурсия окончена.\n"
                                      "Перейти в меню -> /menu")


@bot.message_handler(content_types=['audio'])
def send_text(message):
    bot.send_message(message.chat.id, text='Отличная песня, сохранил в плейлист')
    global step
    if step == 6:
        bot.send_message(message.chat.id, 'Для продолжения экскурсии -> /step7')
    save_to_file(message, 'аудио')


@bot.message_handler(content_types=['video'])
def send_text(message):
    bot.send_message(message.chat.id, text='Видео просто супер')
    global step
    if step == 6:
        bot.send_message(message.chat.id, 'Для продолжения экскурсии -> /step7')
    save_to_file(message, 'видео')


@bot.message_handler(content_types=['document'])
def send_text(message):
    bot.send_message(message.chat.id, text='Сохраню этот документ на всякий случай')
    global step
    if step == 6:
        bot.send_message(message.chat.id, 'Для продолжения экскурсии -> /step7')
    save_to_file(message, 'документ')


@bot.message_handler(content_types=['location'])
def send_text(message):
    bot.send_message(message.chat.id, text='Локацию получил')
    global step
    if step == 6:
        bot.send_message(message.chat.id, 'Для продолжения экскурсии -> /step7')
    save_to_file(message, 'локацию')


@bot.message_handler(content_types=['contact'])
def send_text(message):
    bot.send_message(message.chat.id, text='Контакт сохранен')
    global step
    if step == 6:
        bot.send_message(message.chat.id, 'Для продолжения экскурсии -> /step7')
    save_to_file(message, 'контакт')


@bot.message_handler(content_types=['sticker'])
def send_text(message):
    global step
    if step == 6:
        bot.send_message(message.chat.id, "Крутой стикер, а у меня есть вот такой")
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAIBFF6qrL9iCgqksVhLHNLhHbscsOAqAAIYAAN-hMMI70OajTgDh-sZBA")
        bot.send_message(message.chat.id, 'Для продолжения экскурсии -> /step7')
    else:
        bot.send_message(message.chat.id, "Интересный стикер, сохраню себе")


@bot.message_handler(content_types=['photo'])
def send_text(message):
    bot.send_message(message.chat.id, text='Фотка просто супер !')
    global step
    if step == 6:
        bot.send_message(message.chat.id, 'Для продолжения экскурсии -> /step7')
    file_id = message.json['photo'][2]['file_id']
    togeturl = requests.get('https://api.telegram.org/bot' + token + '/getFile?file_id=' + file_id)
    file_path = json.loads(togeturl.content.decode())['result']['file_path']
    url = 'https://api.telegram.org/file/bot' + str(token) + '/' + file_path
    # save to harddrive
    currenttime = datetime.fromtimestamp(int(message.date)).strftime('%Y-%m-%d_%H-%M')
    img_folder_path = os.path.join(os.path.dirname(__file__), "@"+message.from_user.username)
    try:
        os.makedirs("@"+message.from_user.username)
    except:
        pass
    dirListing = os.listdir(img_folder_path)
    picname = os.path.join(img_folder_path, str(len(dirListing)+1)+'_'+currenttime+'.jpg')
    open(picname, 'wb').write(requests.get(url).content)
    currenttime = datetime.fromtimestamp(int(message.date)).strftime('%d.%m.%y %H:%M')
    nameoffile = '@' + str(message.from_user.username) + '.txt'
    with open(nameoffile, 'a+') as file:
        file.write('@' + message.from_user.username + ' [' + currenttime + ']\n' + 'Пользователь отправил фото' + '\n')


@bot.message_handler(commands=['get_log'])
def get_log_message(message):
    log = open(os.path.join(os.path.dirname(__file__), "@"+message.from_user.username) + '.txt', 'rb')
    bot.send_document(message.chat.id, log)
    log.close()

@bot.message_handler(commands=['get_photos'])
def get_photos_message(message):
    path = os.path.join(os.path.dirname(__file__), "@"+message.from_user.username)
    list_of_photos = os.listdir(path)
    if len(list_of_photos) == 0:
        bot.send_message(message.chat.id, 'Вы не прислали ни одной фотографии')
    else:
        for i in list_of_photos:
            sending = open(os.path.join(os.path.dirname(__file__), "@"+message.from_user.username, i), 'rb')
            bot.send_photo(message.chat.id, sending)
            sending.close()
    bot.send_message(message.chat.id, "Перейти в меню -> /menu")

@bot.message_handler(commands=['menu'])
def get_photos_message(message):
    global step
    step = 0
    input1 = '/start - начать туториал заново\n' \
            '/step1 - Два вида ответов на сообщения\n' \
            '/step2 - Бот может отвечать стикерами\аудио\итд\n' \
            '/step3 - Меню с одной кнопкой\n' \
            '/step4 - Меню с несколькими кнопками\n' \
            '/step5 - Панель быстрого доступа\n' \
            '/step6 - Бот определяет любой тип сообщения\n' \
            '/step7 - Получить лог сообщений \ все фотографии'
    bot.send_message(message.chat.id, input1)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global step
    bot.send_message(call.message.chat.id, call.data)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if step == 3:
        bot.send_message(call.message.chat.id, 'Двигаться дальше -> /step4')
    elif step == 4:
        bot.send_message(call.message.chat.id, "Попробовать еще раз -> /step4\n"
                                              "Двигаться дальше -> /step5")

    for i in range(len(call.message.json['reply_markup']['inline_keyboard'])):
        for j in range(len(call.message.json['reply_markup']['inline_keyboard'][i])):
            if str(call.message.json['reply_markup']['inline_keyboard'][i][j]['callback_data']) == str(call.data):
                replytext = call.message.json['reply_markup']['inline_keyboard'][i][j]['text']

    currenttime = datetime.fromtimestamp(int(call.message.date)).strftime('%d.%m.%y %H:%M')
    nameoffile = '@' + str(call.message.chat.username) + '.txt'
    with open(nameoffile, 'a+') as file:
        file.write('@' + call.message.chat.username + ' [' + currenttime + ']\n' + replytext + '\n')


@bot.message_handler(func=lambda m: True)
def save_text(message):
    global step
    if message.text[0] == "/":
        bot.reply_to(message, 'Такой команды не существует, нажмите на /menu')
    else:
        if step == 0:
            bot.send_message(message.chat.id, 'Чтобы начать смотреть туториал нажмите на /start\n'
                                              'Либо нажмите на /menu чтобы увидеть меню')
        elif step == 1:
            answers = ['ответ 1',
                       'ответ 2',
                       'ответ 3',
                       'ответ 4',
                       'ответ 5']
            bot.reply_to(message, answers[random.randint(0, 4)]+'\n(1. Ответ на сообщение)')
            bot.send_message(message.chat.id, answers[random.randint(0, 4)]+'\n(2. Просто сообщение)')
            bot.send_message(message.chat.id, "----------\nЧтобы продолжить, нажмите на /step2")
        elif step == 2:
            answers = ['CAACAgIAAxkBAANzXqmgRZwecvrkyTAF54vdGZEz7roAAjkAAw220hlfMEC2OVMxNBkE',
                       'CAACAgIAAxkBAANrXqmdf9UJ0I-NAl4PlqG9p_FfKrAAAgQAA-nYEyiPjdYgb2mImRkE',
                       'CAACAgIAAxkBAANsXqmdhNzR0FKAPaUfrPepJMPE6qoAAvcAA1advQoLciQdSPQNMBkE',
                       'CAACAgIAAxkBAANtXqmdjU0nQz7vkzV5D1lMpVyBtOMAAkYAA1KJkSP4_uXkCtUKHRkE',
                       'CAACAgIAAxkBAANuXqmdkY6gTn90VoOM--r1xb269egAAhoAA_cCyA-vLwlpco42yxkE']
            bot.send_sticker(message.chat.id, answers[random.randint(0, 4)])
            bot.send_message(message.chat.id, "Хотите еще? отправьте еще сообщение\n"
                                              "Двигаться дальше -> /step3")
        elif step == 3:
            bot.send_message(message.chat.id, 'Чтобы продолжить дальше, нажмите -> /step4')
        elif step == 4:
            bot.send_message(message.chat.id, 'Чтобы продолжить дальше, нажмите -> /step5')
        elif step == 5:
            bot.send_message(message.chat.id, 'Чтобы продолжить дальше, нажмите -> /step6')
        elif step == 6:
            bot.send_message(message.chat.id, 'Чтобы продолжить дальше, нажмите -> /step7')
        elif step == 7:
            bot.send_message(message.chat.id, 'Чтобы перейти в меню, нажмите -> /menu')
    save_to_file(message)

bot.polling()
