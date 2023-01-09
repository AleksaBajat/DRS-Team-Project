from flask import Flask, request, make_response
import sqlite3
from commands import CreateUserTableCommand

app = Flask(__name__)

@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.get_json()
        print(f"Name : {name}", flush=True)
        CreateUserTableCommand()
        return make_response('Added to database!', 200)


if __name__ == '__main__':
    app.run()