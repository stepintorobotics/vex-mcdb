from flask import Flask, jsonify
import re_fetch
import mc_database

app = Flask(__name__)
connection = None

@app.route("/")
def index():
    return "Hello, world."

@app.route("/refresh/events")
def refresh_events():
    connection = mc_database.connect("indev.db")
    events = re_fetch.fetch_events(180)
    mc_database.insert_events(events, connection)
    events = re_fetch.fetch_events(181)
    mc_database.insert_events(events, connection)
    return "OK"

@app.route("/refresh/teams")
def refresh_teams():
    connection = mc_database.connect("indev.db")
    teams = re_fetch.fetch_teams(1)
    mc_database.insert_teams(teams, connection)
    teams = re_fetch.fetch_teams(41)
    mc_database.insert_teams(teams, connection)
    return "OK"

if __name__ == "__main__":
    connection = mc_database.connect("indev.db")
    mc_database.program_init(connection)
    app.run(debug=True)