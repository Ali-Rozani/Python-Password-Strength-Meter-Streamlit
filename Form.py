import streamlit as st
import bcrypt
import json
import os

# --- Utility Functions ---
def hash_password(password):
    """Hashes the password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    """Verifies the password against the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed.encode())

def save_to_json(user_data, filename="pending_users.json"):
    """Saves user data to a JSON file."""
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            json.dump([], file)  # Initialize with an empty list if file doesn't exist

    with open(filename, "r") as file:
        data = json.load(file)
    
    data.append(user_data)
    
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def register_user(username, password):
    """Registers a new user by inserting the credentials into users.json if the username doesn't exist."""
    if os.path.exists("pending_users.json"):
        with open("pending_users.json", "r") as file:
            users = json.load(file)
            if any(user["username"] == username for user in users):
                return False, "User already exists. Please choose a different username."
    else:
        users = []

    # Store password in plain text (INSECURE)
    user_data = {"username": username, "password": password}  # No hashing

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
        
        if not verify_password(password, user["password"]):
            return False, "Incorrect password. Please try again."
        
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
                # Redirecting after a short delay
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
