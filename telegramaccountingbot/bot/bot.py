from telegram.ext import CommandHandler

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
        balance_handler = CommandHandler('balance', self._handle_balance)
        dispatcher.add_handler(balance_handler)
        
    def _handle_balance(self, bot, update):
        telegram_id = update.message.chat_id
        message = text_generator.balance_dict_to_message(
            self.bookkeeper.dict_id_to_name,
            self.bookkeeper.get_balance())
        bot.send_message(chat_id=telegram_id,
                         text=message)
