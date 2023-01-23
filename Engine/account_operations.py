from flask import jsonify
from models import User, Account
from schemas import AccountSchema

account_schema = AccountSchema()

def transfer_from_card(db, user_id, money):
    status_code = 200

    print(user_id, money, "printing......", flush=True)
    account = db.session.query(Account).filter_by(user_id=user_id, currency='$').first()
    
    if not account:
        return 404
    try:
        value = int(money)
        if value:
            account.balance += value
        db.session.commit()
    except:
        print("Error: ", e, flush=True)
        status_code = 500
        db.session.rollback()

    return status_code

def buy_crypto_with_dollar(db, data):
    status_code = 200
    print(data, flush=True)

    money = float(data['data']['money'])
    rate = float(data['data']['rate'])

    if money is None or rate is None:
        return 400

    real_value = money / rate
    real_value = real_value
    if real_value is None:
        return 401

    try:
        response = subtract_from_account(db, data['id'], money, '$')
        if(response != 200):
            return 500
            
        account = db.session.query(Account).filter_by(user_id=data['id'], currency=data['data']['symbol']).first()

        if not account:
            new_account = Account(user_id=data['id'], balance=real_value, currency=data['data']['symbol'])
            db.session.add(new_account)
            db.session.commit()
            return 201

        else:
            account.balance += real_value
            db.session.commit()
            return 200

    except:
        return 500


def subtract_from_account(db, user_id, value, currency):
    try:
        account = db.session.query(Account).filter_by(user_id=user_id, currency=currency).first()

        if account:
            account.balance -= value
            if(account.balance < 0):
                status_code = 401
                db.session.rollback()
            else:
                status_code = 200
                db.session.commit()

            return status_code

        return 401
    except:
        return 401


def get_user_currencies(db, data):
    if data == None:
        return 404, None
    try:
        accounts = db.session.query(Account).filter_by(user_id= data['id']).all()
        exists = accounts is not None
        if exists:
            data = { "accounts": [account_schema.dump(account) for account in accounts]}
            return 200, data
        else:
            return 404, None

    except:
        return 401

def swap_currencies(db, data):
    status_code = 200
    print(data, flush=True)

    money = float(data['data']['money'])
    rate = float(data['data']['rate'])

    if money is None or rate is None:
        return 400

    to_value = money * rate
    to_value = to_value
    print(to_value)
    if to_value is None:
        return 500

    try:
        response = subtract_from_account(db, data['id'], money, data['data']['fromSymbol'])
        if(response != 200):
            return 500
            
        account = db.session.query(Account).filter_by(user_id=data['id'], currency=data['data']['toSymbol']).first()

        if not account:
            return 500

        else:
            account.balance += to_value
            db.session.commit()
            return 200

    except:
        return 500
