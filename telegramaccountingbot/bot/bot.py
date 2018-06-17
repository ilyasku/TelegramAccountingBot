from telegram.ext import CommandHandler
import time
from datetime import datetime
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
            'balance', self._handle_balance, pass_args=True)
        dispatcher.add_handler(balance_handler)
        add_handler = CommandHandler(
            'add', self._handle_add, pass_args=True)
        dispatcher.add_handler(add_handler)
        
    def _handle_balance(self, bot, update, args):
        telegram_id = update.message.chat_id
        d_id_to_name = self.bookkeeper.dict_id_to_name
        today = datetime.today()
        if len(args) == 0:
            month = today.month
            year = today.year        
            d_balance = self.bookkeeper.get_balance(year, month)
            message_prefix = "balance for {:02d}/{}\n".format(month, year)
        elif len(args) == 1:
            if args[0] == 'total':
                message_prefix = "balance for complete history\n"
                d_balance = self.bookkeeper.get_balance()
            else:
                try:
                    month = int(args[0])
                except ValueError:
                    msg = "Cannot interpret the first parameter ('{0!s}') "
                    msg += "as a number! You need to specify a month "
                    msg += "with a number between 1 and 12!"
                    msg = msg.format(args[0])
                    bot.send_message(chat_id=telegram_id,
                                     text=msg)
                    return
                year = today.year
                d_balance = self.bookkeeper.get_balance(year, month)
                message_prefix = "balance for {:02d}/{}\n".format(month, year)
        elif len(args) == 2:
            try:
                month = int(args[0])
                year = int(args[1])
            except ValueError:
                msg = "Cannot interpret your parameters ('{0!s}', '{1!s}') "
                msg += "as a numbers! You need to specify a month "
                msg += "with a number between 1 and 12, and a year!"
                msg = msg.format(args[0], args[1])
                bot.send_message(chat_id=telegram_id,
                                 text=msg)
                return
            d_balance = self.bookkeeper.get_balance(year, month)
            message_prefix = "balance for {:02d}/{}\n".format(month, year)

        message_prefix = "-" * 10 + "\n" + message_prefix + "-"*10 + "\n"
        message = text_generator.balance_dict_to_message(
            d_id_to_name,
            d_balance)        
        bot.send_message(chat_id=telegram_id,
                         text=message_prefix+message)

    def _handle_add(self, bot, update, args):
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
        date = time.strftime("%Y-%m-%d")
        self.bookkeeper.add_transaction(telegram_id,
                                        value,
                                        date,
                                        location)
        
    def start_polling(self):
        self.updater.start_polling(0.5)

    def stop_polling(self):
        self.updater.stop()
