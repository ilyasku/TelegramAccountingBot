"""
USAGE: 
   o install in develop mode: navigate to the folder containing this file,
                              and type 'python setup.py develop --user'.
                              (ommit '--user' if you want to install for 
                               all users)                           
"""


from setuptools import setup

## use setup to install SDF package and executable scripts
setup(name='telegramaccountingbot',
      version='0.01',
      description='Telegram bot to keep track of your household expenses',
      url='https://github.com/ilyasku/TelegramAccountingBot',
      author='Ilyas Kuhlemann',
      author_email='ilyasp.ku@gmail.com',
      license='MIT',
      packages=["telegramaccountingbot",
                "telegramaccountingbot.bot",
                "telegramaccountingbot.accounting",
                "telegramaccountingbot.accounting.persistence",
                "telegramaccountingbot.executables"],
      entry_points={
          "console_scripts": [
              "tab-mock=telegramaccountingbot.executables.mock_bot_memory:main",
              "telegram-accounting-bot=telegramaccountingbot.executables.telegram_accounting_bot:main"
          ]
      },
      install_requires=[
          "python-telegram-bot",
          "psycopg2"# , "nose",
      ],
      zip_safe=False)
