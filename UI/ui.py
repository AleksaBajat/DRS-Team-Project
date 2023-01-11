from flask import Flask, render_template,request
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

@app.route('/profile')
def profile():
    url = "http://engine:8081/profile"
    response = requests.get(url)
    return render_template('profile.html', username=response.text)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':        
        url = "http://engine:8081/register"

        response = requests.post(url, json=request.form)
        return response.text

if __name__ == '__main__':
    app.run()