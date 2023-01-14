from flask import Flask, render_template,url_for,request, make_response
import requests

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    return render_template('index.html')

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
        url = "http://engine:8081/register"

        response = requests.post(url, json=request.form)

        
        if response.status_code == 409:
            return make_response('Unable to register. Email already exists!', 409)
        elif 200:
            return make_response('Successful registration!', 200)
            

        return make_response('Unable to register. Server error!', 500)

if __name__ == '__main__':
    app.run()