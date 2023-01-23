from models import User, Account
from schemas import UserSchema

user_schema = UserSchema()

def login_user(db, user_data):
    print("user_data:", user_data, flush=True)

    user = db.session.query(User).filter_by(email=user_data['email'], password=user_data['password']).first()    

    exists = user is not None

    if exists:
        user_id = user.id
        return 200, user_id
    else:
        return 404, None


def get_user(db, data):
    print("user_data:", data, flush=True)
    
    if data == None:
        return 404, None

    user = db.session.query(User).filter_by(id=data['id']).first()    

    exists = user is not None

    if exists:
        user = user_schema.dump(user)
        return 200, user
    else:
        return 404, None

def get_user_by_email(db, data):
    print("data:", data, flush=True)

    if data == None:
        return 404, None

    user = db.session.query(User).filter_by(email=data['email']).first()    

    exists = user is not None

    if exists:
        user = user_schema.dump(user)
        return 200, user
    else:
        return 404, None


def add_user(db,user_data):    
    print("user_data:", user_data, flush=True)

    exists = db.session.query(User.email).filter_by(email=user_data['email']).first() is not None

    if exists:
        print("user alredy exists!", flush=True)
        return 409

    new_user = User(name=user_data['name'], lastName=user_data['lastName'], email=user_data['email'], address=user_data['address'],city=user_data['city'], country=user_data['country'], phoneNumber=user_data['phoneNumber'],password=user_data['password'])    

    try:
        db.session.add(new_user)        
        db.session.flush()
        new_account = Account(user_id=new_user.id, balance=0, currency='$')
        db.session.add(new_account)
        db.session.commit()
        status_code = 200
    except Exception as e:
        print("Error: ", e, flush=True)
        status_code = 500
        db.session.rollback()

    return status_code

def update_user(db,user_data):  
    status_code = 200

    try:  
        print("user_data:", user_data, flush=True)

        user = User.query.filter_by(id=user_data['id']).first()

        if not (user_data['password'] != "" and user_data['repeatPassword'] != "" and user_data['password'] == user_data['repeatPassword']):            
            del user_data['password']
            
        del user_data['repeatPassword']

        exists = db.session.query(User).filter_by(id=user_data['id']).first() is not None

        if exists:
            User.query.filter_by(id=user_data['id']).update(user_data)    
        else: 
            status_code = 404
                
        db.session.commit()    
    except Exception as e:
        print(e, flush=True)
        db.session.rollback()
        status_code = 500

    return status_code

def verify_user(db, data):
    status_code = 200

    print(data, flush=True)
    user_id = data['id']

    try:  
        print("user_id:", user_id, flush=True)

        user = db.session.query(User).filter_by(id=user_id).first()
        if user:
            if not is_valid_card(data['data'], user.name):
                return 401

            user.verified = True
        else: 
            status_code = 404
                
        db.session.commit()
    except Exception as e:
        print(e, flush=True)
        status_code = 500

    return status_code
    
def is_valid_card(data, user_name):
    valid = True
    if(data['cardNumber'] != '4242-4242-4242-4242'):
        valid = False
    if(data['month'] != '2'):
        valid = False
    if(data['year'] != '23'):
        valid = False
    if(data['csc'] != '123'):
        valid = False
    if(data['name'] != user_name):
        valid = False

    return valid
    
