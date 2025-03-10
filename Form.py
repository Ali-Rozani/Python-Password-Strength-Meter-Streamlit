import streamlit as st
import sqlite3
import os
import requests

# Database settings
DB_URL = "https://raw.githubusercontent.com/your-username/your-repo/main/users.db"  # Update this
DB_PATH = "users.db"

def download_db():
    """Downloads users.db from GitHub if not found."""
    if not os.path.exists(DB_PATH):
        response = requests.get(DB_URL)
        with open(DB_PATH, "wb") as file:
            file.write(response.content)

def initialize_db():
    """Creates the users table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

download_db()  # Ensure the database exists
initialize_db()  # Run initialization

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# Function to register user
def register_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        return False, "Username already exists!"

# Function to check login
def login_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    return bool(user)

# Streamlit UI
st.title("User Registration / Login")

action = st.sidebar.selectbox("Select Action", ["Register", "Login"])

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

elif action == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        success = login_user(username, password)
        if success:
            st.success("Login Successful! Click below to proceed:")
            st.markdown("[Go to Password Strength Meter](https://password-strength-meter-check.streamlit.app)")
        else:
            st.error("Incorrect username or password.")
