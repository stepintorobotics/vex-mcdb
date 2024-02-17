import sqlite3

def database_init(connection):
    cursor = connection.cursor()

    # Teams
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY,
            team_number STRING,
            team_name STRING,
            team_robot STRING,
            team_organisation STRING,
            team_city STRING,
            team_grade STRING,
            team_program INTEGER,
            FOREIGN KEY (team_program) REFERENCES programs(program_id)
        )
        """
    )
    connection.commit()

    # Awards
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS awards (
            award_id INTEGER PRIMARY KEY,
            award_name STRING,
            award_event INTEGER,
            award_team INTEGER,
            FOREIGN KEY (award_event) REFERENCES events(event_id),
            FOREIGN KEY (award_team) REFERENCES teams(team_id)
        )
        """
    )
    connection.commit()

    # Events
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY,
            event_name STRING,
            event_city STRING,
            event_season INTEGER,
            FOREIGN KEY (event_season) REFERENCES seasons(season_id)
        )
        """
    )
    connection.commit()

    # Divisions
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS divisions (
            division_id INTEGER PRIMARY KEY,
            division_event INTEGER,
            division_name STRING
            FOREIGN KEY (division_event) REFERENCES events(event_id)
        )
        """
    )

    # Matches
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS matches (
            match_id INTEGER PRIMARY KEY,
            match_event INTEGER,
            match_red_team1 INTEGER,
            match_red_team2 INTEGER,
            match_blue_team1 INTEGER,
            match_blue_team2 INTEGER,
            match_red_score INTEGER,
            match_blue_score INTEGER,
            match_division INTEGER,
            FOREIGN KEY (match_event) REFERENCES events(event_id),
            FOREIGN KEY (match_red_team1) REFERENCES teams(team_id),
            FOREIGN KEY (match_red_team2) REFERENCES teams(team_id),
            FOREIGN KEY (match_blue_team1) REFERENCES teams(team_id),
            FOREIGN KEY (match_blue_team2) REFERENCES teams(team_id),
        )
        """
    )
    connection.commit()

    # Notes
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            note_id INTEGER PRIMARY KEY,
            note_data STRING,
            note_event INTEGER,
            note_team INTEGER,
            FOREIGN KEY (note_event) REFERENCES events(event_id),
            FOREIGN KEY (note_team) REFERENCES teams(team_id)
        )
        """
    )
    connection.commit()

    # Seasons and programs
    # These change infrequently, unnecessary to fetch from RE API
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS programs (
            program_id INTEGER PRIMARY KEY,
            program_name STRING
        )
        """
    )
    cursor.execute("INSERT INTO programs (program_id, program_name) VALUES (1, 'VEX Robotics Competition')")
    cursor.execute("INSERT INTO programs (program_id, program_name) VALUES (41, 'VEX IQ Robotics Competition')")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS seasons (
            season_id INTEGER PRIMARY KEY,
            season_name STRING,
            season_program INTEGER,
            FOREIGN KEY (season_program) REFERENCES programs(program_id)
        )
        """
    )
    cursor.execute("INSERT INTO seasons (season_id, season_name, season_program) VALUES (180, 'Full Volume', 41)")
    cursor.execute("INSERT INTO seasons (season_id, season_name, season_program) VALUES (181, 'Over Under', 1)")
    connection.commit()

    # Mark database as initialised
    cursor.execute("INSERT INTO config (config_key, config_value) VALUES ('initialised', 'Y')")
    connection.commit()  


# Run when the API is started
def program_init(connection):
    cursor = connection.cursor()

    # Create API/database configuration table on first run
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS config (
            config_key STRING PRIMARY KEY,
            config_value STRING
        )
        """
    )
    connection.commit()

    # Check if database has been initialised with tables, records, etc.
    cursor.execute("SELECT * FROM config WHERE config_key='initialised'")
    initialised = cursor.fetchone() is not None
    if not initialised:
        database_init(connection)


def connect(file):
    connection = sqlite3.connect(file)
    return connection