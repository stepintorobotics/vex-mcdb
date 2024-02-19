from flask import Flask, jsonify
import re_fetch
import mc_database

app = Flask(__name__)
connection = None

# Index
@app.route("/")
def index():
    return "MCDb API"

# Refreshes all event data (excl. matches, awards) in the UK
@app.route("/refresh/events")
def refresh_events():
    connection = mc_database.connect("indev.db")
    # Fetch data
    events = re_fetch.fetch_data("events", {"region": "United Kingdom", "season[]": [180, 181]})
    # Insert data into database
    mc_database.insert_events(events, connection)
    connection.close()
    return "OK"

# Refreshes all team data (excl. matches, awards) in the UK
@app.route("/refresh/teams")
def refresh_teams():
    connection = mc_database.connect("indev.db")
    # Fetch data
    teams = re_fetch.fetch_data("teams", {"country": "GB", "program[]": [1, 41], "registered": True})
    # Insert data into database
    mc_database.insert_teams(teams, connection)
    connection.close()
    return "OK"

# Refreshes award data from all stored events
@app.route("/refresh/events/awards")
def refresh_awards():
    connection = mc_database.connect("indev.db")
    # Retrieve list of known events
    cursor = connection.cursor()
    cursor.execute("SELECT event_id FROM events")
    events = cursor.fetchall()
    # Fetch and insert awards from all known events
    for event in events:
        awards = re_fetch.fetch_data(f"events/{event[0]}/awards", {})
        mc_database.insert_awards(awards, connection)
    connection.close()
    return "OK"

# Refreshes match data from all stored events
@app.route("/refresh/events/matches")
def refresh_matches():
    connection = mc_database.connect("indev.db")
    # Retrieve list of known events
    cursor = connection.cursor()
    cursor.execute("SELECT event_id, event_divisions FROM events")
    events = cursor.fetchall()
    # Fetch and insert matches from all known events
    for event, num_divisions in events:
        for division in range(1, num_divisions + 1):
            matches = re_fetch.fetch_data(f"events/{event}/divisions/{division}/matches", {})
            mc_database.insert_matches(matches, connection)
    connection.close()
    return "OK"

# Refreshes match data from event specified by ID
@app.route("/refresh/events/id/<int:id>/matches")
def refresh_matches_id(id):
    connection = mc_database.connect("indev.db")
    # Select event from events table
    cursor = connection.cursor()
    cursor.execute("SELECT event_id, event_divisions FROM events WHERE event_id = ?", (id,))
    events = cursor.fetchone()
    # Fetch and insert matches from selected event
    for event, num_divisions in events:
        for division in range(1, num_divisions + 1):
            matches = re_fetch.fetch_data(f"events/{event}/divisions/{division}/matches", {})
            mc_database.insert_matches(matches, connection)
    connection.close()
    return "OK"

# Return notes for team specified by ID
@app.route("/notes/id/<int:id>")
def notes_id(id):
    connection = mc_database.connect("indev.db")
    cursor = connection.cursor()
    cursor.execute("SELECT note_data FROM notes WHERE note_team = ?", (id,))
    notes = cursor.fetchall()
    return jsonify(notes)

if __name__ == "__main__":
    connection = mc_database.connect("indev.db")
    # Initialise database if it does not already exist
    mc_database.program_init(connection)
    connection.close()
    app.run(debug=True)