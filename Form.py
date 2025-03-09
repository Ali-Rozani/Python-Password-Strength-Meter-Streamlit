import streamlit as st
import json
import os
import bcrypt

hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Function to save user data to JSON file
ef save_to_json(user_data, filename="pending_users.json"):
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            json.dump([], file)

    try:
        with open(filename, "r") as file:
            data = json.load(file)
            if not isinstance(data, list):
                data = []
    except (json.JSONDecodeError, ValueError):
        data = []

    data.append(user_data)

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Streamlit UI
st.title("Register")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Register"):
    if username and password:
        save_to_json({"username": username, "password": password})
        
        # ✅ Instead of redirecting automatically, show a clickable button
        st.success("Registration successful! Click below to proceed:")
        st.markdown('[Go to Password Strength Meter](https://password-strength-meter-check.streamlit.app)', unsafe_allow_html=True)
    else:
        st.error("Please fill in all fields!")

# Function to register a user
def register_user(username, password):
    """Registers a new user by inserting credentials into pending_users.json if the username doesn't exist."""
    if os.path.exists("pending_users.json"):
        try:
            with open("pending_users.json", "r") as file:
                users = json.load(file)
                if not isinstance(users, list):
                    users = []
        except (json.JSONDecodeError, ValueError):
            users = []
    else:
        users = []

    if any(user["username"] == username for user in users):
        return False, "User already exists. Please choose a different username."

    user_data = {"username": username, "password": password}  # Storing passwords in plain text (INSECURE)
    save_to_json(user_data)
    return True, "Registration successful!"

# Function to log in a user
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
                st.info("Redirecting to Password Strength Meter Check...")
                
                # Redirect user instantly
                st.markdown("""
                    <meta http-equiv="refresh" content="0;url=https://password-strength-meter-check.streamlit.app">
                """, unsafe_allow_html=True)
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
            st.info("Redirecting to Password Strength Meter Check...")

            # Redirect user instantly
            st.markdown("""
                <meta http-equiv="refresh" content="0;url=https://password-strength-meter-check.streamlit.app">
            """, unsafe_allow_html=True)
        else:
            st.error(message)
