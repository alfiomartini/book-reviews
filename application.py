import os

from flask import Flask, render_template, session
from flask_session import Session
from helpers import login_required

from auth.auth_bp import auth_bp
from edit.edit_bp import edit_bp
from remove.remove_bp import remove_bp
from books.books_bp import books_bp
from api.api_bp import api_bp
from utils.utils_bp import utils_bp

from database import db


app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(edit_bp)
app.register_blueprint(remove_bp)
app.register_blueprint(books_bp)
app.register_blueprint(api_bp)
app.register_blueprint(utils_bp)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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


@app.route("/")
@login_required
def index():
    return render_template('index.html')


@app.route('/readme')
@login_required
def readme():
    return render_template('readme.html')


if __name__ == '__main__':
    app.run(debug=False)
