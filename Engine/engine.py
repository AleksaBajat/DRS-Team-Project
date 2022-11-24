from flask import Flask, request

app = Flask(__name__)

@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        print(f"Name : {name}", flush=True)


if __name__ == '__main__':
    app.run()