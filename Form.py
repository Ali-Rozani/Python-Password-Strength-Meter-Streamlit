import streamlit as st
import json
import os

def save_to_json(user_data, filename="pending_users.json"):
    """Saves user data to a JSON file, handling empty or corrupted JSON files."""
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            json.dump([], file)  # Create an empty list if the file doesn't exist

    try:
        with open(filename, "r") as file:
            data = json.load(file)  # Load JSON data
            if not isinstance(data, list):  # Ensure it's a list
                data = []
    except (json.JSONDecodeError, ValueError):  # Handle empty/corrupt file
        data = []

    data.append(user_data)

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def register_user(username, password):
    """Registers a new user by inserting the credentials into pending_users.json if the username doesn't exist."""
    if os.path.exists("pending_users.json"):
        try:
            with open("pending_users.json", "r") as file:
                users = json.load(file)  # Try loading JSON
                if not isinstance(users, list):  # Ensure it is a list
                    users = []
        except (json.JSONDecodeError, ValueError):  # Handle empty/corrupt file
            users = []
    else:
        users = []

    if any(user["username"] == username for user in users):
        return False, "User already exists. Please choose a different username."

    user_data = {"username": username, "password": password}  # Storing passwords in plain text (INSECURE)
    save_to_json(user_data)
    return True, "Registration successful!"

def login_user(username, password):
    """Logs in the user by validating credentials against the users.json file."""
    if not os.path.exists("pending_users.json"):
        return False, "User does not exist. Please register first."

    with open("pending_users.json", "r") as file:
        users = json.load(file)
        user = next((user for user in users if user["username"] == username and user["password"] == password), None)
        if not user:
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
        else:
            st.error(message)
