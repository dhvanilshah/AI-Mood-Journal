# Python script to add out 5 users to the database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Users
from app import Notes
from app import Moods
from app import Topics
import os
import uuid


engine = create_engine(os.environ["SQLALCHEMY_DATABASE_URI"])


Session = sessionmaker(bind=engine)
session = Session()

def generate_uuid():
    return str(uuid.uuid4())

entries_data = [
    {"username": "serene.joe", "password": "serene.joe", "uuid_key": generate_uuid()},
    {"username": "dhvanil.shah", "password": "dhvanil.shah", "uuid_key": generate_uuid()},
    {"username": "david.katz", "password": "david.katz", "uuid_key": generate_uuid()},
    {"username": "aliza.meller", "password": "aliza.meller", "uuid_key": generate_uuid()},
    {"username": "yuri.hu", "password": "yuri.hu", "uuid_key": generate_uuid()}
]

moods_entries = [
    {"mood": "afraid"},
    {"mood": "angry"},
    {"mood": "anxious"},
    {"mood": "ashamed"},
    {"mood": "awkward"},
    {"mood": "bored"},
    {"mood": "calm"},
    {"mood": "confused"},
    {"mood": "disgusted"},
    {"mood": "excited"},
    {"mood": "frustrated"},
    {"mood": "happy"},
    {"mood": "jealous"},
    {"mood": "nostalgic"},
    {"mood": "proud"},
    {"mood": "sad"},
    {"mood": "satisfied"},
    {"mood": "surprised"}
]

topics_entries = [
    {"topic": "exercise"},
    {"topic": "family"},
    {"topic": "food"},
    {"topic": "friends"},
    {"topic": "god"},
    {"topic": "health"},
    {"topic": "love"},
    {"topic": "recreation"},
    {"topic": "school"},
    {"topic": "sleep"},
    {"topic": "work"}
]

for data in entries_data:
    entry = Users(**data)
    session.add(entry)

for data in moods_entries:
    entry = Moods(**data)
    session.add(entry)

for data in topics_entries:
    entry = Topics(**data)
    session.add(entry)


session.commit()

session.close()
