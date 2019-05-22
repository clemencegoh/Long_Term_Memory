from datetime import datetime, timedelta
import json


class Flashcard:
    def __init__(self,
                 question="",
                 answer="",
                 hint="",
                 notes="",
                 imagepath=""):
        self.question = question
        self.answer = answer
        self.notes = notes
        self.hint = hint
        self.imagepath = imagepath
        self.state = 1
        self.created = datetime.now().date()
        self.next = datetime.now().date()
        self.completed = True

    def __setstate__(self, state):
        self.state = state

    def completeCard(self):
        self.next += timedelta(self.state)
        self.state *= 2
        self.completed = True

    def checkCard(self):
        today = datetime.now().date()
        if self.created == self.next:
            return
        if today == self.next:
            self.completed = False
        elif today > self.next:
            # exceed
            self.completed = False
            self.state = 1
            self.next = today

    def to_json(self):
        return json.dumps({
            "Question": self.question,
            "Answer": self.answer,
            "Hint": self.hint,
            "Notes": self.notes,
            "Image": self.imagepath,
            "State":self.state,
            "Created": self.created.ctime(),
            "Next": self.next.ctime(),
            "Completed": self.completed,
        })

    def to_dict(self):
        return ({
            "Question": self.question,
            "Answer": self.answer,
            "Hint": self.hint,
            "Notes": self.notes,
            "Image": self.imagepath,
            "State": self.state,
            "Created": self.created.ctime(),
            "Next": self.next.ctime(),
            "Completed": self.completed,
        })

    def from_json(self, data):
        o = json.loads(data)
        self.question = o["Question"]
        self.answer = o["Answer"]
        self.hint = o["Hint"]
        self.notes = o["Notes"]
        self.imagepath = o["Image"]
        self.state = o["State"]
        self.created = datetime.strptime(o["Created"], '%a %b %d %H:%M:%S %Y')
        self.next = datetime.strptime(o["Next"], '%a %b %d %H:%M:%S %Y')
        self.completed = o["Completed"]

    def from_dict(self, o):
        self.question = o["Question"]
        self.answer = o["Answer"]
        self.hint = o["Hint"]
        self.notes = o["Notes"]
        self.imagepath = o["Image"]
        self.state = o["State"]
        self.created = datetime.strptime(o["Created"], '%a %b %d %H:%M:%S %Y')
        self.next = datetime.strptime(o["Next"], '%a %b %d %H:%M:%S %Y')
        self.completed = o["Completed"]


