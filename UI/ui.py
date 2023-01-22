from flask import Flask, render_template,url_for,request, make_response, session, redirect
from flask_session import Session
import requests
import json


crypto_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'10',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '1deb7305-08f6-40aa-82aa-b64f5ae29c49',
}

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

@app.route('/buyCrypto', methods=['GET', 'POST'])
def buy_crypto():
    id = session.get('user_id')

    if request.method == 'GET':
        data = ''
        try:
            print('hello', flush=True)
            response = requests.get(crypto_url, params=parameters, headers=headers)
            print('hello2', flush=True)
            data = json.loads(response.text)
        except:
            print("Error while fetching data", flush=True)

        values = {
            "user_id" : session.get('user_id'),
            "data" : data
        }

        return render_template('buyCrypto.html', **values)

    elif request.method == 'POST':
        data = request.form
        print(data, flush=True)

        url = "http://engine:8081/buyCrypto"
        values = {
            'id' : id,
            'data' : data
        }
        response = requests.post(url, json=values)
        print(response, flush=True)
        if(response.status_code != 200 and response.status_code != 201):
            return make_response("Internal server error", response.status_code)
        else:
            return render_template('index.html')



@app.route('/transferFromCard', methods=['POST'])
def transfer_money_from_card():
    id = session.get('user_id')
    if(request.method == 'POST'):
        url = "http://engine:8081/transferFromCard"
        values = {
            "data": request.form,
            "id": id
        }
        print(values, flush=True)
        response = requests.post(url, json=values)
        if response.status_code == 200:
            return render_template('index.html')
        else:
            return make_response("Internal server error", response.status_code)


@app.route('/card', methods=['GET', 'POST'])
def add_card():
    id = session.get('user_id')    

    if(request.method == 'GET'):
        url = "http://engine:8081/user"
        response = requests.get(url,json={'id': id})    

        if response.status_code == 200:
            res = response.json()
            session['verified'] = res['verified']
        else:
            session['verified'] = False

        values = {
                "user_id" : session.get('user_id'),
                "verified" : session.get('verified')
            }
        return render_template('card.html', **values)

    if(request.method == 'POST'):
        url = "http://engine:8081/verify"
        values = {
            "data": request.form,
            "id": id
        }
        print(values, flush=True)
        response = requests.post(url, json=values)
        if response.status_code == 200:
            return render_template('index.html')
        else:
            return make_response("Internal server error", response.status_code)


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
    urlCurrencies = "http://engine:8081/userCurrencies"

    response = requests.get(url,json={'id': id})    
    responseCurrencies = requests.get(urlCurrencies,json={'id': id})

    if response.status_code == 200 and responseCurrencies.status_code==200:
        values = {
            "user_id" : id
        }
        res = response.json() 
        currencies= responseCurrencies.json()
        return render_template('profile.html', user=res,currencies=currencies['accounts'], **values)
    
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
            

if __name__ == '__main__':
    app.run()