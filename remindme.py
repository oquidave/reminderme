from flask import Flask, render_template, jsonify, request, Response

from remindme import app, db 
from remindme.models import User, Reminder
from datetime import datetime
import secrets
import hashlib

@app.route('/users', methods=['GET'])
def get_users():
	apikey = request.headers.get("apikey")
	user_objs = User.query.all()
	users = []
	for user_obj in user_objs:
		users.append({'id': user_obj.id, 'username': user_obj.username, 'email': user_obj.email,
			'apikey': user_obj.apikey})
	return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
	user_obj = User.query.get(id)
	return jsonify({'username': user_obj.username, 'apikey': user_obj.apikey,
		'email': user_obj.email})

@app.route('/users', methods=['POST'])
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
def delete_users(id):
	return jsonify({'user_id': id})

@app.route('/reminders', methods=['GET'])
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
def get_reminder(id):
	return jsonify({'id': 1,'item': 'dr visit', 'description': 'go for checktup', 
		'date': '23-03-2019'}) 

@app.route('/reminders', methods=['POST'])
def add_reminder():
	apikey = request.headers.get("apikey")
	user = db.session.query(User).filter_by(apikey=apikey).one()
	req = request.get_json()
	item = req['item']
	description = req['description']
	due_date =  datetime.strptime(req['due_date'], '%Y-%m-%d %H:%M:%S')
	reminder = Reminder(item = item, description = description, 
		due_date = due_date)
	user.reminders.append(reminder)
	db.session.add(reminder)
	db.session.commit()
	return Response(response="reminder was added", status=200) 

@app.route('/reminders/<id>', methods=['PUT'])
def update_reminder(id):
	return jsonify({'id': 1,'item': 'dr visit', 'description': 'go for check up', 
		'date': '23-04-2019'})

@app.route('/reminders/<id>', methods=['DELETE'])
def delete_reminder(id):
	return jsonify({'reminder_id': id, 'method': 'delete'}) 