# Python script to add out 5 users to the database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Users
from app import Moods
from app import Topics
import os

from utils import generate_uuid, hash_password


engine = create_engine(os.environ["SQLALCHEMY_DATABASE_URI"])


Session = sessionmaker(bind=engine)
session = Session()


users = [
    {"username": "serene.joe", "password": hash_password("serene.joe"), "uuid_key": generate_uuid()},
    {"username": "dhvanil.shah", "password": hash_password("dhvanil.shah"), "uuid_key": generate_uuid()},
    {"username": "david.katz", "password": hash_password("david.katz"), "uuid_key": generate_uuid()},
    {"username": "aliza.meller", "password": hash_password("aliza.meller"), "uuid_key": generate_uuid()},
    {"username": "yuri.hu", "password": hash_password("yuri.hu"), "uuid_key": generate_uuid()}
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

for data in users:
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
