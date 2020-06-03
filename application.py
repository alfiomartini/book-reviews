import os
from helpers import apology, login_required, shorten_title
from flask import Flask, session, url_for, redirect, flash
from flask import render_template, request, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
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
    
    def exec(self,query, params=None):
        _db = self.db
        if params:
            rows = _db.execute(query, params)
        else:
            rows = _db.execute(query)
        return rows

# set up database s
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
# mydb = SQL(db)

# Ensure responses aren't cached
# hard refresh: ctrl+f5 (Windows), ctrl+shift+r(Linux, Mac)
# see https://roadmap.sh/guides/http-caching
# see https://pythonise.com/series/learning-flask/python-before-after-request
@app.after_request
def after_request(response):
    # Cache-Control specifies how long and in what manner should the content be cached. 
    # no-store specifies that the content is not to be cached by any of the caches
    # (public, private, server)
    # must-revalidate avoids that. If this directive is present, it means that stale content 
    # cannot be served in any case and the data must be re-validated from the server before serving.
    # no-cache indicates that the cache can be maintained but the cached content is to be re-validated 
    # (using ETag for example) from the server before being served. 
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    # how long a cache content should be considered fresh? never.
    response.headers["Expires"] = 0
    return response

# App routes

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
        name = request.form.get('username')

        #double checking, since it is done in the front end
        if not name:
            return apology("You must provide a user name.")
        row = db.execute("select * from users where name = :name", {"name":name}).fetchone()
        if row is not None:
            return apology('This user is already registered.')
        password = request.form.get('password')
        if not password:
            return apology("You must provide a passord")
        confirmation = request.form.get('confirmation')
        if not confirmation:
            return apology("You must confirm your passord.")
        # end double ckeck

        hash_passw = generate_password_hash(password)
        if not check_password_hash(hash_passw, confirmation):
            return apology('Password and Confirmation do not match.')
        else:
            db.execute('insert into users(name, password) values(:name,:password)', 
                           {"name":name, "password":hash_passw})
            db.commit()
            # flash("You are registered.")
            return redirect('/login')
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


# Utility Routes

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    name = request.args.get('username')
    # query database to see if there are any row with this username
    row = db.execute("select * from users where name = :name", {"name": name}).fetchone()
    if row is None:
        avail = True
    else:
        avail = False
        print('register row', row['id'], row['name'])
    isAvail =  jsonify(avail)
    print('Available', avail)
    return isAvail


if __name__ == '__main__':
    app.run(debug=True)
