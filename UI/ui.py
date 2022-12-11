from flask import Flask, render_template,url_for,request

from comunication import send_registration
from dtoModel import *

PORT = 5005
HOST = "127.0.0.1"

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/check')
def check():
    return "200 - OK - UI is up!"

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        first_name = request.form['name'] 
        last_name = request.form['lastName'] 
        email = request.form['email'] 
        address = request.form['address'] 
        city = request.form['city'] 
        country = request.form['country'] 
        phoneNumber = request.form['phoneNumber'] 
        password = request.form['password'] 

        data = RegisterDto(first_name, last_name, email, address, city, country, phoneNumber, password)
        response = send_registration(data, HOST, PORT)
        return response

if __name__ == '__main__':
    app.run()