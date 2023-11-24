import streamlit as st

def check_credentials(username, password):
    # Placeholder for actual authentication logic
    # Return True if credentials are valid, False otherwise
    return True if username == "1" and password == "2" else False

def app():
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