import streamlit as st
import pandas as pd
import smtplib
import random
from email.mime.text import MIMEText

# --- CONFIGURATION ---
SENDER_EMAIL = "21.6009hassanraza@gmail.com"
APP_PASSWORD = "awgl btam eate tpyt"

st.set_page_config(page_title="UET Result Portal", page_icon="🔒")

# 1. Data Loading
try:
    # Ensure your file on GitHub is named 'marks.csv'
    df = pd.read_csv('marks.csv')
    # Standardize email columns for comparison
    df['UET Email'] = df['UET Email'].str.strip().str.lower()
    df['Personal Email'] = df['Personal Email'].str.strip().str.lower()
except Exception as e:
    st.error(f"Error loading CSV file: {e}")
    st.stop()

st.title("🔒 UET Secure Result Portal")
st.info("Verification is required to access individual academic records.")

# Session state initialization
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False
if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# Step 1: Email Input
email_input = st.text_input("Enter your registered Email (UET or Personal):").strip().lower()

if st.button("Generate OTP"):
    # Search for the email in both columns
    is_uet_email = email_input in df['UET Email'].values
    is_personal_email = email_input in df['Personal Email'].values

    if is_uet_email or is_personal_email:
        otp = str(random.randint(1000, 9999))
        st.session_state.generated_otp = otp
        st.session_state.user_email = email_input
        
        try:
            msg = MIMEText(f"Your One-Time Password (OTP) for the Result Portal is: {otp}")
            msg['Subject'] = f"Verification Code: {otp}"
            msg['From'] = SENDER_EMAIL
            msg['To'] = email_input
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(SENDER_EMAIL, APP_PASSWORD)
                server.send_message(msg)
            
            st.session_state.otp_sent = True
            st.success("OTP has been sent to your email address.")
        except Exception as e:
            st.error(f"Mail Delivery Error: {e}")
    else:
        st.error("Email address not found in the records.")
        with st.expander("Troubleshooting"):
            st.write("Ensure you are using the exact email provided in the class list.")

# Step 2: Verification and Result Display
if st.session_state.otp_sent:
    st.divider()
    otp_received = st.text_input("Enter the 4-digit OTP:", type="password")
    
    if st.button("Verify & View Result"):
        if otp_received == st.session_state.generated_otp:
            # Locate student record based on the email used
            if st.session_state.user_email in df['UET Email'].values:
                student_row = df[df['UET Email'] == st.session_state.user_email]
            else:
                student_row = df[df['Personal Email'] == st.session_state.user_email]
            
            # Extract Details
            student_name = student_row['Name'].values[0]
            marks = student_row['Psychology Marks'].values[0]
            
            st.success(f"Verification Successful!")
            st.balloons()
            
            # Display Result Card
            st.markdown(f"""
            ### Student Report
            * **Name:** {student_name}
            * **Subject:** Psychology
            * **Obtained Marks:** {marks}
            """)
        else:
            st.error("Invalid OTP. Please check your email and try again.")