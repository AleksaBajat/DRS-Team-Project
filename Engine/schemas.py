from models import User, Account, Transaction
from flask_marshmallow import Marshmallow

emmy = Marshmallow()


class UserSchema(emmy.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class AccountSchema(emmy.SQLAlchemyAutoSchema):
    class Meta:
        model = Account

class TransactionSchema(emmy.SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction