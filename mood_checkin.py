import streamlit as st
import pandas as pd
import os
import json
import hashlib
from datetime import datetime
import matplotlib.pyplot as plt

# --- Password hashing ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Page setup ---
st.set_page_config(page_title="Track & Tell: Feelings Edition", page_icon="😊", layout="centered")

# --- Styling ---
st.markdown("""
    <style>
        .main {
            background-color: #f5faff;
            font-family: 'Segoe UI', sans-serif;
        }
        .stButton>button {
            background-color: #a3d5ff;
            color: black;
            border-radius: 8px;
            padding: 0.5em 1em;
            font-size: 16px;
        }
        .stRadio label, .stTextInput label, .stSelectbox label {
            font-weight: bold;
            font-size: 18px;
        }
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
        }
        h1 {
            color: #3399ff;
        }
    </style>
""", unsafe_allow_html=True)

# --- User file setup ---
USER_FILE = "users.json"
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

# --- Tabs ---
signup_tab, login_tab, tab1, tab2, tab3, tab4 = st.tabs([
    "🆕 Sign Up", "🔐 Login", "🌈 Mood Check-In", "📊 Mood Chart", "🖨️ Emoji Chart", "📘 About"
])

# --- Sign Up ---
with signup_tab:
    st.title("Create an Account")
    new_name = st.text_input("Your name")
    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")

    if st.button("Sign Up"):
        with open(USER_FILE, "r") as f:
            users = json.load(f)

        if new_username in users:
            st.error("Username already exists. Try another.")
        elif new_name and new_username and new_password:
            hashed_pw = hash_password(new_password)
            users[new_username] = {"name": new_name, "password": hashed_pw}
            with open(USER_FILE, "w") as f:
                json.dump(users, f)
            st.success("Account created! You can now log in.")
        else:
            st.warning("Please fill out all fields.")

# --- Login ---
with login_tab:
    st.title("Login")
    login_username = st.text_input("Username", key="login_user")
    login_password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Log In"):
        with open(USER_FILE, "r") as f:
            users = json.load(f)

        if login_username in users:
            stored_pw = users[login_username]["password"]
            if hash_password(login_password) == stored_pw:
                st.session_state["logged_in"] = True
                st.session_state["username"] = login_username
                st.session_state["name"] = users[login_username]["name"]
                st.success(f"Welcome back, {users[login_username]['name']}!")
            else:
                st.error("Incorrect password.")
        else:
            st.error("Username not found.")

# --- Private CSV per user ---
if st.session_state.get("logged_in"):
    username = st.session_state["username"]
    LOG_FILE = f"{username}_mood_log.csv"
    if not os.path.exists(LOG_FILE):
        df = pd.DataFrame(columns=["Date", "Child", "Mood", "Note"])
        df.to_csv(LOG_FILE, index=False)

# --- 🌈 Mood Check-In ---
with tab1:
    if st.session_state.get("logged_in"):
        st.title("Track & Tell: Feelings Edition")
        st.success(f"Welcome {st.session_state['name']}!")

        # 🔓 Log Out button
        if st.button("Log Out"):
            st.session_state.clear()
            st.experimental_rerun()

        child = st.selectbox("Who's checking in?", ["Child A", "Child B", "Child C"])
        mood = st.radio("How are they feeling?", ["😊 Happy", "😢 Sad", "😠 Angry", "😴 Tired", "😕 Confused"])
        note = st.text_area("Optional note")

        if st.button("Submit Mood"):
            new_entry = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Child": child,
                "Mood": mood,
                "Note": note
            }
            df = pd.read_csv(LOG_FILE)
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv(LOG_FILE, index=False)
            st.success("Mood check-in saved!")

# --- 📊 Mood Chart ---
with tab2:
    if st.session_state.get("logged_in"):
        st.title("📊 Mood Chart")
        st.info("Mood visualizations will appear here once you’ve submitted a few check-ins.")
    else:
        st.warning("Please log in to view your mood chart.")

# --- 🖨️ Emoji Chart ---
with tab3:
    st.title("🖨️ Printable Emoji Chart")
    st.markdown("""
    This chart helps kids express how they feel using emojis.  
    You can print it out and hang it in your classroom or home!

    | Emoji | Feeling   | Description         |
    |-------|-----------|---------------------|
    | 😊    | Happy     | Feeling good, smiling inside |
    | 😢    | Sad       | Feeling down or upset |
    | 😠    | Angry     | Feeling mad or frustrated |
    | 😴    | Tired     | Low energy, needs rest |
    | 😕    | Confused  | Unsure or overwhelmed |
    """)

# --- 📘 About ---
with tab4:
    st.title("📘 About Track & Tell")
    st.markdown("""
    **Track & Tell: Feelings Edition** is a wellness tool designed for families, educators, and kids.  
    It helps children build emotional awareness through daily mood check-ins.

    - ✅ Private, per-user mood logs  
    - ✅ Emoji-based check-ins for accessibility  
    - ✅ Printable resources for classrooms and homes  
    - ✅ Built with privacy-first design

    Created by Adam McCool, founder of Track & Tell Wellness Studio.
    """)
