from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# CORS is crucial: It allows your "Game" (which will be on a different URL) 
# to talk to this "Server".
CORS(app)

# This list will hold the scores temporarily
game_data = []

@app.route('/')
def home():
    return "Game Server is Running!"

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.json
    
    # We expect data to look like: {"name": "Alex", "email": "a@b.com", "score": 10}
    if not data or 'score' not in data:
        return jsonify({"error": "Invalid data"}), 400
        
    # Add to our list
    game_data.append(data)
    print(f"New Score: {data}") # Prints to server logs
    
    return jsonify({"message": "Score saved successfully!"}), 200

@app.route('/get_leaderboard', methods=['GET'])
def get_leaderboard():
    # Sort the data by score (Descending: Highest first)
    # We use int() to make sure we compare numbers, not strings
    sorted_data = sorted(game_data, key=lambda x: int(x['score']), reverse=True)
    
    return jsonify(sorted_data), 200

if __name__ == '__main__':
    # CLOUD REQUIREMENT:
    # Cloud servers (like Render) tell us which Port to use via 'os.environ'.
    # If we are on our own computer, we default to 5000.
    port = int(os.environ.get('PORT', 5000))
    
    # host='0.0.0.0' makes the server accessible externally
    app.run(host='0.0.0.0', port=port)