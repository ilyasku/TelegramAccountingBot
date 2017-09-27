from telegram.ext import Updater
from telegramaccountingbot.bot.bot import Bot
from telegramaccountingbot.accounting.accounting import Bookkeeper
from telegramaccountingbot.accounting.persistence.pg_persistence import PGPersistence

import os
HOME = os.path.expanduser("~")
token_file = HOME + "/.accounting_bot/token"
with open(token_file, "r") as f:
    token = f.read()



def main():
    import sys

    if len(sys.argv) < 3:
        sys.stderr.write("ERROR: Requires at least 2 arguments: \n1. name of data base,\n2. user name for data base,\n(3. password of data base user)")
        sys.exit(1)

    db_name = sys.argv[1]
    db_user = sys.argv[2]    
    db_password = None
    if len(sys.argv) > 3:
        db_password = sys.argv[3]

    import logging
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    bot = Bot()
    bookkeeper = Bookkeeper()
    persistence = PGPersistence(db_name, db_user,
                                db_password)
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
