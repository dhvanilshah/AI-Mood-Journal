import os
from flask import Flask, jsonify, request, session
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from utils import generate_uuid, hash_password
from datetime import datetime
from collections import defaultdict
import openai

app = Flask(__name__)
load_dotenv() 

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
db = SQLAlchemy(app)

open_ai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = open_ai_api_key
client = openai.OpenAI()

class Users(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text(), nullable = False)
    password = db.Column(db.Text(), nullable = False)
    uuid_key = db.Column(db.Text(), nullable = False)

    def __init__(self, username, password, uuid_key):
        self.username = username
        self.password = password
        self.uuid_key = uuid_key

    def map(self):
        return {'id': self.id, 'username': self.username, 'password': self.password, 'uuid_key': self.uuid_key}


note_mood = db.Table(
    'note_mood',
    db.Column('note_id', db.ForeignKey('Notes.id')),
    db.Column('mood_id', db.ForeignKey('Moods.id'))
)


note_topic = db.Table(
    'note_topic',
    db.Column('note_id', db.ForeignKey('Notes.id')),
    db.Column('topic_id', db.ForeignKey('Topics.id'))
)


class Notes(db.Model):
    __tablename__ = "Notes"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.ForeignKey('Users.id'), nullable = False)
    note = db.Column(db.Text(), nullable = False)
    date = db.Column(db.DateTime, nullable = False)

    mood = db.relationship("Moods", secondary = note_mood, backref=db.backref('notes', lazy='dynamic'))
    topic = db.relationship('Topics', secondary = note_topic, backref=db.backref('notes', lazy='dynamic'))

    def __init__(self, user_id, note, date_written = None):
        self.user_id = user_id
        self.note = note
        if date_written:
            self.date = date_written
        else:
            self.date = datetime.utcnow()

    def map(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'note': self.note,
            'date': self.date
        }

class Moods(db.Model):
    __tablename__ = "Moods"

    id = db.Column(db.Integer, primary_key = True, )
    mood = db.Column(db.Text(), nullable = False)

    def __init__(self, mood):
        self.mood = mood

    def map(self):
        return {'id': self.id, 'mood': self.mood}


class Topics(db.Model):
    __tablename__ = "Topics"

    id = db.Column(db.Integer, primary_key = True)
    topic = db.Column(db.Text(), nullable = False)

    def __init__(self, topic):
        self.topic = topic

    def map(self):
        return {'id': self.id, 'topic': self.topic}

@app.route('/')
def hello():
    return 'hello world'

@app.route('/addauth', methods = ['POST'])
def addUsers():
    data = request.get_json()
    user = Users(data['username'], hash_password(data['password']), generate_uuid())
    db.session.add(user)
    db.session.commit()
    return jsonify({'uuid': user.uuid_key}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    user = Users.query.filter_by(username = username).first()

    if not user:
        return 'User not found.', 400

    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'uuid': user.uuid_key}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/posts', methods=['GET'])
def posts():
    user_uuid = request.headers.get('UUID')

    if not user_uuid:
        return 'User UUID not found in headers', 400

    user = Users.query.filter_by(uuid_key=user_uuid).first()
    notes = Notes.query.filter_by(user_id=user.id).all()

    if notes:
        res = [note.map() for note in notes]
        return jsonify({'posts': res}), 200
    else:
        return jsonify({'error': 'No notes found for user'}), 401

def call_open_ai(prompt, message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0.7,
        max_tokens=64,
        top_p=1
    )

    return response.choices[0].message.content


@app.route('/delete_post', methods = ['POST'])
def delete_post():
    data = request.get_json()
    note_id = data['note_id']
    note = Notes.query.get(int(note_id))
    db.session.delete(note)
    db.session.commit()
    return jsonify({'note_id': note_id})

