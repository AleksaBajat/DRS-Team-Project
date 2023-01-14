from models import User

def add_user(db,user_data):    
    print("user_data:", user_data, flush=True)

    exists = db.session.query(User.email).filter_by(email=user_data['email']).first() is not None

    if exists:
        print("user alredy exists!", flush=True)
        return 409

    new_user = User(name=user_data['name'], lastName=user_data['lastName'], email=user_data['email'], address=user_data['address'],city=user_data['city'], country=user_data['country'], phoneNumber=user_data['phoneNumber'],password=user_data['password'])    

    try:
        db.session.add(new_user)
        db.session.commit()
        status_code = 200
    except Exception as e:
        print("Error: ", e, flush=True)
        status_code = 500
        db.session.rollback()
        
    return status_code