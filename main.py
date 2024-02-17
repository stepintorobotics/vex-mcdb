from flask import Flask, jsonify
import re_fetch
import mc_database

app = Flask(__name__)
connection = None

@app.route("/")
def index():
    return "Hello, world."

@app.route("/test")
def test():
    events = re_fetch.fetch_test()
    return events

if __name__ == "__main__":
    connection = mc_database.connect("indev.db")
    mc_database.program_init(connection)
    app.run(debug=True)