import hashlib
import secrets
from datetime import datetime

from flask import jsonify, request, Response, abort
from remindme.models import User, Reminder

from remindme import app, db
from functools import wraps


def validate_request(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        data = request.get_json()
        if not data:
            abort(400) #http code for Bad request
        return func(*args, **kwargs)
    return decorated_function


def validate_auth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        apikey = request.headers.get('apikey')
        if not apikey:
            abort(401)
        user = db.session.query(User).filter_by(apikey=apikey).one_or_none()
        print(user)
        if not user:
            abort(401)
        return func(*args, **kwargs)
    return decorated_function


def _get_user():
    apikey = request.headers.get("apikey")
    user = db.session.query(User).filter_by(apikey=apikey).one()
    return user


@app.route('/users', methods=['GET'])
@validate_auth
def get_users():
    user_objs = User.query.all()
    users = []
    for user_obj in user_objs:
        users.append({'id': user_obj.id, 'username': user_obj.username, 'email': user_obj.email,
                      'apikey': user_obj.apikey})
    return jsonify(users)


@app.route('/users/<id>', methods=['GET'])
@validate_auth
def get_user(id):
    user_obj = User.query.get(id)
    return jsonify({'username': user_obj.username, 'apikey': user_obj.apikey, 'email': user_obj.email})


@app.route('/users', methods=['POST'])
@validate_auth
@validate_request
def add_user():
    req = request.get_json()
    username = req['username']
    password = req['password']
    email = req['email']
    apikey = secrets.token_hex(16)

    user_obj = User(username=username, apikey=apikey, email=email,
                    password=hashlib.md5(password.encode('utf8')).hexdigest())
    db.session.add(user_obj)
    db.session.commit()
    return jsonify({'username': username, 'email': email, 'apikey': apikey})


@app.route('/users/<id>', methods=['DELETE'])
@validate_auth
def delete_users(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return Response(response="user was deleted", status=200)


@app.route('/reminders', methods=['GET'])
@validate_auth
def get_reminders():
    apikey = request.headers.get("apikey")
    user = db.session.query(User).filter_by(apikey=apikey).one()
    _reminders = user.reminders.all()
    reminders = []
    for reminder in _reminders:
        reminders.append({'id': reminder.id, 'item': reminder.item,
                          'due_date': reminder.due_date})
    return jsonify(reminders)


@app.route('/reminders/<id>', methods=['GET'])
@validate_auth
def get_reminder(id):
    reminder = Reminder.query.get(id)
    return jsonify({'id': reminder.id, 'item': reminder.item, 'due_date': reminder.due_date})


@app.route('/reminders', methods=['POST'])
@validate_auth
@validate_request
def add_reminder():
    user = _get_user()
    req = request.get_json()
    item = req['item']
    description = req['description']
    due_date = datetime.strptime(req['due_date'], '%Y-%m-%d %H:%M:%S')
    reminder = Reminder(item=item, description=description,
                        due_date=due_date)
    user.reminders.append(reminder)
    db.session.add(reminder)
    db.session.commit()
    return Response(response="reminder was added", status=200)


@app.route('/reminders/<id>', methods=['PUT'])
@validate_auth
@validate_request
def update_reminder(id):
    user = _get_user()
    req = request.get_json()

    reminder = Reminder.query.get(id)
    reminder.item = req['item']
    reminder.description = req['description']
    reminder.due_date = datetime.strptime(req['due_date'], '%Y-%m-%d %H:%M:%S')

    user.reminders.append(reminder)
    db.session.add(reminder)
    db.session.commit()
    return Response(response="reminder was updated", status=200)


@app.route('/reminders/<id>', methods=['DELETE'])
@validate_auth
def delete_reminder(id):
    reminder = Reminder.query.get(id)
    db.session.delete(reminder)
    db.session.commit()
    return Response(response="reminder was deleted", status=200)
