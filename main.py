import streamlit as st
import re

def check_password_strength(password):
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

# Streamlit app
st.title("Password Strength Meter")
st.write("Enter a password to check its strength:")

password = st.text_input("Password:", type="password")

if password:
    strength, score, color = check_password_strength(password)
    
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
