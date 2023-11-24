import streamlit as st
import home
import learn 
import login
import profile
import register
import scan

# Page configuration
st.set_page_config(page_title='Recycle AI', page_icon='♻️', layout='wide')

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Sidebar content
st.sidebar.title("♻️ Recycle AI")
st.sidebar.markdown("## Navigation")

# Navigation Bar
if st.session_state['logged_in']:
    pages = ["Profile", "Scan", "Learn", "Account", "Logout"]
else:
    pages = ["Home", "About", "Login", "Register"]
user_choice = st.sidebar.selectbox("Choose a page:", pages)

# Pages for non-logged-in users
if user_choice == "Home":
    home.app()
elif user_choice == "Login" and not st.session_state['logged_in']:
    login.app()
elif user_choice == "Register" and not st.session_state['logged_in']:
    register.app()
elif user_choice == "Logout":
    st.session_state['logged_in'] = False
    st.rerun()

# Pages for logged-in users
if st.session_state['logged_in']:
    if user_choice == "Profile":
        profile.app()
    elif user_choice == "Scan":
        scan.app()
    elif user_choice == "Learn":
        learn.app()