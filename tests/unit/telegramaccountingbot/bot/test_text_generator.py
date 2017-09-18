import unittest

from telegramaccountingbot.bot.text_generator import balance_dict_to_message


class TestDictToMessage(unittest.TestCase):

    def test_dict_to_message(self):
        dict_id_to_name = {"0": "Hugo",
                           "1": "Ilyas"}
        balance_dict = {"1": 1280,
                        "0": 390,
                        "average": 500}
        response = balance_dict_to_message(dict_id_to_name,
                                           balance_dict)
        self.assertTrue(response.count("average paid: 5.00\n"))
        self.assertTrue(response.count("Ilyas: 12.80 (+7.80)"))
        self.assertTrue(response.count("Hugo: 3.90 (-1.10)"))

