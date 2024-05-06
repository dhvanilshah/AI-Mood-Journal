# Python script to populate the notes database

import os
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from app import Users 
from app import Notes
import pandas as pd

engine = db.create_engine(os.environ["SQLALCHEMY_DATABASE_URI"])
Session = sessionmaker(bind=engine)
session = Session()


# First get a list of all the UUID Keys
query = db.select(Users.uuid_key).distinct()
with engine.connect() as conn:
    uuid_keys = conn.execute(query).fetchall()

uuid_list = []
for record in uuid_keys:
    uuid_list.append(record[0])
num = len(uuid_list)

df = pd.read_csv('data.csv')

for index,row in df.iterrows():
    note = row["Answer"]
    emotions = [col.split(".")[2] for col in df.columns[1:] if row[col] and "f1" in col]
    moods = ' '.join(emotions)
    topics = [col.split(".")[2] for col in df.columns[1:] if row[col] and "t1" in col]
    topics = ' '.join(topics)

    user = uuid_list[index % num]

    data = {"uuid_key": user, "note": note, "mood": moods, "topic": topics}
    entry = Notes(**data)
    session.add(entry)


session.commit()

session.close()


