import jwt
from flask import request
from six import wraps

from app import app
from app.repositories.user_repository import UserRepository


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user_repository = UserRepository()

        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[-1]

        if not token:
            return {
                "message": "Invalid or missing Authentication token!",
            }, 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = user_repository.get_by_id(data['id'])
            if current_user is None:
                return {
                    "message": "Invalid or missing Authentication token!",
                }, 401
        except Exception as e:
            print(e)
            return {"message": "Invalid or missing Authentication token!"}, 401

        return f(current_user=current_user, *args, **kwargs)

    return decorator
