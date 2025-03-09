import streamlit as st
import json
import os
import bcrypt

import streamlit as st

st.title("Register or Login")

# User input fields
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Register"):
    if username and password:
        st.success("Registration Successful! Click the link below to proceed:")
        st.markdown("[Go to Password Strength Meter](https://password-strength-meter-check.streamlit.app)")
    else:
        st.error("Please fill in both fields.")

if st.button("Login"):
    if username and password:
        st.success("Login Successful! Click the link below to proceed:")
        st.markdown("[Go to Password Strength Meter](https://password-strength-meter-check.streamlit.app)")
    else:
        st.error("Please enter both username and password.")

def register_user(username, password):
    """Registers a new user by inserting the credentials into users.json if the username doesn't exist."""
    if os.path.exists("pending_users.json"):
        with open("pending_users.json", "r") as file:
            users = json.load(file)
            if any(user["username"] == username for user in users):
                return False, "User already exists. Please choose a different username."
    else:
        users = []

    # Hash the password using bcrypt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_data = {"username": username, "password": hashed}  # storing hashed password
    save_to_json(user_data)
    return True, "Registration successful!"

def login_user(username, password):
    """Logs in the user by validating credentials against the users.json file."""
    if not os.path.exists("pending_users.json"):
        return False, "User does not exist. Please register first."

    with open("pending_users.json", "r") as file:
        users = json.load(file)
        user = next((user for user in users if user["username"] == username), None)
        if not user:
            return False, "User does not exist. Please register first."
        if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            return False, "Incorrect username or password."
        return True, "Login successful!"

# --- Streamlit App UI ---
st.title("User Registration / Login Page")
action = st.sidebar.selectbox("Select Action", ["Register", "Login"])

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
                st.success(message)
                st.info("Redirecting to the Password Strength Meter Check App...")
                st.markdown(
                    '<meta http-equiv="refresh" content="2;url=https://password-strength-meter-check.streamlit.app">',
                    unsafe_allow_html=True
                )
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
            st.success(message)
            st.info("Redirecting to the Password Strength Meter Check App...")
            st.markdown(
                '<meta http-equiv="refresh" content="2;url=https://password-strength-meter-check.streamlit.app">',
                unsafe_allow_html=True
            )
        else:
            st.error(message)
