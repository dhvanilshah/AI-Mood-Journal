import os
from flask import Flask, jsonify, request, session
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import bcrypt


app = Flask(__name__)
load_dotenv() 

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
db = SQLAlchemy(app)
# login_manager.init_app(app)

class Tweet(db.Model):
    __tablename__ = "Tweets"

    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.Text(), nullable = False)
    tweet = db.Column(db.String(150), nullable = False)

    def __init__(self, author, tweet):
        self.author = author
        self.tweet = tweet
    
    def map(self):
        return {'id': self.id, 'author': self.author, 'tweet': self.tweet}
    
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
    uuid_key = db.Column(db.Text(), nullable = False)
    note = db.Column(db.Text(), nullable = False)

    mood = db.relationship("Moods", secondary = note_mood, backref=db.backref('notes', lazy='dynamic'))
    topic = db.relationship('Topics', secondary = note_topic, backref=db.backref('notes', lazy='dynamic'))


    def __init__(self, uuid_key, note):
        self.uuid_key = uuid_key
        self.note = note
    
    def map(self, mood, topic):
        return {'id': self.id, 'uuid_key': self.uuid_key, 'note': self.note, 'mood': [Moods.id for mood_id in mood], 'topic': [Topics.id for topic_id in topic]}
    
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

@app.route('/messages', methods = ['GET'])
def getMessages():
    tweets = Tweet.query.all()

    res = []
    for tweet in tweets:
        res.append(tweet.map())

    return jsonify(res)

@app.route('/add', methods = ['POST'])
def addMessage():
    data = request.get_json()
    tweet = Tweet(data['author'], data['tweet'])
    db.session.add(tweet)
    db.session.commit()
    return jsonify(tweet.map())

@app.route('/addauth', methods = ['POST'])
def addUsers():
    data = request.get_json()
    user = Users(data['username'], data['password'], data['uuid_key'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.map())

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    user = Users.query.filter_by(username = username).first()

    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401
    

@app.route('/welcome')
def welcome():
    return 'You Already have a page'

@app.route('/delete/<id>', methods = ['DELETE'])
def deleteMessage(id):
    tweet = Tweet.query.get(int(id))
    db.session.delete(tweet)
    db.session.commit()
    return jsonify(tweet.map())

with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
