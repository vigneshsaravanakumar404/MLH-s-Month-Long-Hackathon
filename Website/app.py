import streamlit as st
import about
import account
import home
import learn 
import login
import profile
import register
import scan

# Page configuration
st.set_page_config(page_title='Recycle AI', page_icon='♻️', layout='wide')

# Function to validate login credentials
def check_credentials(username, password):
    # Placeholder for actual authentication logic
    # Return True if credentials are valid, False otherwise
    return True if username == "admin" and password == "password" else False

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Sidebar content
st.sidebar.title("♻️ Recycle AI")
st.sidebar.markdown("## Navigation")

# Define navigation options based on login status
if st.session_state['logged_in']:
    pages = ["Profile", "Scan", "Learn", "Account", "Logout"]
else:
    pages = ["Home", "About", "Login", "Register"]

# Sidebar selectbox for navigation
user_choice = st.sidebar.selectbox("Choose a page:", pages)

# Navigation and page content
if user_choice == "Home":
    st.header("Welcome to Recycle AI")
    st.write("This is the home page of our application.")
elif user_choice == "About":
    st.header("About Recycle AI")
    st.write("Learn more about Recycle AI.")
elif user_choice == "Login" and not st.session_state['logged_in']:
    st.title('Login to Recycle AI')
    input_username = st.text_input("Username", key='input_username')
    input_password = st.text_input("Password", type="password", key='input_password')

    if st.button('Login'):
        if check_credentials(input_username, input_password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = input_username 
            st.success(f"Welcome {input_username}!")
            st.experimental_rerun()
        else:
            st.error("Incorrect username or password")
elif user_choice == "Register" and not st.session_state['logged_in']:
    st.header("Register for Recycle AI")
    st.write("Create an account to use Recycle AI.")
elif user_choice == "Logout":
    st.session_state['logged_in'] = False
    st.experimental_rerun()

# Pages for logged-in users
if st.session_state['logged_in']:
    if user_choice == "Profile":
        st.header(f"{st.session_state['username']}'s Profile")
        st.write("Profile details and settings.")
    elif user_choice == "Scan":
        scan.app()
    elif user_choice == "Learn":
        learn.app()
    elif user_choice == "Account":
        account.app()