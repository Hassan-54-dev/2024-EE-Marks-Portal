import streamlit as st
import pandas as pd
import smtplib
import random
from email.mime.text import MIMEText

# --- CONFIGURATION ---
SENDER_EMAIL = "2024ee302@student.uet.edu.pk"
APP_PASSWORD = "awgl btam eate tpyt"

st.set_page_config(page_title="UET Result Portal", page_icon="🔒")

# 1. Data Loading (Simple & Direct)
try:
    # Check karen ke file ka naam GitHub par 'marks.csv' hi hai na?
    df = pd.read_csv('marks.csv')
    df['Email'] = df['Email'].str.strip().str.lower()
except Exception as e:
    st.error(f"CSV Load nahi ho saki: {e}")
    st.stop() # Agar data hi nahi mila to app yahan ruk jaye gi

st.title("🔒 UET Secure Result Portal")

# Session state initialization
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False
if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# Step 1: Email Input
email_input = st.text_input("Enter Email (e.g. 2024ee302@student.uet.edu.pk):").strip().lower()

if st.button("Send OTP"):
    if email_input in df['Email'].values:
        otp = str(random.randint(1000, 9999))
        st.session_state.generated_otp = otp
        st.session_state.user_email = email_input
        
        try:
            msg = MIMEText(f"Aapka OTP ye hai: {otp}")
            msg['Subject'] = f"{otp} is your OTP"
            msg['From'] = SENDER_EMAIL
            msg['To'] = email_input
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(SENDER_EMAIL, APP_PASSWORD)
                server.send_message(msg)
            
            st.session_state.otp_sent = True
            st.success("OTP bhej diya gaya hai!")
        except Exception as e:
            st.error(f"Email Error: {e}")
    else:
        # Debugging: Show first 2 emails to check format
        st.error("Email nahi mili!")
        with st.expander("Admin Debug (Sirf aapke liye)"):
            st.write("File mein pehli 3 emails ye hain:")
            st.write(df['Email'].head(3).tolist())

# Step 2: Verification
if st.session_state.otp_sent:
    otp_received = st.text_input("Enter OTP:", type="password")
    if st.button("Verify Marks"):
        if otp_received == st.session_state.generated_otp:
            marks = df[df['Email'] == st.session_state.user_email]['Marks'].values[0]
            st.success(f"Aapke marks hain: {marks}/30")
            st.balloons()
        else:
            st.error("Galat OTP!")
