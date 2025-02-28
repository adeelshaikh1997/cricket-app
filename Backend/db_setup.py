import sqlite3
import os

# Delete old db if exists
if os.path.exists('psl_stats.db'):
    os.remove('psl_stats.db')
    print("Old psl_stats.db removed")

conn = sqlite3.connect('psl_stats.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE players (
        name TEXT PRIMARY KEY,
        runs INTEGER,
        wickets INTEGER,
        matches INTEGER,
        batting_avg REAL,
        bowling_avg REAL
    )
''')

cursor.execute('''
    CREATE TABLE matches (
        match_id TEXT PRIMARY KEY,
        team1 TEXT,
        team2 TEXT,
        date TEXT,
        winner TEXT,
        runs INTEGER,
        wickets INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE teams (
        name TEXT PRIMARY KEY,
        wins INTEGER,
        losses INTEGER,
        titles INTEGER
    )
''')

conn.commit()
conn.close()
print("SQLite tables created!")