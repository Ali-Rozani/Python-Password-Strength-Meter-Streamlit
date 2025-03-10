import streamlit as st
from pymongo.mongo_client import MongoClient
import hashlib
import re

# MongoDB connection string
MONGODB_URI = "mongodb+srv://alihaiderkasim1:PSM_ATLAS@psm.kkdeq.mongodb.net/?retryWrites=true&w=majority&appName=PSM"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'temp_users' not in st.session_state:
    st.session_state.temp_users = {}
if 'mongo_status' not in st.session_state:
    st.session_state.mongo_status = "Unknown"

# MongoDB connection
def get_mongo_collection():
    try:
        client = MongoClient(
            MONGODB_URI,
            ssl=True,
            ssl_cert_reqs="CERT_NONE", 
            connectTimeoutMS=5000,
            serverSelectionTimeoutMS=5000
        )
        db = client.psm_database
        st.session_state.mongo_status = "Connected"
        return db.users
    except Exception as e:
        st.session_state.mongo_status = f"Error: {str(e)[:50]}..."
        return None

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register user 
def register_user(username, password):
    # Try MongoDB first
    collection = get_mongo_collection()
    hashed_pw = hash_password(password)
    
    # Always store in session state temporarily
    st.session_state.temp_users[username] = {
        "username": username,
        "password": hashed_pw
    }
    
    if collection:
        try:
            # Check if user exists in MongoDB
            if collection.find_one({"username": username}):
                return False, "Username already exists"
            
            # Add to MongoDB
            collection.insert_one({
                "username": username,
                "password": hashed_pw
            })
            return True, "Registration successful!"
        except Exception as e:
            return True, "Registration saved temporarily. Database sync pending."
    else:
        return True, "Registration saved temporarily. Database unavailable."

# Login function
def login(username, password):
    hashed_pw = hash_password(password)
    
    # Check session state first (temporary storage)
    if username in st.session_state.temp_users:
        if st.session_state.temp_users[username]["password"] == hashed_pw:
            return True
    
    # Try MongoDB
    collection = get_mongo_collection()
    if collection:
        user = collection.find_one({"username": username})
        if user and user.get("password") == hashed_pw:
            # Add to session state for faster future logins
            st.session_state.temp_users[username] = user
            return True
    
    return False

# Password strength checker function
def check_password_strength(password):
    score = sum([
        len(password) >= 8,
        bool(re.search(r'[A-Z]', password)),
        bool(re.search(r'[a-z]', password)),
        bool(re.search(r'[0-9]', password)),
        bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    ])
    
    strength_map = {
        0: ("Very Weak", 20, "darkred"),
        1: ("Very Weak", 20, "darkred"),
        2: ("Weak", 40, "red"),
        3: ("Moderate", 60, "orange"),
        4: ("Strong", 80, "lightgreen"),
        5: ("Very Strong", 100, "green")
    }
    
    return strength_map[score]

# Main application
def main():
    st.title("Login Or Register (Credentials Will Be Stored In MongoDB)")
    
    # Show database status in sidebar
    st.sidebar.text(f"Database: {st.session_state.mongo_status}")
    
    if not st.session_state.logged_in:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                if login(username, password):
                    st.session_state.logged_in = True
                    st.success("Login successful!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password")
        
        with tab2:
            new_username = st.text_input("New Username", key="reg_username")
            new_password = st.text_input("New Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            
            if st.button("Register"):
                if not new_username or not new_password:
                    st.error("Please fill in all fields")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    success, message = register_user(new_username, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
    else:
        # Show password strength meter
        st.header("Check Password Strength")
        test_password = st.text_input("Enter a password to test:", type="password")
        
        if test_password:
            strength, score, color = check_password_strength(test_password)
            
            st.write(f"**Password Strength:** :{color}[{strength}]")
            st.progress(score/100)
            
            # Provide feedback based on strength
            if strength == "Very Weak" or strength == "Weak":
                st.error("Try adding uppercase letters, numbers, and special characters!")
            elif strength == "Moderate":
                st.warning("Your password could be stronger. Try making it longer.")
            else:
                st.success("Great password choice!")
        
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
