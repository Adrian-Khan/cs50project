import requests
import re

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code):
    return render_template("error.html", message=message, code=code)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def formatTag(tag):
    words = re.findall('[A-Z][^A-Z]*', tag)
    formatted_tag = ' '.join(words)
    return formatted_tag
