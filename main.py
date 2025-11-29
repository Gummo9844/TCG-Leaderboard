from flask import Flask, request, redirect, render_template_string
import json
import os

app = Flask(__name__)
VOLUME_PATH = '/app/data'

JSON_TEMPLATE = {
    "gummo": {"wins": 1, "losses": 0},
    "rafa": {"wins": 0,"losses": 3},
    "joão": {"wins": 2,"losses": 0},
    "gusta": {"wins": 0,"losses": 0},
    "theo": {"wins": 0,"losses": 0},
    "mel": {"wins": 0,"losses": 0},
    "bh": {"wins": 0,"losses": 0}
}

def verify_path(path):
    if os.path.exists(VOLUME_PATH):
        scores_path = os.path.join(VOLUME_PATH, 'scores.json')
        print("Usando caminho do volume para scores.")
        return scores_path
    else:
        scores_path = 'scores.json'
        print("Usando caminho local para scores.")
        return scores_path

def verify_file(scores_path):
    if not os.path.exists(scores_path):
        with open(scores_path, 'w') as f:
            return json.dump(JSON_TEMPLATE, f)
    return print("scores.json encontrado.")

def load_scores(scores_path):
    try:
        with open(scores_path, "r", encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

@app.route('/', methods=['GET'])
def home():
    return redirect('/scores')

@app.route('/scores', methods=['GET'])
def leaderboard():
    leaderboard = dict(sorted(scores.items(), key=lambda item: item[1]['wins'], reverse=True))

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pokémon TCG Leaderboard</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #e0e0e0; text-align: center; padding: 20px; }
            h1 { color: #bb86fc; }
            table { margin: 0 auto; border-collapse: collapse; width: 60%; box-shadow: 0 0 20px rgba(0,0,0,0.5); }
            th, td { padding: 15px; text-align: center; border-bottom: 1px solid #333; }
            th { background-color: #1f1f1f; color: #03dac6; font-size: 1.2em; }
            tr:hover { background-color: #2c2c2c; }
            .rank { font-weight: bold; color: #cf6679; }
        </style>
    </head>
    <body>
        <h1>🏆 Leaderboard TCG 🏆</h1>
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Jogador</th>
                    <th>Vitórias</th>
                    <th>Derrotas</th>
                </tr>
            </thead>
            <tbody>
                {% for player, stats in leaderboard.items() %}
                <tr>
                    <td class="rank">#{{ loop.index }}</td>
                    <td>{{ player|capitalize }}</td>
                    <td>{{ stats['wins'] }}</td>
                    <td>{{ stats['losses'] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """

    # 3. Renderiza o HTML injetando os dados
    return render_template_string(html_template, leaderboard=leaderboard)
    
    return f"Current Scores:\n {leaderboard}", 200

@app.route('/update', methods=['GET'])
def update():
    winner = (request.args.get('winner')).lower()
    loser = (request.args.get('loser')).lower()
    print(f"Winner: {winner} | Loser: {loser}")

    if winner in scores and loser in scores:
        scores[winner]["wins"] += 1
        scores[loser]["losses"] += 1
        
        with open(scores_path, "w", encoding='utf-8') as f:
            json.dump(scores, f, ensure_ascii=False, indent=4)

        print(f"{scores.get(winner)}")
    return f"Update received\nScores: {scores}", 200

scores_path = verify_path(VOLUME_PATH)
verify_file(scores_path)
scores = load_scores(scores_path)
print(f"Current Scores:\n {scores}")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    