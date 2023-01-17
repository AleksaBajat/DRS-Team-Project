from flask import Flask, request, make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db
from user_operations import add_user, login_user, get_user, update_user
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_chiefs.db'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        status_code = add_user(db, data)
        return make_response('Register',status_code)

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()

        status_code, user_id = login_user(db, data)  

        if status_code == 200:
            return make_response(jsonify(user_id=user_id), status_code)
        else:
            return make_response('Login failed', status_code)

@app.route("/user")
def user():
    if request.method == 'GET':
        data = request.get_json()

        print(data, flush=True)

        status_code, user = get_user(db, data)

        if status_code == 200:
            return make_response(jsonify(user), status_code)
        else:
            return make_response('Get user failed.', status_code)


@app.route("/updateUser", methods=['POST'])
def update():
    data = request.get_json()
    status_code = update_user(db, data)
    return make_response('Update user',status_code)

if __name__ == '__main__':    
    app.run(debug=True)    