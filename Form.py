import streamlit as st
import json
import os

# Function to save user data
def save_to_json(data, filename="pending_users.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = []
    else:
        users = []

    users.append(data)  # Append new user data

    with open(filename, "w") as file:
        json.dump(users, file, indent=4)

# Function to register a user
def register_user(username, password):
    filename = "pending_users.json"

    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = []
    else:
        users = []

    if any(user["username"] == username for user in users):
        return False, "User already exists. Please choose a different username."

    save_to_json({"username": username, "password": password})  # Store password in plain text
    return True, "Registration successful!"

# Function to login a user
def login_user(username, password):
    filename = "pending_users.json"

    if not os.path.exists(filename):
        return False, "User does not exist. Please register first."

    with open(filename, "r") as file:
        try:
            users = json.load(file)
        except json.JSONDecodeError:
            users = []

    user = next((user for user in users if user["username"] == username and user["password"] == password), None)
    if not user:
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
                st.success("Registration Successful! Redirecting...")
                st.markdown("""
                    <meta http-equiv="refresh" content="2;url=password-strength-meter-check.streamlit.app">
                """, unsafe_allow_html=True)
            else:
                st.error(message)

elif action == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        success, message = login_user(username, password)
        if success:
            st.success("Login Successful! Redirecting...")
            st.markdown("""
                <meta http-equiv="refresh" content="2;url=password-strength-meter-check.streamlit.app">
            """, unsafe_allow_html=True)
        else:
            st.error(message)
