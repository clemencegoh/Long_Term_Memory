import unittest
from .card_model import Flashcard
from datetime import datetime, timedelta

class TestCardModels(unittest.TestCase):
    def test_simple(self):
        c = Flashcard(question="Hello _?", answer="World")
        self.assertEqual(c.next, datetime.now().date())

        # ensure that after checking, completed still true
        c.checkCard()
        self.assertTrue(c.completed, "checkcard makes it incomplete")

        c.completeCard()
        self.assertEqual(c.next, datetime.now().date() + timedelta(1), "next not adjusted")

    def test_conversion(self):
        c = Flashcard("Hello", "World")
        json_form = c.to_json()
        print(json_form)

        o = Flashcard()
        o.from_json(json_form)
        o.completeCard()
        self.assertEqual(o.to_json(), json_form)

    def test_datetime(self):
        # standard datetime to string
        datenow = datetime.now().date().ctime()
        print(datenow)
        print(type(datenow))

        # resulting string to datetime
        converted = datetime.strptime(datenow, '%a %b %d %H:%M:%S %Y')
        # converted = datetime.strptime(datenow, '%Y-%m-%d')
        print(type(converted))
        print(converted)
        print(converted.ctime())


if __name__ == '__main__':
    unittest.main()