from models import User
from flask_marshmallow import Marshmallow

emmy = Marshmallow()

class UserSchema(emmy.SQLAlchemyAutoSchema):
    class Meta:
        model = User