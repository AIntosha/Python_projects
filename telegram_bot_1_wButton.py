### from youtube videotutor

#1
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import MessageHandler
#2
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
#3
from telegram import ReplyKeyboardRemove

## to catch errors
def log_error(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print('Error>>>: {}'.format(e))


button_help = 'SOS_BUTTON'

def button_help_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='SOS ON THE WAY WIU WIU WIU',
        reply_markup=ReplyKeyboardRemove()
    )

# @log_error
def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text == button_help:
        return button_help_handler(update=update, context=context)

    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_help)
            ],
        ],
        resize_keyboard=True,
    )


    update.message.reply_text(
        text='Press the button bitch',
        reply_markup=reply_markup,
    )


def main():
    print('Start')

    updater = Updater(
        token='!!token!!',
        use_context=True,
    )

    # print(updater.bot.get_me())

    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))

    updater.start_polling()
    updater.idle()

    # print('Finish')

if __name__ == "__main__":
    main()
