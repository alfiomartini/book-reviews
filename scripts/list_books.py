import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
class SQL:
    def __init__(self,db):
        self.db = db 
    
    def exec(self,query):
        _db = self.db
        rows = _db.execute(query)
        return rows


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
mydb = SQL(db)


books = mydb.exec('select isbn, title, author, year from books')
for book in books:
    print(book['isbn'], book['title'], book['author'], book['year'])

