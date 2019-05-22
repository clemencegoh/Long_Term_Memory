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
            # loop through questions and update
            if item["Next"] == datetime.datetime.now().date().ctime():
                stats.append("Pending")
            elif item["Next"] < datetime.datetime.now().date().ctime():
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
    flashcard_list = []
    flashcard_id = []

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
        flashcard_id.append(key)
        flashcard_list.append(f.to_json())


    return render_template('index.html',
                           flashcard_id = flashcard_id,
                           flashcard_list= flashcard_list)


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

        return render_template("index.html", single_card=single_card)

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


if __name__=='__main__':
    # checkDB()
    app.run(port='8080')
    # app.run(host='0.0.0.0', port=80)