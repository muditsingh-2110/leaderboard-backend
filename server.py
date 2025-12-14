import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# --- DATABASE SETUP ---
# This connects to the Render Database using the URL we saved earlier
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATA MODEL (The Table) ---
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)

# Create the table if it doesn't exist
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Game Server with Database is Running!"

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.json
    
    # Create a new player record
    new_player = Player(
        name=data['name'],
        email=data['email'],
        score=int(data['score'])
    )
    
    # Save to Database
    db.session.add(new_player)
    db.session.commit()
    
    return jsonify({"message": "Score saved to Database!"}), 200

@app.route('/get_leaderboard', methods=['GET'])
def get_leaderboard():
    # Fetch from Database and Sort by Score (Descending)
    players = Player.query.order_by(Player.score.desc()).all()
    
    # Convert to JSON list
    output = []
    for p in players:
        output.append({"name": p.name, "score": p.score})
    
    return jsonify(output), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)