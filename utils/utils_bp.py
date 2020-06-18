from flask import Blueprint, render_template, request, jsonify
from helpers import login_required
from database import db

utils_bp = Blueprint('utils_bp', __name__)

# Utility Routes
@utils_bp.route("/check", methods=["GET"])
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

@utils_bp.route('/search/<string:term>', methods=['GET'])
@login_required
def search(term):
    term = term.lower()
    try:
        year = int(term)
    except:
        year = None;

    term = "%" + term + "%" 
    print(term)
    
    if year:
        sql_search = '''select  isbn, title, author, year from books 
                            where  lower(isbn) like :term or lower(title) like :term or 
                            lower(author) like :term or year = :year 
                            order by title'''
    else:
        sql_search = '''select  isbn, title, author, year from books 
                            where  lower(isbn) like :term or lower(title) like :term or 
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
