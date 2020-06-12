from flask import Blueprint, render_template, request
from flask import flash, redirect, session
# from flask_session import Session
from helpers import apology, login_required
from database import db
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates',
              static_folder='static', static_url_path='/auth_static')

  
@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted 
        name = request.form.get("username")
        if not name:
            return apology("You must provide a username.")
        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            return apology("You must provide a password.")
        # Query database for username
        row = db.execute("SELECT * FROM users WHERE name = :name",
                          {"name": name}).fetchone()
        # Ensure username exists and password is correct
        if (row is None) or (not check_password_hash(row["password"], password)):
            return apology("Invalid username and/or password")
        # print('username: ', row['name'])

        # Remember which user has logged in
        session["user_id"] = row["id"]
        session['username'] = row['name']
         
        # Redirect user to home page
        flash(f'User {name} now logged in')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
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
            flash(f"User {name} is registered.")
            return render_template('index.html')
            # return redirect('/')
    else:
        return render_template('register.html')

@auth_bp.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@auth_bp.route("/password")
@login_required
def password():
    if request.method == 'POST':
        # access post parameters
        old = request.form.get('oldpassword')
        new = request.form.get('newpassword')
        conf = request.form.get('confirmation')
        # see if new and confirmation password match
        if new != conf:
            return apology("New passord and confirmation do not match.")
        # query database to access user data
        row = db.execute("select * from users where id = :id", 
                        {"id":session['user_id']}).fetchone()
        oldhash = row['password']
        if not check_password_hash(oldhash, old):
            return apology('Current password is wrong.')
        newhash = generate_password_hash(new)
        # update database with new user password 
        db.execute('update users set password = :newhash id = :id', 
                {"newhash": newhash, "id": session['user_id']})
        return redirect('/logout')
    else:
        return render_template('password.html')
