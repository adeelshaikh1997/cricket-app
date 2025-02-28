from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# DB connection helper
def get_db():
    conn = sqlite3.connect('psl_stats.db')
    conn.row_factory = sqlite3.Row  # Returns dict-like rows
    return conn

@app.route('/')
def home():
    return "Welcome to PSL Stats App!"

# Player Explorer API
@app.route('/api/players/<name>')
def get_player(name):
    conn = get_db()
    cursor = conn.cursor()
    player = cursor.execute('SELECT * FROM players WHERE name = ?', (name,)).fetchone()
    conn.close()
    if player:
        return jsonify(dict(player))
    return jsonify({"error": "Player not found"}), 404

# Match Filter API
@app.route('/api/matches')
def get_matches():
    team = request.args.get('team', '')
    season = request.args.get('season', '')
    conn = get_db()
    cursor = conn.cursor()
    query = 'SELECT * FROM matches WHERE 1=1'
    params = []
    if team:
        query += ' AND (team1 = ? OR team2 = ?)'
        params.extend([team, team])
    if season:
        query += ' AND date LIKE ?'
        params.append(f'{season}%')
    query += ' LIMIT 10'
    matches = cursor.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(m) for m in matches])

# Team Comparison API
@app.route('/api/teams/<team1>/<team2>')
def compare_teams(team1, team2):
    conn = get_db()
    cursor = conn.cursor()
    team1_data = cursor.execute('SELECT * FROM teams WHERE name = ?', (team1,)).fetchone()
    team2_data = cursor.execute('SELECT * FROM teams WHERE name = ?', (team2,)).fetchone()
    conn.close()
    if team1_data and team2_data:
        return jsonify({"team1": dict(team1_data), "team2": dict(team2_data)})
    return jsonify({"error": "One or both teams not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)