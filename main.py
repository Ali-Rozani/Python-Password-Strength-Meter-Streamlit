import streamlit as st

def check_password_strength(password):
    """
    Evaluate the strength of a password based on length, complexity, etc.
    """
    strength = 0
    feedback = []

    # Check length
    if len(password) >= 8:
        strength += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Check for uppercase letters
    if any(char.isupper() for char in password):
        strength += 1
    else:
        feedback.append("Password should contain at least one uppercase letter.")

    # Check for lowercase letters
    if any(char.islower() for char in password):
        strength += 1
    else:
        feedback.append("Password should contain at least one lowercase letter.")

    # Check for numbers
    if any(char.isdigit() for char in password):
        strength += 1
    else:
        feedback.append("Password should contain at least one number.")

    # Check for special characters
    if any(not char.isalnum() for char in password):
        strength += 1
    else:
        feedback.append("Password should contain at least one special character.")

    # Determine strength level
    if strength == 5:
        return "Strong", feedback
    elif strength >= 3:
        return "Moderate", feedback
    else:
        return "Weak", feedback

def main():
    st.title("Password Strength Meter")

    # Input field for password
    password = st.text_input("Enter your password:", type="password")

    if password:
        # Check password strength
        strength, feedback = check_password_strength(password)

        # Display strength
        st.write(f"Password Strength: **{strength}**")

        # Provide feedback
        if feedback:
            st.write("Suggestions to improve your password:")
            for suggestion in feedback:
                st.write(f"- {suggestion}")

if __name__ == "__main__":
    main()
