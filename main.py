from flask import Flask, jsonify
from flask_cors import CORS
import re_fetch
import mc_database

app = Flask(__name__)
CORS(app)
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
    cursor.execute("SELECT event_divisions FROM events WHERE event_id = ?", (id,))
    num_divisions = cursor.fetchone()[0]
    # Fetch and insert matches from selected event
    for division in range(1, num_divisions + 1):
        matches = re_fetch.fetch_data(f"events/{id}/divisions/{division}/matches", {})
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

# Return teams IDs for a match
@app.route("/match/<int:event>/<int:div>/<int:match_type>/<int:match_inst>/<int:match_num>")
def match_teams(event, div, match_type, match_inst, match_num):
    connection = mc_database.connect("indev.db")
    cursor = connection.cursor()
    response = mc_database.match_teams(event, div, match_type, match_inst, match_num, cursor)
    return jsonify(response)

# Return full statistics for one team
@app.route("/stats/<int:event>/<int:team>")
def stats_single(event, team):
    connection = mc_database.connect("indev.db")
    cursor = connection.cursor() 
    response = {
        "season": mc_database.event_season(event, cursor),
        "teams": {
            "red1": {
                "team_name": mc_database.team_name(team, cursor),
                "team_number": mc_database.team_number(team, cursor),
                "team_robot": mc_database.team_robot(team, cursor),
                "team_grade": mc_database.team_grade(team, cursor),
                "team_organisation": mc_database.team_organisation(team, cursor),
                "team_city": mc_database.team_city(team, cursor),
                "points_total": mc_database.team_total_points(team, cursor),
                "points_event": mc_database.team_event_points(team, event, cursor),
                "points_avg_total": int(mc_database.team_total_points(team, cursor) / mc_database.team_matches_total(team, cursor)),
                "points_avg_event": int(mc_database.team_event_points(team, event, cursor) / mc_database.team_matches_event(team, event, cursor)),
                "matches_total": mc_database.team_matches_total(team, cursor),
                "matches_event": mc_database.team_matches_event(team, event, cursor),
                "wins_total": mc_database.team_wins_total(team, cursor),
                "wins_event": mc_database.team_wins_event(team, event, cursor),
                "wins_pct_total": int((mc_database.team_wins_total(team, cursor) / mc_database.team_matches_total(team, cursor)) * 100),
                "wins_pct_event": int((mc_database.team_wins_event(team, event, cursor) / mc_database.team_matches_event(team, event, cursor)) * 100),
                "team_hs_total": mc_database.team_hs_total(team, cursor),
                "team_hs_event": mc_database.team_hs_event(team, event, cursor),
                "team_hs_total_match": mc_database.team_hs_total_match(team, mc_database.team_hs_total(team, cursor), cursor),
                "team_hs_event_match": mc_database.team_hs_event_match(team, event, mc_database.team_hs_event(team, event, cursor), cursor),
                "awards": mc_database.awards(team, cursor)
            }
        }
    }
    connection.close()
    return jsonify(response)

