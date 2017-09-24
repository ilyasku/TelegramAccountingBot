from telegram.ext import CommandHandler
import time
import logging
from . import text_generator

logger = logging.getLogger("telegramaccountingbot.bot")
logger.setLevel(logging.WARNING)

class Bot:
    def __init__(self):
        self.updater = None
        self.bookkeeper = None

    def set_updater(self, updater):
        self.updater = updater

    def set_bookkeeper(self, bookkeeper):
        self.bookkeeper = bookkeeper

    def initialize_handler(self):
        dispatcher = self.updater.dispatcher
        balance_handler = CommandHandler(
            'balance', self._handle_balance)
        dispatcher.add_handler(balance_handler)
        add_handler = CommandHandler(
            'add', self._handle_add, pass_args=True)
        dispatcher.add_handler(add_handler)
        
    def _handle_balance(self, bot, update):
        telegram_id = update.message.chat_id
        d_id_to_name = self.bookkeeper.dict_id_to_name
        d_balance = self.bookkeeper.get_balance()
        message = text_generator.balance_dict_to_message(
            d_id_to_name,
            d_balance)        
        bot.send_message(chat_id=telegram_id,
                         text=message)

    def _handle_add(self, bot, update, args):
        print("==== _handle_add")
        print(args)
        telegram_id = update.message.chat_id
        if not self.bookkeeper.has_id(telegram_id):
            msg = "Unknown Telegram Id!"
            bot.send_message(chat_id=telegram_id,
                             text=msg)
            logger.warning("attempt to add by id " + str(telegram_id))
            return
        if len(args) < 2:            
            msg = "Not enough parameters for /add !\n"
            msg += "Need to provide at least 2:\n"
            msg += "   1. Amount you just paid,\n"
            msg += "   2. Name of shop."
            bot.send_message(chat_id=telegram_id,
                             text=msg)            
            return
        try:
            value = int(float(args[0]) * 100)
        except:
            msg = "Cannot interpret the first parameter ('{0!s}') "
            msg += "as a number! You need to provide the amount you "
            msg += "just paid as first parameter!"
            msg = msg.format(args[0])
            bot.send_message(chat_id=telegram_id,
                             text=msg)
            return
        location = str(args[1])
        date = time.strftime("%Y:%m:%d::%H:%M:%S")
        self.bookkeeper.add_transaction(telegram_id,
                                        value,
                                        date,
                                        location)
        
    def start_polling(self):
        self.updater.start_polling(0.5)

    def stop_polling(self):
        self.updater.stop()


def handle_balance(bot, update):
    telegram_id = update.message.chat_id
    message = "jau jau wau jau hau"
    bot.send_message(chat_id=telegram_id,
                     text=message)

    
def handle_balance_for_lambda(bot, update, bookkeeper):
    telegram_id = update.message.chat_id
    message = text_generator.balance_dict_to_message(
        bookkeeper.dict_id_to_name,
        bookkeeper.get_balance())
    bot.send_message(chat_id=telegram_id,
                     text=message)
