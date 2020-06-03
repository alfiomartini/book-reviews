import os
from helpers import apology, login_required, shorten_title
from flask import Flask, session, url_for, redirect, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Extends basic database setup
class SQL:
    def __init__(self,db):
        self.db = db 
    
    def exec(self,query):
        _db = self.db
        rows = _db.execute(query)
        return rows

# set up database s
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
mydb = SQL(db)


@app.route("/")
@login_required
def index():
    return "Index: TODO"

@app.route("/login")
def login():
    return "Login: TODO"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        pass
    else:
        return render_template('register.html')

@app.route("/new")
@login_required
def new():
    return "New Review: TODO"

@app.route("/edit")
@login_required
def edit():
    return "Edit: TODO"

@app.route("/remove")
@login_required
def remove():
    return "Remove: TODO"

@app.route("/password")
@login_required
def password():
    return "Change Password: TODO"


if __name__ == '__main__':
    app.run(debug=True)
