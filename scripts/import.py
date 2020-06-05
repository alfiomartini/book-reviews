import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

 
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# open csv file and insert data into table books:

with open('books.csv', 'r', newline='', encoding='utf-8') as file:
    file_csv = csv.reader(file)
    headers = next(file_csv) # skip headers
    for isbn, title, author, year in file_csv:
        db.execute('''insert into books(isbn, title, author, year) 
                      values(:isbn, :title, :author, :year)''',
                   {"isbn": isbn, "title": title, "author": author,
                     "year": int(year)})
    db.commit()