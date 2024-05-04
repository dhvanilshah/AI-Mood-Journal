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
    
app.secret_key = b'737210ef5b5a2e512223a7a0e3aa8011a7d1e65bdc8c369e4253b43e38064d5f'

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


    # user = Users.query.filter_by(username=username).first()

    # if user and user.check_password(password):
    #     return jsonify({'message': 'Login successful'}), 200
    # else:
    #     return jsonify({'message': 'Invalid username or password'}), 401
    

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
