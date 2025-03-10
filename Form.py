import streamlit as st
import os
import requests
import time

# Your Flask server running on PC
YOUR_PC_IP = "http://192.168.100.5000"

# Streamlit UI Setup
st.set_page_config(page_title="User System", page_icon="🔑", layout="centered")

# 🎨 Apply Custom Styling
st.markdown("""
    <style>
    .stTextInput, .stButton > button {
        font-size: 18px !important;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 10px;
        font-size: 16px;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# Function to send login request to Flask server
def login_user(username, password):
    """Send login request to Flask backend"""
    url = f"{YOUR_PC_IP}/login"
    data = {"username": username, "password": password}

    try:
        response = requests.post(url, json=data)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}

# Function to send register request to Flask server
def register_user(username, password):
    """Send register request to Flask backend"""
    url = f"{YOUR_PC_IP}/store_credentials"
    data = {"username": username, "password": password}

    try:
        response = requests.post(url, json=data)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}

# 🎭 Sidebar Menu
action = st.sidebar.radio("🔍 Choose Action", ["Login", "Register"])

# 🚀 Login Page
if action == "Login":
    st.title("🔐 Login to Your Account")

    username = st.text_input("👤 Username", placeholder="Enter your username")
    password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")

    if st.button("Login"):
        if not username or not password:
            st.error("⚠️ Please enter both username and password!")
        else:
            response = login_user(username, password)
            if response["status"] == "success":
                st.success("✅ Login Successful! Redirecting...")
                time.sleep(2)  # Simulate loading time
                st.balloons()  # 🎉 Celebration effect
            else:
                st.error(f"❌ {response['message']}")

# 🆕 Registration Page
if action == "Register":
    st.title("📝 Register a New Account")

    username = st.text_input("👤 Choose a Username", placeholder="Enter a new username")
    password = st.text_input("🔑 Create a Password", type="password", placeholder="Enter a strong password")
    confirm_password = st.text_input("🔐 Confirm Password", type="password", placeholder="Re-enter password")

    if st.button("Register"):
        if not username or not password or not confirm_password:
            st.warning("⚠️ Please fill all the fields!")
        elif password != confirm_password:
            st.error("❌ Passwords do not match!")
        else:
            response = register_user(username, password)
            if response["status"] == "success":
                st.success("🎉 Registration Successful! You can now log in.")
                st.balloons()  # 🎈 Fun effect!
            else:
                st.error(f"❌ {response['message']}")
