import json
import os
import sqlite3

conn = sqlite3.connect('psl_stats.db')
cursor = conn.cursor()

data_dir = 'data/psl_male_json/'  # Updated path
print(f"Looking in: {os.path.abspath(data_dir)}")
if not os.path.exists(data_dir):
    print("Error: data/psl_male_json/ folder not found!")
    exit()

players = {}
matches = {}
teams = {"Lahore Qalandars": {"wins": 0, "losses": 0, "titles": 0},
         "Karachi Kings": {"wins": 0, "losses": 0, "titles": 0},
         "Multan Sultans": {"wins": 0, "losses": 0, "titles": 0},
         "Peshawar Zalmi": {"wins": 0, "losses": 0, "titles": 0},
         "Quetta Gladiators": {"wins": 0, "losses": 0, "titles": 0},
         "Islamabad United": {"wins": 0, "losses": 0, "titles": 0}}

file_count = 0
for filename in os.listdir(data_dir):
    if filename.endswith('.json'):
        file_count += 1
        filepath = os.path.join(data_dir, filename)
        print(f"Processing: {filepath}")
        try:
            with open(filepath, 'r') as f:
                match = json.load(f)
                match_id = filename.replace('.json', '')
                team1 = match['info']['teams'][0]
                team2 = match['info']['teams'][1]
                date = match['info']['dates'][0]
                winner = match['info'].get('outcome', {}).get('winner', 'N/A')
                runs = 0
                wickets = 0

                if winner != 'N/A':
                    teams[winner]["wins"] += 1
                    teams[team2 if winner == team1 else team1]["losses"] += 1

                for team in [team1, team2]:
                    for player in match['info']['players'].get(team, []):
                        players[player] = players.get(player, {'runs': 0, 'wickets': 0, 'matches': 0})
                        players[player]['matches'] += 1

                matches[match_id] = {'team1': team1, 'team2': team2, 'date': date, 'winner': winner, 'runs': runs, 'wickets': wickets}
        except Exception as e:
            print(f"Error in {filename}: {e}")

print(f"Processed {file_count} JSON files")
print(f"Players found: {len(players)}")
print(f"Matches found: {len(matches)}")

for player, stats in players.items():
    cursor.execute('INSERT OR REPLACE INTO players (name, runs, wickets, matches) VALUES (?, ?, ?, ?)', 
                   (player, stats['runs'], stats['wickets'], stats['matches']))

for match_id, info in matches.items():
    cursor.execute('INSERT OR REPLACE INTO matches (match_id, team1, team2, date, winner, runs, wickets) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                   (match_id, info['team1'], info['team2'], info['date'], info['winner'], info['runs'], info['wickets']))

for team, stats in teams.items():
    cursor.execute('INSERT OR REPLACE INTO teams (name, wins, losses, titles) VALUES (?, ?, ?, ?)', 
                   (team, stats['wins'], stats['losses'], stats['titles']))

conn.commit()
conn.close()
print("PSL data loaded into SQLite!")