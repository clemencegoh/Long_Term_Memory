from flask import Flask, request, redirect, url_for, render_template, jsonify
import os
import random
from werkzeug.utils import secure_filename
import json
import datetime
from database.card_model import Flashcard


DATABASE = "database/database.json"
UPLOAD_FOLDER = "static/images"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    """
    List all subjects
    :return:
    """

    subjects = []
    stats = []  # determine if there is something to do today

    with open(DATABASE, 'r') as data:
        # loop through subjects
        for sub, item in json.load(data).items():

            today = datetime.datetime.now()
            converted = datetime.datetime.strptime(item["Next"], '%a %b %d %H:%M:%S %Y')


            # loop through questions and update
            if converted == today:
                stats.append("Pending")
            elif converted < today:
                stats.append("Overdue")
            else:
                stats.append("None")
            subjects.append(sub)

    return render_template('index.html',
                           subjects=subjects,
                           stats=stats)


@app.route('/<subject>', methods=['GET'])
def explore_subject(subject):
    """
    List all question-answer pairs in subject
    :return:
    """

    cards = {}
    flashcard_list = []  # the flashcard object itself
    flashcard_id = []  # unique ids for each card, should be just a number
    flashcard_complete = []

    # open subject
    with open(DATABASE, 'r') as data:
        for sub, item in json.load(data).items():
            if sub == subject:
                cards = item["FlashCards"]
                break

    # parse cards here
    for key, value in cards.items():
        f = Flashcard()
        f.from_dict(value)
        f.checkCard()

        # ensure sorted by not completed at the top
        if not f.completed:
            flashcard_id.insert(0, key)
            flashcard_list.insert(0, f.question)
            flashcard_complete.insert(0, f.completed)
        else:
            flashcard_id.append(key)
            flashcard_list.append(f.question)
            flashcard_complete.append(f.completed)

    return render_template('subject.html',
                           subject=subject,
                           flashcard_id = flashcard_id,
                           flashcard_list= flashcard_list,
                           flashcard_complete=flashcard_complete)


############# create, delete content #########################
@app.route('/flashcards/<subject>/<id>', methods=['GET', 'POST', 'DELETE'])
def getNext(subject, id):
    """
    Shows single flashcard, could be used to navigate to the next one
    :param subject: subject to look under
    :param id: flashcard id
    :return:
    """
    if request.method == 'GET':
        with open(DATABASE, 'r') as f:
            data = json.loads(f.read())
            single_card = data[subject]["FlashCards"][id]

        imagepath = single_card["Image"]
        if imagepath == "":
            imagepath = "static/images/nothing-to-see-here-carrot.gif"

        return render_template("card.html",
                               question=single_card["Question"],
                               answer=single_card["Answer"],
                               hint=single_card["Hint"],
                               notes=single_card["Notes"],
                               imagepath=imagepath)

    if request.method == 'POST':
        # parse form
        file = request.files["Image"]
        filename = ""
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        parsed_data = Flashcard(
            question=request.form["Question"],
            answer=request.form["Answer"],
            hint=request.form["Hint"],
            notes=request.form["Notes"],
            imagepath=os.path.join('static', filename)
        )

        # create and edit
        with open(DATABASE, 'r') as f:
            data = json.loads(f.read())
            data[subject]["FlashCards"][id] = parsed_data.to_dict()
            # print(data)

        # commit
        with open(DATABASE, 'w') as f:
            f.write(json.dumps(data))

        # 200 OK
        resp = jsonify(success=True)
        return resp

    if request.method == "DELETE":
        with open(DATABASE, 'r') as f:
            data = json.loads(f.read())
            del data[subject]["FlashCards"][id]

        with open(DATABASE, 'w') as f:
            f.write(json.dumps(data))

        # 200 OK
        resp = jsonify(success=True)
        return resp

# answer and complete card
@app.route('/flashcards/<subject>/<id>/complete', methods=['POST'])
def completeCard(subject, id):

    success = request.form["Success"]

    with open(DATABASE, 'r') as f:
        card = Flashcard()
        # data = f.read()
        data = json.loads(f.read())
        card.from_dict(data[subject]["FlashCards"][id])

        if success == "true" or success == "True":
            card.completeCard()
        else:
            # reset state
            card.__setstate__(1)
            card.completeCard()

        if data[subject]["Next"] > card.next.ctime():
            data[subject]["Next"] = card.next.ctime()

        data[subject]["FlashCards"][id] = card.to_dict()

    # commit
    with open(DATABASE, 'w') as f:
        f.write(json.dumps(data))

    # 200 OK
    resp = jsonify(success=True)
    return resp

if __name__=='__main__':
    # checkDB()
    app.run(port='8080')
    # app.run(host='0.0.0.0', port=80)