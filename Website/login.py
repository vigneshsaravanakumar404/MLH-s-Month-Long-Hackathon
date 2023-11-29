import streamlit as st
import hmac
import time
import toml
import auth0
import json
import requests
import http.client
from auth0.authentication import GetToken
from auth0.management import Auth0, connections
import webbrowser



def app():
  st.header("Login for Recycle AI")
  st.write("Log in to use Recycle AI.")

  AUTH0_DOMAIN = "dev-d5hj6m6f3p5vaiiz.us.auth0.com"
  CLIENT_ID = "Iz8vFz0HJOnuAOqHCUXruG1mn3mWvPi5"
  CLIENT_SECRET = "mrP6L_KXVkQgcniPTE--Xcpz5_Z_pTQPOSPTMJeph7c5tAsIJIy4lHTmPl8PwLwv"

  auth0 = Auth0(AUTH0_DOMAIN, CLIENT_ID, None)

  email = st.text_input("Email")
  username = st.text_input("Username")
  password = st.text_input("Password", type="password")

  if st.button("Login") and username is not None: 

    
      
    
    your_redirect_uri = "https://github.com"
    your_state = "STATE"
  
    # Specify additional parameters if needed
    additional_parameters = {
        "param1": "value1",
        "param2": "value2",
        # Add more parameters as necessary
    }
  
    # Construct the URL with parameters
    url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "response_type": "code",  # or "token" depending on your needs
        "client_id": CLIENT_ID,
        "connection": "Username-Password-Authentication",
        "redirect_uri": your_redirect_uri,
        "state": your_state,
        #**additional_parameters,  # Include additional parameters
    }
  
    # Make the GET request
    response = requests.get(url, params=params)
    st.success('This is a success message!', icon="✅")
    st.sidebar.title("♻️ Recycle AI")
    st.sidebar.markdown("## Navigation")
    pages = ["Home", "About", "Login", "Register"]
    user_choice = st.sidebar.selectbox("Choose a page:", pages)
    st.session_state['logged_in'] = True
    st.session_state['username'] = username
    #webbrowser.open(response.url)
  
    # Print the response
    print(response.url)

  

# Main Streamlit app starts here


app()
