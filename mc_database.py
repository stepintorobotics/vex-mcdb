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
            award_id INTEGER,
            award_team INTEGER,
            award_name STRING,
            award_event INTEGER,
            PRIMARY KEY (award_id, award_team),
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
            event_sku STRING,
            event_name STRING,
            event_city STRING,
            event_season INTEGER,
            event_divisions INTEGER,
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
            division_name STRING,
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
            match_red_team1 INTEGER NULL,
            match_red_team2 INTEGER NULL,
            match_blue_team1 INTEGER NULL,
            match_blue_team2 INTEGER NULL,
            match_red_score INTEGER NULL,
            match_blue_score INTEGER NULL,
            match_division INTEGER,
            match_program INTEGER,
            FOREIGN KEY (match_event) REFERENCES events(event_id),
            FOREIGN KEY (match_red_team1) REFERENCES teams(team_id),
            FOREIGN KEY (match_red_team2) REFERENCES teams(team_id),
            FOREIGN KEY (match_blue_team1) REFERENCES teams(team_id),
            FOREIGN KEY (match_blue_team2) REFERENCES teams(team_id),
            FOREIGN KEY (match_program) REFERENCES program_id(programs)
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


def insert_events(events, connection):
    data = events
    cursor = connection.cursor()
    for event in data:
        cursor.execute(
            """
            INSERT OR REPLACE INTO events (event_id, event_sku, event_name, event_city, event_season, event_divisions)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (event["id"], event["sku"], event["name"], event["location"]["city"], event["season"]["id"], len(event["divisions"]))
        )
    connection.commit()


def insert_teams(teams, connection):
    data = teams
    cursor = connection.cursor()
    for team in data:
        cursor.execute(
            """
            INSERT OR REPLACE INTO teams (team_id, team_number, team_name, team_robot, team_organisation, team_city, team_grade, team_program)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (team["id"], team["number"], team["team_name"], team["robot_name"], team["organization"], team["location"]["city"], team["grade"], team["program"]["id"])
        )
    connection.commit()

def insert_awards(awards, team, connection):
    data = awards
    cursor = connection.cursor()
    for award in data:
        cursor.execute(
            """
            INSERT OR REPLACE INTO awards (award_id, award_team, award_name, award_event)
            VALUES (?, ?, ?, ?)
            """, (award["id"], team, award["title"], award["event"]["id"])
        )
    connection.commit()