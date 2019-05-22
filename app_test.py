import unittest
import requests

class TestCardModels(unittest.TestCase):
    def test_delete(self):
        r = requests.delete("http://localhost:8080/flashcards/Math/01")
        self.assertEqual(r.status_code, 200)

        with open('database/database.json', 'w') as d:
            with open('database/regenerate.json', 'r') as f:
                d.write(f.read())
                self.assertEqual(d.read(), f.read())

    def test_create(self):
        with open('templates/akstar.png', 'rb') as f:
            r = requests.post("http://localhost:8080/flashcards/Math/02",
                              files={'Image': f},
                              data={
                                  'Question': 'Hello _?',
                                  'Answer': 'World',
                                  'Hint': 'Standard',
                                  'Notes': 'Basics of programming'
                              })
            self.assertEqual(r.status_code, 200)

    def test_complete(self):
        r = requests.post("http://localhost:8080/flashcards/Math/01/complete",
                          data={
                              "Success": True
                          })
        self.assertEqual(r.status_code, 200)

    def test_complete_unsuccessful(self):
        r = requests.post("http://localhost:8080/flashcards/Math/01/complete",
                          data={
                              "Success": False
                          })
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()