@app.route('/new_post', methods=['POST'])
def new_post():
    user_uuid = request.headers.get('UUID')

    if not user_uuid:
        return 'User UUID not found in headers', 400

    user = Users.query.filter_by(uuid_key=user_uuid).first()

    data = request.get_json()
    note = data['note']

    mood_records = Moods.query.all()
    moods = (', ').join([m.mood for m in mood_records])
    mood_prompt = ("You will be provided with a journal entry, and your task is to classify its sentiment as one or more "
              "of the following moods: {}."
              "ONLY USE THE MODDS PROVIDED IN THIS PROMPT. Return the moods as a comma separated string.").format(moods)
    ai_predicted_moods = call_open_ai(mood_prompt, note).split(',')
    ai_predicted_moods = [s.strip() for s in ai_predicted_moods]
    predicted_mood_records = Moods.query.filter(Moods.mood.in_(ai_predicted_moods)).all()

    topic_records = Topics.query.all()
    topics = (', ').join([t.topic for t in topic_records])
    topics_prompt = (
        "You will be provided with a journal entry, and your task is to classify its topic as one or more "
        "of the following topic: {}."
        "ONLY USE THE TOPICS PROVIDED IN THIS PROMPT. Return the moods as a comma separated string.").format(topics)
    ai_predicted_topics = call_open_ai(topics_prompt, note).split(',')
    ai_predicted_topics = [s.strip() for s in ai_predicted_topics]
    predicted_topic_records = Topics.query.filter(Topics.topic.in_(ai_predicted_topics)).all()

    new_note = Notes(user_id=user.id, note=note)
    new_note.mood.extend(predicted_mood_records)
    new_note.topic.extend(predicted_topic_records)

    db.session.add(new_note)
    db.session.commit()

    return jsonify({'note': new_note.map()}), 200


@app.route('/moods_between_dates', methods=['GET'])
def get_moods_between_dates():
    user_uuid = request.headers.get('UUID')

    if not user_uuid:
        return 'User UUID not found in headers', 400

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return 'Start date or end date not provided', 400

    try:
        date_format = "%Y-%m-%dT%H:%M:%S%z"
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date, date_format)
    except ValueError:
        return 'Invalid date format. Please use YYYY-MM-DD', 400

    user = Users.query.filter_by(uuid_key=user_uuid).first()

    if not user:
        return 'User not found', 404

    user_notes = Notes.query.filter_by(user_id=user.id)
    notes = user_notes.filter(Notes.date.between(start_date, end_date)).order_by(Notes.date).all()

    mood_hash = defaultdict(list)
    for note in notes:
        date_key = (note.date).strftime("%Y-%m-%d")
        moods = [m.mood for m in note.mood]
        mood_hash[date_key].extend(moods)

    events = []
    for date, moods in mood_hash.items():
        unique_moods = list(set(moods))
        for m in unique_moods:
            events.append({
                'title': m.title(),
                'start': date,
                'end': date,
                'className': "danger",
            })

    return jsonify(events), 200


@app.route('/topics_between_dates', methods=['GET'])
def get_topics_between_dates():
    user_uuid = request.headers.get('UUID')

    if not user_uuid:
        return 'User UUID not found in headers', 400

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return 'Start date or end date not provided', 400

    try:
        date_format = "%Y-%m-%dT%H:%M:%S%z"
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date, date_format)
    except ValueError:
        return 'Invalid date format. Please use YYYY-MM-DD', 400

    user = Users.query.filter_by(uuid_key=user_uuid).first()

    if not user:
        return 'User not found', 404

    user_notes = Notes.query.filter_by(user_id=user.id)
    notes = user_notes.filter(Notes.date.between(start_date, end_date)).order_by(Notes.date).all()

    topic_hash = defaultdict(list)
    for note in notes:
        date_key = (note.date).strftime("%Y-%m-%d")
        moods = [t.topic for t in note.topic]
        topic_hash[date_key].extend(moods)

    events = []
    for date, topics in topic_hash.items():
        unique_topics = list(set(topics))
        for m in unique_topics:
            events.append({
                'title': m.title(),
                'start': date,
                'end': date,
                'className': "danger",
            })

    return jsonify(events), 200


@app.route('/welcome')
def welcome():
    return 'You Already have a page'

# @app.route('/delete/<id>', methods = ['DELETE'])
# def deleteMessage(id):
#     tweet = Tweet.query.get(int(id))
#     db.session.delete(tweet)
#     db.session.commit()
#     return jsonify(tweet.map())

with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
