from flask import Flask, render_template,url_for

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/check')
def check():
    return "200 - OK - UI is up!"

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()