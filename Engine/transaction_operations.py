from models import Account, Transaction,User
from schemas import AccountSchema,TransactionSchema
from sqlalchemy import distinct
from user_operations import get_user, get_user_by_email
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process
from Crypto.Hash import keccak
import time
import random


account_schema = AccountSchema()


def get_accounts(app, db, id):
    with app.app_context():
        return db.session.query(Account).filter(Account.user_id==id).all()

def get_currencies(app, db, id):
     with app.app_context():
        return db.session.query(distinct(Account.currency)).filter(Account.user_id==id).all()

def transaction_ui(app,db, id):
    with ThreadPoolExecutor() as executor:
        accounts_future = executor.submit(get_accounts,app, db, id)
        currencies_future = executor.submit(get_currencies, app, db, id)

        accounts = accounts_future.result()
        currencies = currencies_future.result()

        ui_data = {        
            "accounts": [account_schema.dump(account) for account in accounts],
            "currencies": [c[0] for c in currencies]
        }
        return 200, ui_data



def hash_function(sender, recipient, amount):
    bubble = sender + recipient + str(amount) + str(random.randint(1,100000))
    bubble = bubble.encode()
    k = keccak.new(digest_bits=256)
    k.update(bubble)

    return k.hexdigest()

def finish_transaction(db, transaction_id, amount, sender_id, recipient_id):       
    try:
        time.sleep(20)
        state = 'Denied'
        transaction = db.session.query(Transaction).filter_by(id=transaction_id).first()    

        status_sender,sender = get_user(db, {"id":transaction.sender_id})
        status_recipient,recipient = get_user(db, {"id":transaction.recipient_id})

        sender_account = db.session.query(Account).filter_by(user_id=sender_id, currency=transaction.currency).first()

        if float(amount) < float(sender_account.balance):
            sender_account.balance = str(float(sender_account.balance) - float(amount))

            recipient_account = db.session.query(Account).filter_by(user_id=recipient_id,currency=transaction.currency).first()

            if recipient_account is not None:
                recipient_account.balance = str(float(recipient_account.balance) + float(amount))
            else:
                recipient_account = Account(balance=amount,currency='$',user_id=recipient_id)

            db.session.add(sender_account)
            db.session.add(recipient_account)
            
            state = 'Done'

        transaction.state = state
        db.session.add(transaction) 
        db.session.commit()
        print("PROCESS DONE")
    except Exception as e:
        db.session.rollback()
        print(e, flush=True)
    
def create_transaction(db, data):    
    status_sender,sender = get_user(db, data)
    status_recipient,recipient = get_user_by_email(db, data)

    if status_sender == 404 or status_recipient == 404:
        return 404, "Can't find given users."

    amount = data['amount']
    
    transaction_id = hash_function(sender['email'], recipient['email'], amount)

    transaction = Transaction(id=transaction_id,sender_id=sender['id'],recipient_id=recipient['id'], amount=amount, currency=data['currency'])
    db.session.add(transaction)
    db.session.commit()

    process = Process(target=finish_transaction, args=(db, transaction_id, amount, sender['id'], recipient['id']))
    process.start()

    return 200, "Transaction started!"

def get_user_transactions(db, data):
    if data == None:
        return 404, None
    try:
        transactions = db.session.query(Transaction).where((Transaction.sender_id==data['id'])|(Transaction.recipient_id==data['id'])).all()

        exists = transactions is not None
        if exists:
            return 200, transactions
        else:
            return 404, None

    except Exception as e:
        print(e,flush=True)
        return 401,None