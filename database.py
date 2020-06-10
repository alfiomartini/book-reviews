from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os 

# set up database s
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))