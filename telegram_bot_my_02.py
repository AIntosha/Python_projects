'''
1. Были команды /start /help /fuck
2. Посылание нахер сопровождается стикером ---
3. Добавить кнопку в меню /button1
4. Добавить несколько кнопок в /buttons
5. Добавить красивую кнопку в меню /button1_cool
6. Добавить несколько красивых в /buttons_cool
somefixes working on v3
'''

# to answer to >>> regular messages
from telegram.ext import MessageHandler, Filters
# for buttons
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import Sticker

# when someone /start >>> bot answer by def start
def start(update, context):
    output = "Ты кто такой? я тебя не звал, ступай восвоясе"
    context.bot.send_message(chat_id=update.effective_chat.id, text=output)


def help(update, context):
    output = "Список команд:\n" \
             "/help - вызывает это меню\n" \
             "/fuck - посылает вас нахер\n" \
             "/button1 - можно тыкнуть кнопку\n" \
             "/buttons - много кнопок"
    context.bot.send_message(chat_id=update.effective_chat.id, text=output)


def fuck(update, context):
    output = "🤔 Слыш Мыш 🤔"
    context.bot.send_message(chat_id=update.effective_chat.id, text=output)

# CAADAgADQAADyIsGAAE7MpzFPFQX5QI

def button1(update, context):
    keyboard = [[InlineKeyboardButton("Конечно Фраер", callback_data='Красава, проходи')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Ты фраер или мент позорный?', reply_markup=reply_markup)


def buttons(update, context):
    keyboard = [[InlineKeyboardButton("Я тупой, не знаю", callback_data='Земля тебе пухом додик'),
                 InlineKeyboardButton("Беру помощь зала", callback_data="Ты безнадежен, забей")],
                 [InlineKeyboardButton("!!! 300 !!!", callback_data="ты в ловушке...ОТСОСИ У ТРАКТОРИСТА")]]
    update.message.reply_text('Сколько будет 150+150 ?', reply_markup=InlineKeyboardMarkup(keyboard))


def button_answer(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=query.data)
    # query.edit_message_text(text="Ай Красава, проходи")


# unknown commands answer
def unknown(update, context):
    output = "Лучше напиши /fuck"
    context.bot.send_message(chat_id=update.effective_chat.id, text=output)


# bot answers to regular messages \\ to yourself > text=update.message.text
def echo(update, context):
    # output = Sticker.file_unique_id('CAADAgADQAADyIsGAAE7MpzFPFQX5QI')
    output = "йоу йоу йоу, 282 майами сити"
    context.bot.send_message(chat_id=update.effective_chat.id, text=output)


# updater == frontend of telegram.bot
updater = Updater(token='token', use_context=True)
dispatcher = updater.dispatcher


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('fuck', fuck))
updater.dispatcher.add_handler(CommandHandler('button1', button1))
updater.dispatcher.add_handler(CommandHandler('buttons', buttons))
updater.dispatcher.add_handler(CallbackQueryHandler(button_answer))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))


updater.start_polling()
updater.idle()
