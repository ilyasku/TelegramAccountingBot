from telegram.ext import Updater
from telegramaccountingbot.bot.bot import Bot
from telegramaccountingbot.bot.text_generator import balance_dict_to_message
from telegramaccountingbot.accounting.accounting import Bookkeeper

import os
HOME = os.path.expanduser("~")
token_file = HOME + "/.accounting_bot/token"
with open(token_file, "r") as f:
    token = f.read()

    
class MockBookkeeper(Bookkeeper):
    def __init__(self):
        self.dict_id_to_name = {}
        
    
class MockBot(Bot):

    def _handle_balance(self, bot, update):
        balance_dict = {"a": 501, "b": 3010,
                        "c": 1267, "174510834": 500,
                        "average": 1317}
        id_to_name = {"a": "Anna", "b": "Bruno",
                      "c": "Christ", "174510834": "Ilyas"}
        telegram_id = update.message.chat_id
        print(telegram_id)
        message = balance_dict_to_message(id_to_name, balance_dict)
        bot.send_message(chat_id=telegram_id,
                         text=message)

        
def main():
    bot = MockBot()
    bot.set_bookkeeper(MockBookkeeper())
    bot.set_updater(Updater(token=token))
    print("initializing")
    bot.initialize_handler()
    print("start polling")
    bot.start_polling()
    raw_input("press enter to exit  ")
    print("stop polling")
    bot.stop_polling()

    
if __name__ == "__main__":
    main()
