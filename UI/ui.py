from flask import Flask, render_template,url_for,request, make_response, session, redirect
from flask_session import Session
import requests
import json

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 1800
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
@app.route('/index')
def index():
    values = {
            "user_id" : session.get('user_id')
        }
    return render_template('index.html', **values)

@app.route('/check')
def check():
    return "200 - OK - UI is up!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':                
        values = {
            "user_id" : session.get('user_id')
        }

        return render_template('login.html', **values)

    elif request.method == 'POST':
        url = "http://engine:8081/login"

        response = requests.post(url, json=request.form)

        if response.status_code == 200:
            res = response.json()
            print(res['user_id'], flush=True)            
            session['user_id'] = res['user_id']
            return render_template('index.html')
        elif response.status_code == 404:
            return make_response('Login unsuccessful. Check your credentials and try again!', 404)

        return make_response('Login unsuccessful. Server error.', 500)

@app.route('/profile')
def profile():
    id = session.get('user_id')    
    url = "http://engine:8081/user"
    
    response = requests.get(url,json={'id': id})    

    if response.status_code == 200:
        values = {
            "user_id" : id
        }
        res = response.json()        
        return render_template('profile.html', user=res, **values)
    
@app.route('/logout')
def logout():
    session.clear();      
    return render_template('index.html')
    

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':        
        url = "http://engine:8081/register"

        response = requests.post(url, json=request.form)
                
        if response.status_code == 409:
            return make_response('Unable to register. Email already exists!', 409)
        elif 200:            
            return make_response('Successful registration!', 200)
            

        return make_response('Unable to register. Server error!', 500)

@app.route('/editProfile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'GET':
        id = session.get('user_id')
        if id:
            url = "http://engine:8081/user"

            response = requests.get(url, json={"id":id})

            res = response.json()
            res['user_id'] = id

            print(res, flush=True)

            return render_template('editProfile.html', **res)
        else:
            redirect('/login')
    elif request.method == 'POST':
        url = "http://engine:8081/updateUser"
        
        id = session.get('user_id')

        if id:
            data = dict(request.form)
            data['id'] = id
            response = requests.post(url, json=data)            
                    
            if response.status_code == 200:            
                return make_response('Changes saved!', 200)
            elif response.status_code == 404:
                return make_response('Unable to save changes. User not found!', 404)
                

            return make_response('Unable to save changes. Server error!', 500)
        else:
            redirect('/login')


@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if request.method == 'GET':
        id = session.get('user_id')
        if id:
            url = "http://engine:8081/transaction/ui"

            response = requests.get(url, json={"id":id})

            res = response.json()
            res['user_id'] = id

            print(res, flush=True)

            return render_template('transaction.html', **res)
        else:
            redirect('/login')
    elif request.method == 'POST':
        id = session.get('user_id')
        if id:
            url = "http://engine:8081/transaction"            

            data = dict(request.form)
            data['id'] = id

            print("TRANSACTION DATA " + str(data), flush=True)

            response = requests.post(url, json=data)

            if response.status_code == 200:            
                return make_response('Transaction in progress!', 200)
            elif response.status_code == 404:
                return make_response('Unable to begin the transaction!', 400)                      
            

if __name__ == '__main__':
    app.run()