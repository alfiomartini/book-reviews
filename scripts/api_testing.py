import os
import csv
import json
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

GOODREADS_KEY = 'wKy3eEHxspfhDj5YJ5POHw'

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

# test api

resp = requests.get("https://www.goodreads.com/book/review_counts.json",
     params={"key": GOODREADS_KEY, "isbns": "0743474155"})
print(resp)
print('----------------------------------------------------------------')
print(resp.text) #json text
print('----------------------------------------------------------------')
# json decoder: json -> python object
jsonObj = resp.json() #js object
print(jsonObj)
print('----------------------------------------------------------------')
print(jsonObj['books'])
print(jsonObj['books'][0])
print(jsonObj['books'][0]['work_ratings_count'])
print(jsonObj['books'][0]['average_rating'])
