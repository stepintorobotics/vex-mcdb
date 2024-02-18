import sqlite3

# Creates tables, inserts preset data
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
            match_division INTEGER,
            match_name STRING,
            match_number INTEGER,
            match_round INTEGER,
            match_season INTEGER,
            match_red_team1 INTEGER NULL,
            match_red_team2 INTEGER NULL,
            match_blue_team1 INTEGER NULL,
            match_blue_team2 INTEGER NULL,
            match_red_score INTEGER NULL,
            match_blue_score INTEGER NULL,
            FOREIGN KEY (match_event) REFERENCES events(event_id),
            FOREIGN KEY (match_red_team1) REFERENCES teams(team_id),
            FOREIGN KEY (match_red_team2) REFERENCES teams(team_id),
            FOREIGN KEY (match_blue_team1) REFERENCES teams(team_id),
            FOREIGN KEY (match_blue_team2) REFERENCES teams(team_id),
            FOREIGN KEY (match_season) REFERENCES program_id(programs)
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
    # Iterate through events and insert data
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
    # Iterate through teams and insert data
    for team in data:
        cursor.execute(
            """
            INSERT OR REPLACE INTO teams (team_id, team_number, team_name, team_robot, team_organisation, team_city, team_grade, team_program)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (team["id"], team["number"], team["team_name"], team["robot_name"], team["organization"], team["location"]["city"], team["grade"], team["program"]["id"])
        )
    connection.commit()

def insert_awards(awards, connection):
    data = awards
    cursor = connection.cursor()
    # Iterate through events for awards and insert data
    for award in data:
        for winner in award["teamWinners"]:
            cursor.execute(
                """
                INSERT OR REPLACE INTO awards (award_id, award_team, award_name, award_event)
                VALUES (?, ?, ?, ?)
                """, (award["id"], winner["team"]["id"], award["title"], award["event"]["id"])
            )
    connection.commit()

def insert_matches(matches, connection):
    data = matches
    cursor = connection.cursor()
    # Iterate through events
    for match in data:
        # Get season of current match via events table
        event = match["event"]["id"]
        cursor.execute("SELECT event_season FROM events WHERE event_id = ?", (event,))
        season = cursor.fetchone()[0]
        # 181 is VRC, so has four teams
        if season == 181:
            red1 = match["alliances"][1]["teams"][0]["team"]["id"]
            red2 = match["alliances"][1]["teams"][1]["team"]["id"]
            blue1 = match["alliances"][0]["teams"][0]["team"]["id"]
            blue2 = match["alliances"][0]["teams"][1]["team"]["id"]
        # 180 is VIQRC, so has two teams
        elif season == 180:
            red1 = match["alliances"][1]["teams"][0]["team"]["id"]
            red2 = None
            blue1 = match["alliances"][0]["teams"][0]["team"]["id"]
            blue2 = None
        # Insert into database
        cursor.execute(
            """
            INSERT OR REPLACE INTO matches (match_id, match_event, match_division, match_name, match_number, match_round, match_season, match_red_team1, match_red_team2, match_blue_team1, match_blue_team2, match_red_score, match_blue_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (match["id"], event, match["division"]["id"], match["name"], match["matchnum"], match["round"], season, red1, red2, blue1, blue2, match["alliances"][1]["score"], match["alliances"][0]["score"])
        )
    connection.commit()