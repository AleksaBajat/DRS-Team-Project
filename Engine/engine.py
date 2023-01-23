from flask import Flask, request, make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
from account_operations import transfer_from_card, buy_crypto_with_dollar, swap_currencies
from models import db
from user_operations import add_user, login_user, get_user, update_user, verify_user
from transaction_operations import transaction_ui, create_transaction
from account_operations import get_user_currencies
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

@app.route("/userCurrencies")
def userCurrencies():
    if request.method == 'GET':
        data = request.get_json()

        print(data, flush=True)

        status_code, accounts = get_user_currencies(db, data)

        if status_code == 200:
            return make_response(jsonify(accounts), status_code)
        else:
            return make_response('Get accounts failed.', status_code)

@app.route("/updateUser", methods=['POST'])
def update():
    data = request.get_json()
    status_code = update_user(db, data)
    return make_response('Update user',status_code)


@app.route("/transaction/ui", methods=['GET'])
def transaction_ui_data():
    data = request.get_json()    

    status_code, ui_data = transaction_ui(db, data['id'])

    if status_code == 200:
        return make_response(jsonify(ui_data), status_code)
    else:
        return make_response('Get user failed.', status_code)

@app.route('/transaction', methods=["POST"])
def transaction():
    if request.method == "POST":
        data = request.get_json() 

        status_code, response = create_transaction(db, data)

        return make_response(response, status_code)

@app.route("/verify", methods=['POST'])
def verify():
    if request.method == 'POST':
        data = request.get_json()
        print(data, flush=True) 
        status_code = verify_user(db, data['id'])
        if status_code == 200:
            return make_response('User verified', status_code)
        else:
            return make_response('User not verified', status_code)

@app.route("/transferFromCard", methods=['POST'])
def transfer_from_card_to_account():
    if(request.method == 'POST'):
        data = request.get_json()
        status_code = transfer_from_card(db, data['id'], data['data']['money'])
        if status_code == 200:
            return make_response('Successifully transfered', status_code)
        else:
            return make_response('Money not transfered', status_code)


@app.route("/swapCrypto", methods=['POST'])
def swap_crypto():
    if(request.method == 'POST'):
        data = request.get_json()
        status_code = swap_currencies(db, data)
        if status_code != 200:
            return make_response('Currencies not swapped', status_code)
        else:
            return make_response('Success', status_code)

@app.route("/buyCrypto", methods=['POST'])
def buy_crypto():
    if(request.method == 'POST'):
        data = request.get_json()
        status_code = buy_crypto_with_dollar(db, data)
        if(status_code != 200 and status_code != 201):
            return make_response('Internal server error', status_code)
        else:
            return make_response('Success', status_code)



if __name__ == '__main__':    
    app.run(debug=True)    