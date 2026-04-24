import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="UET Lahore Result", page_icon="📝")

st.title("📝 Student Marks Portal")
st.write("Apni University Email enter karke marks dekhen.")

# Data load karne ka function
@st.cache_data
def load_data():
    # 'marks.csv' file aapke project folder mein honi chahiye
    return pd.read_csv('marks.csv')

try:
    df = load_data()
    # Email columns ko clean karna (spaces khatam karna)
    df['Email'] = df['Email'].str.strip().str.lower()

    # Input Box
    input_email = st.text_input("University Email ID:").strip().lower()

    if st.button("Show My Marks"):
        if input_email:
            # Email search karna
            result = df[df['Email'] == input_email]
            
            if not result.empty:
                marks_obtained = result['Marks'].values[0]
                st.success(f"Aapke marks hain: **{marks_obtained}**")
                st.balloons()
            else:
                st.error("Ye Email list mein nahi mili. Baraye meherbani sahi email likhen.")
        else:
            st.warning("Pehle Email enter karen.")

except FileNotFoundError:
    st.error("Error: 'marks.csv' file nahi mili. Folder check karen.")
