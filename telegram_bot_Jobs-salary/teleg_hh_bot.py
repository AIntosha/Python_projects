import telebot
from datetime import datetime
import requests
import statistics
from requests_html import HTMLSession
import re

token = '--> TOKEN <--'
bot = telebot.TeleBot(token)
step = 0

vacancy = ''

def lego(message, vacancy):
    usdrate = 75
    avgsalarylist = list()
    vacancywithSalary = 0
    def responce(page, per_page, text=vacancy):
        responce = requests.get('https://api.hh.ru/vacancies/',
                                headers={'User-Agent': 'Python (fuoff@gmail.com)'},
                                params={
                                    'text': text,
                                    'page': page,
                                    'per_page': per_page
                                })
        return responce.json()


    # вывести все вакансии в столбик
    for x in range(responce(page=0, per_page=100)['pages']):
        templist = responce(page=x, per_page=100)['items']
        for i in templist:
            if i['salary'] is None:
                continue
            else:
                vacancywithSalary += 1
                if i['salary']['currency'] == 'RUR':
                    if i['salary']['from'] is None and i['salary']['to'] is not None:
                        avgsalarylist.append(i['salary']['to'])
                    elif i['salary']['from'] is not None and i['salary']['to'] is None:
                        avgsalarylist.append(i['salary']['from'])
                    elif i['salary']['from'] is not None and i['salary']['to'] is not None:
                        avgsalarylist.append(int(round((i['salary']['from'] + i['salary']['to']) / 2)))
                    else:
                        print('ERRRRRORRRR')
                # USD
                else:
                    if i['salary']['from'] is None and i['salary']['to'] is not None:
                        avgsalarylist.append(i['salary']['to'] * usdrate)
                    elif i['salary']['from'] is not None and i['salary']['to'] is None:
                        avgsalarylist.append(i['salary']['from'] * usdrate)
                    elif i['salary']['from'] is not None and i['salary']['to'] is not None:
                        avgsalarylist.append(int(round(((i['salary']['from'] + i['salary']['to']) / 2) * usdrate)))
                    else:
                        print('ERRRRRORRRR')

    textik = 'Профессия: ' + str(vacancy)
    bot.send_message(message.chat.id, '---------------')
    bot.send_message(message.chat.id, textik)

    if responce(page=0, per_page=1)['pages'] == 2000:
        session = HTMLSession()
        url = 'https://hh.ru/search/vacancy?L_is_autosearch=false&area=113&clusters=true&enable_snippets=true&text=%' + vacancy + '&page=0'
        page = session.get(url)
        vacNum = ''
        vacNumPage = page.html.find(
            'body > div.HH-MainContent.HH-Supernova-MainContent > div > div > div > div.bloko-columns-wrapper > div > '
            'div.bloko-column.bloko-column_xs-0.bloko-column_s-8.bloko-column_m-12.bloko-column_l-16 > div > h1')
        xRegex = re.compile('\d')
        allnumbers = re.findall(xRegex, vacNumPage[0].text)
        for i in allnumbers:
            vacNum += i
        textik = 'Всего вакансий: ' + str(vacNum)
        bot.send_message(message.chat.id, textik)
    else:
        if responce(page=0, per_page=1)['pages'] == 1:
            bot.send_message(message.chat.id, "Вакансий не найдено")
        else:
            textik = 'Всего вакансий: ' + str(responce(page=0, per_page=1)['pages'])
            bot.send_message(message.chat.id, textik)
    try:
        textik = 'Средняя зарплата: ' + str(int(round(statistics.median(avgsalarylist))))
        bot.send_message(message.chat.id, textik)
    except:
        pass

    textik = 'По ссылке можешь ознакомиться подробнее'
    bot.send_message(message.chat.id, '---------------')
    bot.send_message(message.chat.id, 'Теперь можешь написать другую')


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
    output1 = "Здарова, бандит\n" \
              "Ботик запилен на бесплатном хостинге и в один поток, так что не торопи малыша, он медленный"
    bot.send_message(message.chat.id, output1)
    bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAIHIV64KNeL41Y5VkoLbKAKJm1AEULSAAL5BAACNkcTAAF2SFZFjqak9RkE")
    bot.send_message(message.chat.id, "Пиши любую профессию по типу Python junior и жди результатов")

    save_to_file(message)

@bot.message_handler(func=lambda m: True)
def save_text(message):
    if message.text[0] == "/":
        bot.reply_to(message, 'Такой команды не существует, просто пиши текстом профессию и жди резалтов')
    else:
        vacancy = message.text
        bot.send_message(message.chat.id, 'Запрос получен, ожидай ответа')
        lego(message, vacancy)

    save_to_file(message)

bot.polling()
