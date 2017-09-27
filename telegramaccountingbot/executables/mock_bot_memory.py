from telegram.ext import Updater
from telegramaccountingbot.bot.bot import Bot
from telegramaccountingbot.accounting.accounting import Bookkeeper

import os
HOME = os.path.expanduser("~")
token_file = HOME + "/.accounting_bot/token"
with open(token_file, "r") as f:
    token = f.read()

    
class InMemoryPersistence:
    def __init__(self):
        self._transactions = []
        self._id_to_name = []

    def add_id_name_pair(self, _id, name):
        self._id_to_name.append((_id, name))

    def get_dict_id_to_name(self):
        d = {}
        for pair in self._id_to_name:
            d[pair[0]] = pair[1]
        return d

    def get_transactions(self, _id):
        l = []
        for tr in self._transactions:
            if tr['id'] == _id:
                l.append(tr)
        return l

    def add_transaction(self, _id, value, date, location):
        self._transactions.append(
            {"id": _id, "value": value,
             "date": date, "location": location})

    
class MockBookkeeper(Bookkeeper):
    def __init__(self):
        self.dict_id_to_name = {"a": "Anna", "b": "Bruno",
                                "c": "Christ", 174510834: "Ilyas",
                                370060018: "Annika"}

    def get_balance(self):
        return {"a": 501, "b": 3010,
                "c": 1267, "174510834": 500,
                "average": 1317}


def main():
    import logging
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    bot = Bot()
    bookkeeper = Bookkeeper()
    persistence = InMemoryPersistence()
    persistence.add_id_name_pair(174510834, "Ilyas")
    bookkeeper.set_persistence(persistence)
    bot.set_bookkeeper(bookkeeper)
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
