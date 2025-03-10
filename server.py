from flask import Flask, request, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow connections from any device

JSON_FILE = "users.json"  # File where credentials will be stored

def load_users():
    """Load user data from JSON file"""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []  # If file is corrupted, reset to empty list
    return []

def save_users(users):
    """Save user data to JSON file"""
    with open(JSON_FILE, "w") as file:
        json.dump(users, file, indent=4)

@app.route('/store_credentials', methods=['POST'])
def store_credentials():
    """Receives user credentials from Streamlit and saves them in users.json"""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    users = load_users()

    # Check if username exists
    for user in users:
        if user["username"] == username:
            return jsonify({"status": "error", "message": "Username already exists"}), 400

    # Add new user
    users.append({"username": username, "password": password})
    save_users(users)

    return jsonify({"status": "success", "message": "User credentials saved!"})

if __name__ == '__main__':
    app.run(host="192.168.100.2", port=8501, debug=True)  # Run on your PC
