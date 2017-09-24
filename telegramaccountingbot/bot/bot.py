from telegram.ext import CommandHandler
import time
from . import text_generator


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
        
    def _handle_balance(self, bot, update):
        print("==== _handle_balance")
        telegram_id = update.message.chat_id
        print(telegram_id)
        d_id_to_name = self.bookkeeper.dict_id_to_name
        print("======== d_id_to_name")
        print(d_id_to_name)
        d_balance = self.bookkeeper.get_balance()
        print("======== d_balance")
        print(d_balance)
        message = text_generator.balance_dict_to_message(
            d_id_to_name,
            d_balance)        
        bot.send_message(chat_id=telegram_id,
                         text=message)

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
