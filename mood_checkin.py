import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
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
LOG_FILE = "mood_log.csv"

# Create CSV if it doesn't exist
if not os.path.exists(LOG_FILE):
    df = pd.DataFrame(columns=["Date", "Mood", "Note"])
    df.to_csv(LOG_FILE, index=False)

# Page setup
st.set_page_config(page_title="Track & Tell: Feelings Edition", page_icon="😊", layout="centered")
tab1, tab2, tab3, tab4 = st.tabs(["🌈 Mood Check-In", "📊 Mood Chart", "🖨️ Emoji Chart", "📘 About"])
# Tabs



   # 🌈 Mood Check-In
with tab1:
    st.title("Track & Tell: Feelings Edition")
    child = st.selectbox("Who's checking in?", ["Child A", "Child B", "Child C"])
    st.write("Helping kids build emotional awareness through daily check-ins.")
    
    mood = st.radio("How are you feeling today?", ["😄 Happy", "😊 Calm", "😐 Okay", "😢 Sad", "😠 Angry", "😴 Tired", "🤩 Excited"])
    note = st.text_input("Want to tell us more?", "")
    
    
    if st.button("Log Mood"):
        today = datetime.now().strftime("%Y-%m-%d")
        existing = pd.read_csv(LOG_FILE)
        new_entry = pd.DataFrame([[today, child, mood, note]], columns=["Date", "Child", "Mood", "Note"])
        updated = pd.concat([existing, new_entry], ignore_index=True)
        updated.to_csv(LOG_FILE, index=False)
        st.success(f"Mood logged for {today}!")
    
    st.subheader("Recent Mood Entries")
    log_df = pd.read_csv(LOG_FILE)
    st.dataframe(log_df.tail(5))

    st.download_button(
        label="📤 Download Full Mood Log",
        data=log_df.to_csv(index=False),
        file_name="mood_log.csv",
        mime="text/csv"
    )

    
# 📊 Mood Chart
with tab2:
    st.title("Mood Chart")
    log_df = pd.read_csv(LOG_FILE)
    if not log_df.empty:
        mood_counts = log_df["Mood"].value_counts()
        fig, ax = plt.subplots()
        mood_counts.plot(kind="bar", color="#A7C7E7", ax=ax)
        ax.set_title("Mood Frequency")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    else:
        st.info("No mood data yet. Log a mood to see the chart!")

# 🖨️ Emoji Chart
with tab3:
    st.title("Printable Emoji Chart")
    st.write("Use this chart for kids to color or circle how they feel.")

    emojis = ["😄 Happy", "😊 Calm", "😐 Okay", "😢 Sad", "😠 Angry", "😴 Tired", "🤩 Excited"]
    for emoji in emojis:
        st.markdown(f"<div style='font-size:40px;'>{emoji}</div>", unsafe_allow_html=True)

    st.write("Tip: Press Command+P to print this page or save as PDF.")
st.markdown("[Download a printable emoji chart](https://fromunderapalmtree.com/printable-emoji-feelings-chart-for-kids/)")   

# 📘 About
with tab4:
    st.title("About This App")
    st.write("""
    **Track & Tell: Feelings Edition** was created to help children build emotional awareness in a simple, visual, and supportive way.

    Whether you're a teacher guiding a classroom or a parent checking in at home, this tool offers a gentle daily prompt: *“How are you feeling today?”*

    Kids can point to an emoji, color a printable chart, or select their mood digitally — giving grown-ups a quick pulse on how they’re doing emotionally.

    Over time, this helps children:
    - 🧠 Build emotional vocabulary
    - 💬 Express feelings with confidence  
    - 🧒 Develop self-awareness and empathy

    This app is:
    - 🎨 Calm and friendly in design
    - 🖨️ Printable for offline use
    - 📊 Trackable for spotting patterns
    - 🧩 Easy to integrate into homeschool, classroom, or family routines

    Because emotional wellness is just as important as physical health — and every child deserves tools to feel seen, heard, and supported.
    """)

