import streamlit as st
from pymongo import MongoClient
import hashlib

# MongoDB connection
def connect_to_mongodb():
    try:
        # Replace with your MongoDB connection string
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        db = client["streamlit_auth"]  # Database name
        collection = db["users"]  # Collection name
        client.server_info()  # Test connection
        st.success("Connected to MongoDB successfully!")
        return collection
    except Exception as e:
        st.error(f"Failed to connect to MongoDB: {e}")
        st.error("Please ensure MongoDB is running and accessible.")
        return None

# Hash password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Check if user exists
def user_exists(username, collection):
    return collection.find_one({"username": username}) is not None

# Register new user
def register_user(username, password, collection):
    if user_exists(username, collection):
        return False
    hashed_password = hash_password(password)
    collection.insert_one({"username": username, "password": hashed_password})
    return True

# Authenticate user
def authenticate_user(username, password, collection):
    user = collection.find_one({"username": username})
    if user and user["password"] == hash_password(password):
        return True
    return False

# Streamlit app
def main():
    st.title("Login/Registration System")

    # Connect to MongoDB
    collection = connect_to_mongodb()
    if collection is None:
        st.stop()  # Stop the app if MongoDB connection fails

    # Login/Registration toggle
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate_user(username, password, collection):
                st.success("Logged in successfully!")
                # Redirect to another website
                st.markdown("[Go to Password Strength Meter](https://www.password-strength-meter-app.streamlit.app)")
            else:
                st.error("Invalid username or password")

    elif choice == "Register":
        st.subheader("Register")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")

        if st.button("Register"):
            if register_user(new_username, new_password, collection):
                st.success("Registration successful! Please login.")
            else:
                st.error("Username already exists")

if __name__ == "__main__":
    main()
