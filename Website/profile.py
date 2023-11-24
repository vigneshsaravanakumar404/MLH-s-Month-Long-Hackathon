import streamlit as st  

def app():
    st.header(f"{st.session_state['username']}'s Profile")
    st.write("Profile details and settings.")