from telegramaccountingbot.bot.bot import Bot
from telegramaccountingbot.accounting.accounting import Bookkeeper

import os
HOME = os.path.expanduser("~")
token_file = HOME + "/.accounting_bot/token"
with open(token_file, "r") as f:
    token = f.read()

