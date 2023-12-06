from functools import wraps
from flask import abort, redirect, url_for, make_response
from flask_login import current_user
from .models import User

def user_login_required(user):
    def decorator(func):
        # return make_response(current_user.role)
        @wraps(func)
        def decorated_view(*args, **kwargs):
            # return make_response(current_user.role)
            if current_user.is_anonymous:
                return make_response("fix the role issue")
                return make_response('Unauthorized', 401)
            return func(*args, **kwargs)
        return decorated_view
    return decorator

            # if current_user.is_anonymous or current_user.role != role:
            # if not current_user.is_authenticated or current_user.role != role:
