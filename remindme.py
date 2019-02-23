from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
	apikey = request.headers.get("apikey")
	return jsonify({'username': 'oquidave', 'apikey': apikey})

@app.route('/users', methods=['POST'])
def add_users():
	username = request.form['username'].strip()
	password = request.form['password'].strip()
	full_names = request.form['full_names'].strip()
	return jsonify({'username': username, 'password': password,
		'full_names': full_names})

@app.route('/users/<id>', methods=['DELETE'])
def delete_users(id):
	return jsonify({'user_id': id})

@app.route('/reminders', methods=['GET'])
def get_reminders():
	pass 

@app.route('/reminders/<id>', methods=['GET'])
def get_reminder(id):
	return jsonify({'reminder_id': id, 'method': 'get'}) 

@app.route('/reminders', methods=['POST'])
def add_reminder():
	pass 

@app.route('/reminders/<id>', methods=['PUT'])
def update_reminder(id):
	pass

@app.route('/reminders/<id>', methods=['DELETE'])
def delete_reminder(id):
	return jsonify({'reminder_id': id, 'method': 'delete'}) 

if __name__ == '__main__':
  app.run(debug=True, host = "0.0.0.0", port=int(4000))
