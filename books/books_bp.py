from flask import Blueprint, render_template, request
from flask import flash, redirect, session
from helpers import login_required, check_user, api_book
from database import db

books_bp = Blueprint('books_bp', __name__, template_folder='templates',
              static_folder='static', static_url_path='/books_static')

@books_bp.route('/books/<string:isbn>', methods=["GET"])
@login_required
def books(isbn):
    # query database to get book data
    book = db.execute('select * from books where isbn = :isbn', {"isbn":isbn}).fetchone()
     
    # query goodreads apis(goodreads, bookrack) for average rating and number of ratings
    book_data = api_book(book, isbn)
    reviews = db.execute('''select id, isbn_id, name, review, rating from 
                            users 
                              join 
                            (select user_id, isbn_id, review, rating 
                             from reviews where isbn_id=:isbn) 
                             as isbn_reviews
                             on id = isbn_reviews.user_id;''',
                             {"isbn":isbn}).fetchall()
    # print(reviews)
    rack_data = {}
    this_has_review = check_user(reviews);
    print(this_has_review)
    if reviews:
        counter = 0;
        sum = 0;
        for review in reviews:
            counter += 1
            sum += review['rating']
        avg = sum / counter
        rack_data['rack_avg'] = f'{avg:.2f}'
        rack_data['rack_reviews'] = counter
    return render_template('books.html', book=book_data, reviews=reviews, 
                            rack=rack_data, this_has_review=this_has_review)

@books_bp.route('/add/<string:isbn>', methods=['POST'])
def add(isbn):
    if request.method == 'POST':
        rating = int(request.form.get('rating'))
        review = request.form.get('review')
        db.execute('''insert into reviews(isbn_id,user_id,review,rating)
                    values(:isbn,:user_id,:review,:rating)''',
                    {"isbn":isbn,"user_id":session['user_id'],
                    "review":review,"rating":rating})
        db.commit()
        flash(f'Added review for book with isbn {isbn}')
        return redirect('/')