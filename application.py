import os
from helpers import apology, login_required, shorten_title
from helpers import api_book
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

# set up database s
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def search_reviews():
    user_reviews = {}
    books_list = []
    books = db.execute('''select name, isbn, title, author,year, review, rating 
                        from users, books, reviews
                        where users.id=reviews.user_id and reviews.isbn_id = 
                        books.isbn and  users.id=:user_id''',
                        {"user_id":session['user_id']}).fetchall()
    if books:
        for book in books:
            book_dict = dict(book.items())
            print(book['isbn'])
            book_dict['tooltip'] = 'ISBN: ' + book['isbn'] \
                                + '\n' + "Title : " + book['title']\
                                + '\n' + 'Author : ' + book['author']\
                                + '\n' + 'Year : ' + str(book['year'])\
                                + '\n' + 'Rating : ' + str(book['rating'])\
                                # + '\n' + 'Review : ' + book['review']
            books_list.append(book_dict)
        user_reviews['found'] = True
        user_reviews['books'] = books_list
    else:
        user_reviews['books'] = books
        user_reviews['found'] = False

    return user_reviews

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
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
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
        print('username: ', row['name'])
        # Remember which user has logged in
        session["user_id"] = row["id"]
        # set user_id in the database
        # db.set_userid(session['user_id'])

        # Redirect user to home page
        flash(f'User {name} now logged in')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


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

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/edit")
@login_required
def edit():
    user_reviews = search_reviews()
    if user_reviews['found']:
        flash('Select one of the books to edit your review.')
        return render_template('edit.html', books=user_reviews['books'])
    else:
        message = 'No book reviews found for this user.'
        return render_template('empty.html', message=message)

@app.route("/edit_review", methods=['POST'])
@login_required
def edit_review():
    rating = request.form.get('rating')
    review = request.form.get('review')
    isbn_id = request.form.get('isbn')
    user_id = session['user_id']
    db.execute('''update reviews set review=:review, rating=:rating
                  where user_id =:user_id and isbn_id =:isbn_id''',
                  {"review": review, "rating": rating, 
                  "isbn_id":isbn_id, "user_id":user_id})
    db.commit()
    flash(f'Review and rating for book with isbn : {isbn} updated.')
    return redirect('/')


@app.route("/remove")
@login_required
def remove():
    user_reviews = search_reviews()
    if user_reviews['found']:
        flash('Select one of the books to delete your review.')
        return render_template('remove.html', books=user_reviews['books'])
    else:
        message = 'No book reviews found for this user.'
        return render_template('empty.html', message=message)


@app.route("/remove_review", methods=['POST'])
@login_required
def remove_review():
    isbn_id = request.form.get('isbn')
    user_id = session['user_id']
    db.execute('''delete from reviews 
                  where user_id =:user_id and isbn_id =:isbn_id''',
                  {"isbn_id":isbn_id, "user_id":user_id})
    db.commit()
    flash(f'Review and rating for book with isbn : {isbn_id} removed.')
    return redirect('/')

@app.route("/password")
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

@app.route('/books/<string:isbn>', methods=["GET"])
@login_required
def books(isbn):
    # query database to get book data
    book = db.execute('select * from books where isbn = :isbn', {"isbn":isbn}).fetchone()
    #print(book['isbn'], book['title'], book['author'], book['year'])
    # query goodreads api for average rating and number of ratings
    book_data = api_book(book, isbn)
    # print(book_data)
    reviews = db.execute('''select name, review, rating from  users, reviews 
                            where isbn_id=:isbn and id=user_id''',
                         {"isbn":isbn}).fetchall()
    # print(reviews)
    rack_data = {}
    if reviews:
        counter = 0;
        sum = 0;
        for review in reviews:
            counter += 1
            sum += review['rating']
        avg = sum / counter
        rack_data['rack_avg'] = f'{avg:.2f}'
        rack_data['rack_reviews'] = counter
    return render_template('book_info.html', book=book_data, reviews=reviews, rack=rack_data)
    # display info ('book_info.html')


# Utility Routes

@app.route('/add/<string:isbn>', methods=['POST'])
def add(isbn):
    rating = int(request.form.get('rating'))
    review = request.form.get('review')
    db.execute('''insert into reviews(isbn_id,user_id,review,rating)
                  values(:isbn,:user_id,:review,:rating)''',
                  {"isbn":isbn,"user_id":session['user_id'],
                   "review":review,"rating":rating})
    db.commit()
    flash(f'Added review for book with isbn {isbn}')
    return redirect('/')

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
        #print('register row', row['id'], row['name'])
    isAvail =  jsonify(avail)
    #print('Available', avail)
    return isAvail

@app.route('/search/<string:term>', methods=['GET'])
@login_required
def search(term):
    term = term.lower()

    try:
        year = int(term)
    except:
        year = None;

    term = "%" + term + "%" 
    
    if year:
        sql_search = '''select  isbn, title, author, year from books 
                            where  isbn like :term or lower(title) like :term or 
                            lower(author) like :term or year = :year 
                            order by title'''
    else:
        sql_search = '''select  isbn, title, author, year from books 
                            where  isbn like :term or lower(title) like :term or 
                            lower(author) like :term
                            order by title'''
    books = db.execute(sql_search, {"term":term, "year":year}).fetchall()
    if books:
        books_list = []
        for book in books:
            # https://stackoverflow.com/questions/10588375/can-i-assign-values-in-rowproxy-using-the-sqlalchemy
            book_dict = dict(book.items())
            # print(book_dict)
            # book_dict['tooltip'] = '<em><u>ISBN</u></em> : ' + book['isbn']\
            #                     + '\n' + '<em><u>Title</u></em> : ' + book['title']\
            #                     + '\n' + '<em><u>Author</u></em> : ' + book['author']\
            #                     + '\n' + '<em><u>Year</u></em>: ' + str(book['year'])
            book_dict['tooltip'] = 'ISBN: ' + book['isbn']\
                                + '\n' + 'Title : ' + book['title']\
                                + '\n' + 'Author : ' + book['author']\
                                + '\n' + 'Year: ' + str(book['year'])
            books_list.append(book_dict)
        html = render_template('search.html', books = books_list)
        #print(html)
        return html
    else:
        message ='No books were found.'
        return render_template('empty.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
