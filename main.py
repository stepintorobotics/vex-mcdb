from flask import Flask, jsonify
import re_fetch

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, world."

@app.route("/test")
def test():
    events = re_fetch.fetch_test()
    return events

if __name__ == "__main__":
    app.run(debug=True)
