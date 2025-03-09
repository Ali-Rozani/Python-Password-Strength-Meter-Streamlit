import streamlit as st
import json
import os
import bcrypt

# Function to save user data
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

# Function to register a user
def register_user(username, password):
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = {}
    else:
        users = {}

    if username in users:
        return False, "User already exists. Please choose a different username."

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    save_to_json({"username": username, "password": hashed_password})
    return True, "Registration successful!"

# Function to login a user
def login_user(username, password):
    if not os.path.exists("users.json"):
        return False, "User does not exist. Please register first."

    with open("users.json", "r") as file:
        try:
            users = json.load(file)
        except json.JSONDecodeError:
            users = {}

    if username not in users:
        return False, "User does not exist. Please register first."

    if not bcrypt.checkpw(password.encode('utf-8'), users[username].encode('utf-8')):
        return False, "Incorrect username or password."

    return True, "Login successful!"

# --- Streamlit App UI ---
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
                st.success("Registration Successful!")
                st.markdown("[Go to Password Strength Meter](https://password-strength-meter-check.streamlit.app)")
            else:
                st.error(message)

elif action == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        success, message = login_user(username, password)
        if success:
            st.success("Login Successful!")
            st.markdown("[Go to Password Strength Meter](https://password-strength-meter-check.streamlit.app)")
        else:
            st.error(message)
