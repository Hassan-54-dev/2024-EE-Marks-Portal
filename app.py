import streamlit as st
import pandas as pd
import smtplib
import random
from email.mime.text import MIMEText

# --- CONFIGURATION ---
SENDER_EMAIL = "21.6009hassanraza@gmail.com"  # Aapki apni Gmail
APP_PASSWORD = "awgl btam eate tpyt"     # Jo Google se liya tha

@st.cache_data
def load_data():
    return pd.read_csv('marks.csv')

st.title("🔒 Secure Student Portal")

df = load_data()
df['Email'] = df['Email'].str.strip().str.lower()

# Step 1: Email Verification
email_input = st.text_input("Enter University Email:").strip().lower()

if "otp" not in st.session_state:
    st.session_state.otp = None
if "verified_email" not in st.session_state:
    st.session_state.verified_email = None

if st.button("Send OTP"):
    if email_input in df['Email'].values:
        otp = str(random.randint(1000, 9999))
        st.session_state.otp = otp
        st.session_state.verified_email = email_input
        
        # Email Sending Logic
        try:
            msg = MIMEText(f"Aapka Result Portal OTP code ye hai: {otp}")
            msg['Subject'] = "Your OTP Code"
            msg['From'] = SENDER_EMAIL
            msg['To'] = email_input
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(SENDER_EMAIL, APP_PASSWORD)
                server.send_message(msg)
            st.success("OTP aapki email par bhej diya gaya hai!")
        except Exception as e:
            st.error("Email bhejney mein masla hua. Check App Password.")
    else:
        st.error("Email list mein nahi mili!")

# Step 2: OTP Verification
if st.session_state.otp:
    otp_input = st.text_input("Enter 4-Digit OTP:")
    if st.button("Verify & Show Marks"):
        if otp_input == st.session_state.otp:
            user_data = df[df['Email'] == st.session_state.verified_email]
            marks = user_data['Marks'].values[0]
            st.success(f"Aapke marks hain: {marks}")
            st.balloons()
        else:
            st.error("Galat OTP!")
except FileNotFoundError:
    st.error("Error: 'marks.csv' file nahi mili. Folder check karen.")
