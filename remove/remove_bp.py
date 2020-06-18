from flask import Blueprint, render_template, request
from flask import flash, redirect, session
from helpers import apology, login_required, search_reviews
from database import db


remove_bp = Blueprint('remove_bp', __name__, template_folder='templates',
              static_folder='static', static_url_path='/remove_static')


@remove_bp.route("/remove")
@login_required
def remove():
    user_reviews = search_reviews()
    if user_reviews['found']:
        flash('Select one of the books to delete your review.')
        return render_template('remove.html', books=user_reviews['books'])
    else:
        message = 'No book reviews found for this user.'
        return render_template('empty.html', message=message)


@remove_bp.route("/remove_review", methods=['POST'])
@login_required
def remove_review():
    if request.method == 'POST':
        isbn_id = request.form.get('isbn')
        user_id = session['user_id']
        db.execute('''delete from reviews 
                    where user_id =:user_id and isbn_id =:isbn_id''',
                    {"isbn_id":isbn_id, "user_id":user_id})
        db.commit()
        flash(f'Review and rating for book with isbn : {isbn_id} removed.')
        return redirect('/')
