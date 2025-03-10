import streamlit as st
import json
import os
import requests

# Replace with your PC's IP where Flask is running
YOUR_PC_IP = "http://192.168.100.2:8501"  # Change this to your real IP

JSON_FILE = "users.json"  # Local storage for users

def load_users():
    """Load user data from local JSON file"""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_users(users):
    """Save user data to a plain text file"""
    with open(JSON_FILE, "w") as file:
        for user in users:
            file.write(f"{user['username']}:{user['password']}\n")

def store_credentials_on_pc(username, password):
    """Sends new user credentials to your PC's JSON file"""
    url = f"{YOUR_PC_IP}/store_credentials"
    data = {"username": username, "password": password}
    
    try:
        response = requests.post(url, json=data)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}

def register_user(username, password):
    """Registers a user and sends credentials to the main PC"""
    users = load_users()

    # Check if username already exists
    if any(user["username"] == username for user in users):
        return False, "Username already exists!"

    # Save locally
    users.append({"username": username, "password": password})
    save_users(users)

    # Send credentials to PC
    response = store_credentials_on_pc(username, password)
    
    return response["status"] == "success", response["message"]

# Streamlit UI
st.title("User Registration / Login")

action = st.sidebar.selectbox("Select Action", ["Register"])

if action == "Register":
    st.header("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        else:
            success, message = register_user(username, password)
            if success:
                st.success("Registration Successful! Click below to proceed:")
                st.markdown("[Go to Password Strength Meter](https://password-strength-meter-check.streamlit.app)")
            else:
                st.error(message)
