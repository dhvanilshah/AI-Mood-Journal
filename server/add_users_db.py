# Python script to add out 5 users to the database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Users
from app import Notes
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

for data in entries_data:
    entry = Users(**data)
    session.add(entry)


session.commit()

session.close()
