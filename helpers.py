import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
import requests
from database import db

def check_user(reviews):
    print(session['username'])
    for review in reviews:
        print(review['name'])
        if review['name'] == session['username']:
            return 'yes'
    return 'no'

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

        
def api_book(book, isbn):
    GOODREADS_KEY = 'wKy3eEHxspfhDj5YJ5POHw'
    try:
        resp = requests.get("https://www.goodreads.com/book/review_counts.json",
            params={"key": GOODREADS_KEY, "isbns": isbn})
        resp_obj = resp.json()
        book_dict = dict(book.items())
        book_dict['good_reviews'] = resp_obj['books'][0]['work_ratings_count']
        book_dict['good_avg'] = resp_obj['books'][0]['average_rating']
    except:
        book_dict = dict(book.items())
        # book_dict['good_reviews'] = 0
        # book_dict['good_avg'] = 0
    
    return book_dict
    

def shorten_title(title, size):
    short = title.lower().capitalize()[:size]
    if len(title) > size:
        short += '...'
    return short

def apology(message):
    return render_template("apology.html", message=message)


def login_required(f):
    """
    Decorate routes to require login.
    https://www.datacamp.com/community/tutorials/decorators-python
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        # We use session.get("user_id") to check if the key exists in the session.
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper
