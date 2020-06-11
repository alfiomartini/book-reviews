from flask import Blueprint, jsonify, abort
from database import db

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/api/<string:isbn>', methods=['GET'])
def api(isbn):
    # query database to get book data
    book = db.execute('select * from books where isbn = :isbn', {"isbn":isbn}).fetchone()
    if book:
        # print(book_data)
        book_api = dict(book.items())
        reviews = db.execute('''select review, rating from reviews 
                                where isbn_id=:isbn''',
                            {"isbn":isbn}).fetchall()
        print(reviews)
        if reviews:
            counter = 0;
            sum = 0;
            for review in reviews:
                counter += 1
                sum += review['rating']
            avg = sum / counter
            book_api['review_count'] = counter
            book_api['average_score'] = float(f'{avg:.1f}')
        else:
            book_api['review_count'] = 0
            # book_api['average_score'] = '-'
        return jsonify(book_api), 200, {'Content-Type': 'application/json'}
    else:
         abort(404)