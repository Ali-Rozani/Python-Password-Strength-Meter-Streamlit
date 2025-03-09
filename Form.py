import streamlit as st
import json
import os
import bcrypt

hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Save user data to a JSON file
def save_to_json(data, filename="users.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = {}
    else:
        users = {}

    users[data["username"]] = data["password"]

    with open(filename, "w") as file:
        json.dump(users, file, indent=4)

# Register a new user
def register_user(username, password):
    """Registers a user if the username is not already taken."""
    filename = "users.json"

    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = {}
    else:
        users = {}

    if username in users:
        return False, "User already exists. Please choose a different username."

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    users[username] = hashed  # Store the hashed password

    with open(filename, "w") as file:
        json.dump(users, file, indent=4)

    return True, "Registration successful!"

# Login user
def login_user(username, password):
    """Logs in a user if credentials are correct."""
    filename = "users.json"

    if not os.path.exists(filename):
        return False, "User does not exist. Please register first."

    with open(filename, "r") as file:
        try:
            users = json.load(file)
        except json.JSONDecodeError:
            users = {}

    if username not in users:
        return False, "User does not exist. Please register first."

    if not bcrypt.checkpw(password.encode('utf-8'), users[username].encode('utf-8')):
        return False, "Incorrect username or password."

    return True, "Login successful!"

# --- Streamlit UI ---
st.title("User Registration & Login")

action = st.sidebar.radio("Select Action", ["Register", "Login"])

if action == "Register":
    st.header("Register")
    with st.form("registration_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit_reg = st.form_submit_button("Register")

    if submit_reg:
        if password != confirm_password:
            st.error("Passwords do not match!")
        else:
            success, message = register_user(username, password)
            if success:
                st.success("Registration Successful! Click the link below to proceed:")
                st.markdown("[Go to Password Strength Meter](https://password-strength-meter-check.streamlit.app)")
            else:
                st.error(message)

elif action == "Login":
    st.header("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_login = st.form_submit_button("Login")

    if submit_login:
        success, message = login_user(username, password)
        if success:
            st.success("Login Successful! Click the link below to proceed:")
            st.markdown("[Go to Password Strength Meter](https://password-strength-meter-check.streamlit.app)")
        else:
            st.error(message)
