import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
import requests


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
        book_dict['good_reviews'] = 0
        book_dict['good_avg'] = 0
    
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
