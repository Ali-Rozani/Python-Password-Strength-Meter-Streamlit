import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import hashlib
import certifi
import json
import os

# Initialize session state
if 'login_status' not in st.session_state:
    st.session_state.login_status = False
if 'pending_registrations' not in st.session_state:
    st.session_state.pending_registrations = []

# MongoDB connection
def connect_to_mongodb():
    # Use a local connection string (make sure your local MongoDB is running)
    uri = "mongodb://localhost:27017/psm_database"
    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        print("Connected to MongoDB!")
        # Return the 'users' collection from the 'psm_database' database
        return client["psm_database"]["users"]
    except Exception as e:
        print(f"MongoDB error: {e}")
        return None

    
def get_db():
    try:
        client = MongoClient(
            "mongodb+srv://alihaiderkasim1:PSM_ATLAS@psm.kkdeq.mongodb.net/?retryWrites=true&w=majority&appName=PSM",
            server_api=ServerApi('1'),
            tls=True,
            tlsCAFile=certifi.where(),
            connectTimeoutMS=5000,
            serverSelectionTimeoutMS=5000
        )
        client.admin.command('ping')
        return client.psm_database.users
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None

# Local storage functionality
def save_local_data():
    # Save pending registrations to a file
    with open("pending_users.json", "w") as f:
        json.dump(st.session_state.pending_registrations, f)

def load_local_data():
    # Load pending registrations from file
    if os.path.exists("pending_users.json"):
        with open("pending_users.json", "r") as f:
            st.session_state.pending_registrations = json.load(f)

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register user (works offline)
def register_user(username, password):
    hashed_password = hash_password(password)
    user_data = {"username": username, "password": hashed_password}
    
    # Try to save to MongoDB if connected
    collection = connect_to_mongodb()
    if collection is not None:
        try:
            if collection.find_one({"username": username}):
                return False, "Username already exists"
            collection.insert_one(user_data)
            return True, "Registration successful!"
        except Exception as e:
            print(f"MongoDB error: {e}")
    
    # Fallback: store locally if MongoDB is unavailable
    st.session_state.pending_registrations.append(user_data)
    save_local_data()
    return True, "Registration saved locally (MongoDB offline)"

# Authenticate user
def authenticate_user(username, password):
    hashed_password = hash_password(password)
    
    # Try MongoDB first
    collection = connect_to_mongodb()
    if collection:
        user = collection.find_one({"username": username})
        if user and user["password"] == hashed_password:
            return True
    
    # Check local storage if MongoDB failed
    for user in st.session_state.pending_registrations:
        if user["username"] == username and user["password"] == hashed_password:
            return True
    
    return False

def get_db():
    try:
        # Attempt connection with more specific SSL settings
        client = MongoClient(
            "mongodb+srv://alihaiderkasim1:PSM_ATLAS@psm.kkdeq.mongodb.net/?retryWrites=true&w=majority&appName=PSM",
            ssl=True,
            ssl_cert_reqs="CERT_NONE",  # Disables certificate verification - only for development!
            connectTimeoutMS=5000,
            serverSelectionTimeoutMS=5000
        )
        # Test connection
        client.server_info()
        return client.psm_database.users
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None
# Password strength checker
def check_password_strength(password):
    import re
    score = sum([
        len(password) >= 8,
        bool(re.search(r'[A-Z]', password)),
        bool(re.search(r'[a-z]', password)),
        bool(re.search(r'[0-9]', password)),
        bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    ])
    
    strength_levels = {
        5: ("Very Strong", 100, "green"),
        4: ("Strong", 80, "lightgreen"),
        3: ("Moderate", 60, "orange"),
        2: ("Weak", 40, "red"),
        1: ("Very Weak", 20, "darkred"),
        0: ("Very Weak", 20, "darkred")
    }
    
    return strength_levels[score]

# Main app
def main():
    st.title("Login/Registration")
    load_local_data()  # Load any pending registrations
    
    if not st.session_state.login_status:
        # Login/Registration UI
        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Menu", menu)
        
        if choice == "Login":
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login"):
                if authenticate_user(username, password):
                    st.session_state.login_status = True
                    st.success("Login successful!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials")
                    
        elif choice == "Register":
            st.subheader("Register")
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            
            if st.button("Register"):
                if not new_username or not new_password:
                    st.warning("Please fill all fields")
                else:
                    success, message = register_user(new_username, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
    else:
        # Password strength meter
        st.subheader("Check Password Strength")
        test_password = st.text_input("Enter password:", type="password")
        
        if test_password:
            strength, score, color = check_password_strength(test_password)
            st.write(f"**Password Strength:** :{color}[{strength}]")
            st.progress(score / 100)
            
        if st.sidebar.button("Logout"):
            st.session_state.login_status = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()