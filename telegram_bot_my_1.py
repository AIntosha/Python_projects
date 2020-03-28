from telegram.ext import Updater
# to answer to >>> /commands
from telegram.ext import CommandHandler
# to answer to >>> regular messages
from telegram.ext import MessageHandler, Filters


# updater == frontend of telegram.bot
updater = Updater(token='1094576304:AAFKUkLSX52kY6ebwggfO-AyTcocFSonWvc', use_context=True)
dispatcher = updater.dispatcher


# when someone /start >>> bot anwser by def start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ты кто такой? я тебя не звал, ступай восвоясе")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


# experimenting with new /command
# context.args = [what typed]
def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)


# bot answers to regular messages \\ to yourself > text=update.message.text
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="GET OUT OF EHEREE")

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)





updater.start_polling()
