import streamlit as st
import pandas as pd
import smtplib
import random
from email.mime.text import MIMEText

# --- CONFIGURATION ---
SENDER_EMAIL = "2024ee302@student.uet.edu.pk"
APP_PASSWORD = "awgl btam eate tpyt"

# Page Config
st.set_page_config(page_title="UET Secure Result Portal", page_icon="🔒")

@st.cache_data
def load_data():
    return pd.read_csv('marks.csv')

st.title("🔒 UET Lahore - Secure Result Portal")
st.write("Apni University Email enter karen, aapko OTP code bheja jaye ga.")

try:
    df = load_data()
    df['Email'] = df['Email'].str.strip().str.lower()

    if "otp_sent" not in st.session_state:
        st.session_state.otp_sent = False
    if "generated_otp" not in st.session_state:
        st.session_state.generated_otp = None
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""

    # Step 1: Email Input
    email_input = st.text_input("University Email ID:").strip().lower()

    if st.button("Send OTP"):
        if email_input in df['Email'].values:
            otp = str(random.randint(1000, 9999))
            st.session_state.generated_otp = otp
            st.session_state.user_email = email_input
            
            try:
                # Email Content
                email_body = f"Assalam-o-Alaikum,\n\nAapka Result Portal OTP code ye hai: {otp}\n\nKisi ko ye code mat batayen."
                msg = MIMEText(email_body)
                msg['Subject'] = f"{otp} is your Result Portal OTP"
                msg['From'] = SENDER_EMAIL
                msg['To'] = email_input
                
                # Sending Process
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(SENDER_EMAIL, APP_PASSWORD)
                    server.send_message(msg)
                
                st.session_state.otp_sent = True
                st.success(f"OTP aapki email ({email_input}) par bhej diya gaya hai!")
            except Exception as e:
                st.error(f"Email bhejney mein masla hua: {e}")
        else:
            st.error("Ye Email record mein nahi mili!")

    # Step 2: Verification
    if st.session_state.otp_sent:
        st.divider()
        otp_received = st.text_input("Enter 4-Digit OTP Code:", type="password")
        
        if st.button("Verify & Show My Marks"):
            if otp_received == st.session_state.generated_otp:
                student_data = df[df['Email'] == st.session_state.user_email]
                marks = student_data['Marks'].values[0]
                st.success(f"Verified! Aapke marks hain: **{marks}/30**")
                st.balloons()
            else:
                st.error("Galat OTP!")

except FileNotFoundError:
    st.error("Error: 'marks.csv' file nahi mili.")
except Exception as e:
    st.error(f"System Error: {e}")
