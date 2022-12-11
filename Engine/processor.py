from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from daoModel import *


def register(data):
    try:
        engine = create_engine("sqlite:///mydb.db", echo=True)
        Session = sessionmaker(bind=engine)
        with Session() as session:
            temp = data
            model = Register(temp.first_name, temp.last_name, temp.email, temp.address, temp.city, temp.country, temp.phone, temp.password)
            
            result = session.query(Register).filter(Register.email == model.email).first()
            if result:
                return StatusCode.ERROR

            session.add(model)
            session.commit()

        return StatusCode.SUCCESS
        
    except:
        return StatusCode.INTERNAL_SERVER_ERROR