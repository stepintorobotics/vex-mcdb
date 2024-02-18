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
    events = re_fetch.fetch_data("events", {"region": "United Kingdom", "season": [180]})
    events.extend(re_fetch.fetch_data("events", {"region": "United Kingdom", "season": [181]}))
    mc_database.insert_events(events, connection)
    connection.close()
    return "OK"

@app.route("/refresh/teams")
def refresh_teams():
    connection = mc_database.connect("indev.db")
    teams = re_fetch.fetch_data("teams", {"country": "GB", "program": [1], "registered": True})
    teams.extend(re_fetch.fetch_data("teams", {"country": "GB", "program": [41], "registered": True}))
    mc_database.insert_teams(teams, connection)
    connection.close()
    return "OK"

@app.route("/refresh/events/awards")
def refresh_awards():
    connection = mc_database.connect("indev.db")
    cursor = connection.cursor()
    cursor.execute("SELECT event_id FROM events")
    events = cursor.fetchall()
    for event in events:
        awards = re_fetch.fetch_data(f"events/{event[0]}/awards", {})
        mc_database.insert_awards(awards, connection)
    connection.close()
    return "OK"

if __name__ == "__main__":
    connection = mc_database.connect("indev.db")
    mc_database.program_init(connection)
    connection.close()
    app.run(debug=True)