from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from models import db
from user_operations import add_user
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


if __name__ == '__main__':    
    app.run(debug=True)
    