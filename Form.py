import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import hashlib
import certifi
import time

# Initialize session state
if 'login_status' not in st.session_state:
    st.session_state.login_status = False

# MongoDB connection
def connect_to_mongodb():
    uri = "mongodb+srv://alihaiderkasim1:PSM_ATLAS@psm.kkdeq.mongodb.net/?retryWrites=true&w=majority&appName=PSM"

    # Create a new client and connect to the server with SSL configuration
    try:
        # Use certifi CA bundle for SSL verification
        client = MongoClient(
            uri,
            server_api=ServerApi('1'),
            tlsCAFile=certifi.where(),
            retryWrites=True,
            w="majority",
            tls=True,
            tlsAllowInvalidCertificates=True  # Only use in development, not production
        )
        
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        
        # Create database and collection if they don't exist
        db = client["psm_database"]
        users_collection = db["users"]
        return users_collection
        
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        st.error(f"Failed to connect to MongoDB. Error: {e}")
        return None

# Hash password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Check if user exists
def user_exists(username, collection):
    try:
        return collection.find_one({"username": username}) is not None
    except Exception as e:
        st.error(f"Database error: {e}")
        return False

# Register new user
def register_user(username, password, collection):
    try:
        if user_exists(username, collection):
            return False
            
        # Hash the password before storing
        hashed_password = hash_password(password)
        
        # Insert the new user into the collection
        result = collection.insert_one({
            "username": username, 
            "password": hashed_password,
            "created_at": time.time()
        })
        
        print(f"User created with ID: {result.inserted_id}")
        return True
        
    except Exception as e:
        st.error(f"Registration error: {e}")
        return False

# Authenticate user
def authenticate_user(username, password, collection):
    try:
        user = collection.find_one({"username": username})
        if user and user["password"] == hash_password(password):
            return True
        return False
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return False

# Password strength meter
def check_password_strength(password):
    import re
    
    # Define criteria
    length = len(password) >= 8
    uppercase = bool(re.search(r'[A-Z]', password))
    lowercase = bool(re.search(r'[a-z]', password))
    digit = bool(re.search(r'[0-9]', password))
    special_char = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

    # Calculate strength score
    strength_score = sum([length, uppercase, lowercase, digit, special_char])

    # Determine strength level
    if strength_score == 5:
        return "Very Strong", 100, "green"
    elif strength_score == 4:
        return "Strong", 80, "lightgreen"
    elif strength_score == 3:
        return "Moderate", 60, "orange"
    elif strength_score == 2:
        return "Weak", 40, "red"
    else:
        return "Very Weak", 20, "darkred"

# Main application
def main():
    st.title("Password Strength Meter System")

    # Connect to MongoDB - do this only once
    collection = connect_to_mongodb()

    # Display appropriate interface based on login status
    if not st.session_state.login_status:
        # Show login/register interface
        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("Login"):
                    if collection:
                        if authenticate_user(username, password, collection):
                            st.session_state.login_status = True
                            st.success("Login successful!")
                            st.experimental_rerun()
                        else:
                            st.error("Invalid username or password")
                    else:
                        st.error("Cannot connect to database. Please try again later.")

        elif choice == "Register":
            st.subheader("Create New Account")
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.button("Register"):
                if collection:
                    if new_password != confirm_password:
                        st.error("Passwords do not match!")
                    elif not new_username or not new_password:
                        st.warning("Please fill in all fields")
                    else:
                        if register_user(new_username, new_password, collection):
                            st.success("Account created successfully! Please login.")
                            # Automatically switch to login page
                            time.sleep(1)
                            st.experimental_rerun()
                        else:
                            st.error("Username already exists or registration failed")
                else:
                    st.error("Cannot connect to database. Please try again later.")
    else:
        # Password strength meter functionality
        st.subheader("Password Strength Meter")
        st.write("Enter a password to check its strength:")
        
        test_password = st.text_input("Password:", type="password")
        
        if test_password:
            strength, score, color = check_password_strength(test_password)
            
            # Display strength level
            st.write(f"**Password Strength:** :{color}[{strength}]")
            
            # Display a colored progress bar
            st.progress(score / 100)
            
            # Display feedback with emojis and colors
            if strength == "Very Weak":
                st.error("🚨 Your password is very weak. Please use a longer password with a mix of characters.")
            elif strength == "Weak":
                st.warning("⚠️ Your password is weak. Consider adding more complexity.")
            elif strength == "Moderate":
                st.info("🟠 Your password is moderate. It could be stronger with more variety.")
            elif strength == "Strong":
                st.success("✅ Your password is strong! Good job.")
            elif strength == "Very Strong":
                st.success("🎉 Your password is very strong! Excellent.")
                
        # Logout button    
        if st.sidebar.button("Logout"):
            st.session_state.login_status = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
