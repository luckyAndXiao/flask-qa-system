from functools import wraps
from flask import g, url_for, redirect
def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        print('g.user:', g.user)
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))

    return inner
