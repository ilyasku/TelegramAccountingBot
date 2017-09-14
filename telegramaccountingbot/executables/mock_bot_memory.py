from telegram.ext import Updater
from telegramaccountingbot.bot.bot import Bot
from telegramaccountingbot.accounting.accounting import Bookkeeper

import os
HOME = os.path.expanduser("~")
token_file = HOME + "/.accounting_bot/token"
with open(token_file, "r") as f:
    token = f.read()

    
class MockBookkeeper(Bookkeeper):
    def __init__(self):
        self.dict_id_to_name = {}

    def get_balance(self):
        return {"a": 501, "b": 3010,
                "c": 1267, "ilyas": 500,
                "average": 1317}

    
def main():
    bot = Bot()
    bot.set_bookkeeper(MockBookkeeper())
    bot.set_updater(Updater(token=token))
    bot.initialize_handler()
    raw_input("press enter to exit  ")
    
if __name__ == "__main__":
    main()

