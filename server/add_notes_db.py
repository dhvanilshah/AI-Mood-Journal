# Python script to populate the notes database

import os
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from app import Users, Notes, Moods, Topics
import pandas as pd
import random
from datetime import datetime, timedelta


engine = db.create_engine(os.environ["SQLALCHEMY_DATABASE_URI"])
Session = sessionmaker(bind=engine)
session = Session()


# First get a list of all the UUID Keys
query = db.select(Users.id).distinct()
with engine.connect() as conn:
    uid_keys = conn.execute(query).fetchall()

uid_list = [record[0] for record in uid_keys]
num = len(uid_list)

# Function to get the Mood IDs
def get_mood_ids(mood_list):
    moods_ids = []
    for mood in mood_list:
        query = db.select(Moods.id).where(Moods.mood == mood)

        with engine.connect() as conn:
            moods = conn.execute(query).fetchall()

        moods_list = [record[0] for record in moods][0]
        moods_ids.append(moods_list)
    return moods_ids

# Function to get the Topic IDs
def get_topic_ids(topic_list):
    topics_ids = []
    for topic in topic_list:
        query = db.select(Topics.id).where(Topics.topic == topic)

        with engine.connect() as conn:
            topics = conn.execute(query).fetchall()

        topic_list = [record[0] for record in topics][0]
        topics_ids.append(topic_list)
    return topics_ids

def random_date():
    start_date = datetime(2023, 9, 1)
    end_date = datetime(2024, 5, 1)
    start_timestamp = start_date.timestamp()
    end_timestamp = end_date.timestamp()
    random_timestamp = random.uniform(start_timestamp, end_timestamp)
    random_date = datetime.fromtimestamp(random_timestamp)
    return random_date


df = pd.read_csv('data.csv')

for index, row in df.iterrows():
    note = row["Answer"]
    emotions = [col.split(".")[2] for col in df.columns[1:] if row[col] and "f1" in col]
    moods = get_mood_ids(emotions)
    topics = [col.split(".")[2] for col in df.columns[1:] if row[col] and "t1" in col]
    topics = get_topic_ids(topics)

    user = uid_list[index % num]

    mood_instances = [session.query(Moods).get(mood_id) for mood_id in moods]
    topic_instances = [session.query(Topics).get(topic_id) for topic_id in topics]

    new_note = Notes(user_id=user, note=note, date_written=random_date())
    new_note.mood.extend(mood_instances)
    new_note.topic.extend(topic_instances)

    session.add(new_note)


session.commit()

session.close()


