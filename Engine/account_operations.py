from flask import jsonify
from models import User, Account
from schemas import AccountSchema

account_schema = AccountSchema()

def transfer_from_card(db, user_id, money):
    status_code = 200

    print(user_id, money, "printing......", flush=True)
    account = db.session.query(Account).filter_by(id=user_id, currency='$').first()
    
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

