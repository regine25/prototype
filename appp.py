import streamlit as st
import pandas as pd
from io import BytesIO
import os

# --- Set Page Configuration FIRST ---
st.set_page_config(page_title="School Schedule Dashboard", layout="wide")

# --- Check if Excel file exists ---
file_path = "generated_schedulepro.xlsx"
if not os.path.exists(file_path):
    st.error(f"❌ File not found: {file_path}")
    st.stop()  # Stop the app here if the file doesn't exist
else:
    st.success(f"✅ Excel file found: {file_path}")

# --- Load Excel File ---
@st.cache_data
def load_schedule():
    return pd.read_excel(file_path)

df = load_schedule()

st.title("📅 School Schedule Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Schedule")

instructors = st.sidebar.multiselect("Instructor", df["Instructor"].dropna().unique())
rooms = st.sidebar.multiselect("Room", df["Room"].dropna().unique())
sections = st.sidebar.multiselect("Section", df["Section"].dropna().unique())
days = st.sidebar.multiselect("Day", df["Day"].dropna().unique())

# --- Apply Filters ---
filtered_df = df.copy()

if instructors:
    filtered_df = filtered_df[filtered_df["Instructor"].isin(instructors)]
if rooms:
    filtered_df = filtered_df[filtered_df["Room"].isin(rooms)]
if sections:
    filtered_df = filtered_df[filtered_df["Section"].isin(sections)]
if days:
    filtered_df = filtered_df[filtered_df["Day"].isin(days)]

# --- Display Data ---
st.subheader("📋 Filtered Schedule")
st.dataframe(filtered_df, use_container_width=True)

# --- Download Filtered Schedule ---
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Schedule')
    return output.getvalue()

excel_data = to_excel(filtered_df)

st.download_button(
    label="📥 Download as Excel",
    data=excel_data,
    file_name="filtered_schedule.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
import sqlite3
from passlib.hash import bcrypt

# Connect to SQLite database (creates one if it doesn’t exist)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create a table for users
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
""")
conn.commit()
conn.close()
print("✅ Database setup completed!")
import streamlit as st
import sqlite3
from passlib.hash import bcrypt

def register_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    hashed_password = bcrypt.hash(password)  # Hash password securely
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        st.success("✅ Account created successfully!")
    except:
        st.error("❌ Username already exists.")
    
    conn.close()

st.title("🔐 User Registration")

new_username = st.text_input("Enter a username")
new_password = st.text_input("Enter a password", type="password")

if st.button("Register"):
    if new_username and new_password:
        register_user(new_username, new_password)
    else:
        st.warning("⚠️ Please fill all fields.")
def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    record = cursor.fetchone()
    
    if record and bcrypt.verify(password, record[0]):
        return True  # Login Successful
    
    return False  # Login Failed

st.title("🔑 User Login")

login_username = st.text_input("Username")
login_password = st.text_input("Password", type="password")

if st.button("Login"):
    if authenticate_user(login_username, login_password):
        st.success(f"✅ Welcome, {login_username}!")
        # Proceed to dashboard features
    else:
        st.error("❌ Incorrect username or password.")
if "authenticated_user" not in st.session_state:
    st.warning("🔐 Please log in to access the dashboard.")
    st.stop()

st.title("📅 School Schedule Dashboard")
# Add dashboard features here
import streamlit as st
import pandas as pd

# Load the Excel file
file_path = "generated_schedulepro.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")

# Streamlit App UI
st.title("📅 Scheduling Dashboard")
st.write("Here’s the uploaded schedule data:")
st.dataframe(df)  # Displays the DataFrame interactively