# Return full statistics for four teams (typical VRC match)
@app.route("/stats/<int:event>/<int:team1>/<int:team2>/<int:team3>/<int:team4>")
def stats_vrc(event, team1, team2, team3, team4):
    connection = mc_database.connect("indev.db")
    cursor = connection.cursor() 
    response = {
        "season": mc_database.event_season(event, cursor),
        "teams": {
            "red1": {
                "team_name": mc_database.team_name(team1, cursor),
                "team_number": mc_database.team_number(team1, cursor),
                "team_robot": mc_database.team_robot(team1, cursor),
                "team_grade": mc_database.team_grade(team1, cursor),
                "team_organisation": mc_database.team_organisation(team1, cursor),
                "team_city": mc_database.team_city(team1, cursor),
                "points_total": mc_database.team_total_points(team1, cursor),
                "points_event": mc_database.team_event_points(team1, event, cursor),
                "points_avg_total": int(mc_database.team_total_points(team1, cursor) / mc_database.team_matches_total(team1, cursor)),
                "points_avg_event": int(mc_database.team_event_points(team1, event, cursor) / mc_database.team_matches_event(team1, event, cursor)),
                "matches_total": mc_database.team_matches_total(team1, cursor),
                "matches_event": mc_database.team_matches_event(team1, event, cursor),
                "wins_total": mc_database.team_wins_total(team1, cursor),
                "wins_event": mc_database.team_wins_event(team1, event, cursor),
                "wins_pct_total": int((mc_database.team_wins_total(team1, cursor) / mc_database.team_matches_total(team1, cursor)) * 100),
                "wins_pct_event": int((mc_database.team_wins_event(team1, event, cursor) / mc_database.team_matches_event(team1, event, cursor)) * 100),
                "team_hs_total": mc_database.team_hs_total(team1, cursor),
                "team_hs_event": mc_database.team_hs_event(team1, event, cursor),
                "team_hs_total_match": mc_database.team_hs_total_match(team1, mc_database.team_hs_total(team1, cursor), cursor),
                "team_hs_event_match": mc_database.team_hs_event_match(team1, event, mc_database.team_hs_event(team1, event, cursor), cursor),
                "awards": mc_database.awards(team1, cursor)
            },
            "red2": {
                "team_name": mc_database.team_name(team2, cursor),
                "team_number": mc_database.team_number(team2, cursor),
                "team_robot": mc_database.team_robot(team2, cursor),
                "team_grade": mc_database.team_grade(team2, cursor),
                "team_organisation": mc_database.team_organisation(team2, cursor),
                "team_city": mc_database.team_city(team2, cursor),
                "points_total": mc_database.team_total_points(team2, cursor),
                "points_event": mc_database.team_event_points(team2, event, cursor),
                "points_avg_total": int(mc_database.team_total_points(team2, cursor) / mc_database.team_matches_total(team2, cursor)),
                "points_avg_event": int(mc_database.team_event_points(team2, event, cursor) / mc_database.team_matches_event(team2, event, cursor)),
                "matches_total": mc_database.team_matches_total(team2, cursor),
                "matches_event": mc_database.team_matches_event(team2, event, cursor),
                "wins_total": mc_database.team_wins_total(team2, cursor),
                "wins_event": mc_database.team_wins_event(team2, event, cursor),
                "wins_pct_total": int((mc_database.team_wins_total(team2, cursor) / mc_database.team_matches_total(team2, cursor)) * 100),
                "wins_pct_event": int((mc_database.team_wins_event(team2, event, cursor) / mc_database.team_matches_event(team2, event, cursor)) * 100),
                "team_hs_total": mc_database.team_hs_total(team2, cursor),
                "team_hs_event": mc_database.team_hs_event(team2, event, cursor),
                "team_hs_total_match": mc_database.team_hs_total_match(team2, mc_database.team_hs_total(team2, cursor), cursor),
                "team_hs_event_match": mc_database.team_hs_event_match(team2, event, mc_database.team_hs_event(team2, event, cursor), cursor),
                "awards": mc_database.awards(team2, cursor)
            },
            "blue1": {
                "team_name": mc_database.team_name(team3, cursor),
                "team_number": mc_database.team_number(team3, cursor),
                "team_robot": mc_database.team_robot(team3, cursor),
                "team_grade": mc_database.team_grade(team3, cursor),
                "team_organisation": mc_database.team_organisation(team3, cursor),
                "team_city": mc_database.team_city(team3, cursor),
                "points_total": mc_database.team_total_points(team3, cursor),
                "points_event": mc_database.team_event_points(team3, event, cursor),
                "points_avg_total": int(mc_database.team_total_points(team3, cursor) / mc_database.team_matches_total(team3, cursor)),
                "points_avg_event": int(mc_database.team_event_points(team3, event, cursor) / mc_database.team_matches_event(team3, event, cursor)),
                "matches_total": mc_database.team_matches_total(team3, cursor),
                "matches_event": mc_database.team_matches_event(team3, event, cursor),
                "wins_total": mc_database.team_wins_total(team3, cursor),
                "wins_event": mc_database.team_wins_event(team3, event, cursor),
                "wins_pct_total": int((mc_database.team_wins_total(team3, cursor) / mc_database.team_matches_total(team3, cursor)) * 100),
                "wins_pct_event": int((mc_database.team_wins_event(team3, event, cursor) / mc_database.team_matches_event(team3, event, cursor)) * 100),
                "team_hs_total": mc_database.team_hs_total(team3, cursor),
                "team_hs_event": mc_database.team_hs_event(team3, event, cursor),
                "team_hs_total_match": mc_database.team_hs_total_match(team3, mc_database.team_hs_total(team3, cursor), cursor),
                "team_hs_event_match": mc_database.team_hs_event_match(team3, event, mc_database.team_hs_event(team3, event, cursor), cursor),
                "awards": mc_database.awards(team3, cursor)
            },
            "blue2": {
                "team_name": mc_database.team_name(team4, cursor),
                "team_number": mc_database.team_number(team4, cursor),
                "team_robot": mc_database.team_robot(team4, cursor),
                "team_grade": mc_database.team_grade(team4, cursor),
                "team_organisation": mc_database.team_organisation(team4, cursor),
                "team_city": mc_database.team_city(team4, cursor),
                "points_total": mc_database.team_total_points(team4, cursor),
                "points_event": mc_database.team_event_points(team4, event, cursor),
                "points_avg_total": int(mc_database.team_total_points(team4, cursor) / mc_database.team_matches_total(team4, cursor)),
                "points_avg_event": int(mc_database.team_event_points(team4, event, cursor) / mc_database.team_matches_event(team4, event, cursor)),
                "matches_total": mc_database.team_matches_total(team4, cursor),
                "matches_event": mc_database.team_matches_event(team4, event, cursor),
                "wins_total": mc_database.team_wins_total(team4, cursor),
                "wins_event": mc_database.team_wins_event(team4, event, cursor),
                "wins_pct_total": int((mc_database.team_wins_total(team4, cursor) / mc_database.team_matches_total(team4, cursor)) * 100),
                "wins_pct_event": int((mc_database.team_wins_event(team4, event, cursor) / mc_database.team_matches_event(team4, event, cursor)) * 100),
                "team_hs_total": mc_database.team_hs_total(team4, cursor),
                "team_hs_event": mc_database.team_hs_event(team4, event, cursor),
                "team_hs_total_match": mc_database.team_hs_total_match(team4, mc_database.team_hs_total(team4, cursor), cursor),
                "team_hs_event_match": mc_database.team_hs_event_match(team4, event, mc_database.team_hs_event(team4, event, cursor), cursor),
                "awards": mc_database.awards(team4, cursor)
            }
        }
    }
    connection.close()
    return jsonify(response)

if __name__ == "__main__":
    connection = mc_database.connect("indev.db")
    # Initialise database if it does not already exist
    mc_database.program_init(connection)
    connection.close()
    app.run(debug=True)