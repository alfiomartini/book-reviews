from flask import Blueprint, render_template, request
from flask import flash, redirect, session
# from flask_session import Session
from helpers import apology, login_required, search_reviews
from database import db

edit_bp = Blueprint('edit_bp', __name__, template_folder='templates',
              static_folder='static', static_url_path='/edit_static')

@edit_bp.route("/edit")
@login_required
def edit():
    user_reviews = search_reviews()
    if user_reviews['found']:
        flash('Select one of the books to edit your review.')
        return render_template('edit.html', books=user_reviews['books'])
    else:
        message = 'No book reviews found for this user.'
        return render_template('empty.html', message=message)

@edit_bp.route("/edit_review", methods=['POST'])
@login_required
def edit_review():
    if request.method == 'POST':
        rating = request.form.get('rating')
        review = request.form.get('review')
        isbn_id = request.form.get('isbn')
        user_id = session['user_id']
        db.execute('''update reviews set review=:review, rating=:rating
                    where user_id =:user_id and isbn_id =:isbn_id''',
                    {"review": review, "rating": rating, 
                    "isbn_id":isbn_id, "user_id":user_id})
        db.commit()
        flash(f'Review and rating for book with isbn : {isbn_id} updated.')
        return redirect('/')