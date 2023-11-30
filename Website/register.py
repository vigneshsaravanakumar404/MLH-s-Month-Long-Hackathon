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



def app():
  st.header("Register for Recycle AI")
  st.write("Create an account to use Recycle AI.")

  AUTH0_DOMAIN = "dev-d5hj6m6f3p5vaiiz.us.auth0.com"
  CLIENT_ID = "Iz8vFz0HJOnuAOqHCUXruG1mn3mWvPi5"
  CLIENT_SECRET = "mrP6L_KXVkQgcniPTE--Xcpz5_Z_pTQPOSPTMJeph7c5tAsIJIy4lHTmPl8PwLwv"

  auth0 = Auth0(AUTH0_DOMAIN, CLIENT_ID, None)

  email = st.text_input("Email")
  firstname = st.text_input("First Name")
  lastname = st.text_input("Last Name")
  username = st.text_input("Username")
  password = st.text_input("Password", type="password")
  confirm_password = st.text_input("Confirm Password", type="password")


  conn = http.client.HTTPSConnection("dev-d5hj6m6f3p5vaiiz.us.auth0.com")

  payload = "{\"client_id\":\"Iz8vFz0HJOnuAOqHCUXruG1mn3mWvPi5\",\"client_secret\":\"mrP6L_KXVkQgcniPTE--Xcpz5_Z_pTQPOSPTMJeph7c5tAsIJIy4lHTmPl8PwLwv\",\"audience\":\"https://dev-d5hj6m6f3p5vaiiz.us.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}"

  headers = { 'content-type': "application/json" }

  conn.request("POST", "/oauth/token", payload, headers)

  res = conn.getresponse()
  data = res.read()

  response_json = json.loads(data.decode("utf-8"))
  access_token = response_json.get("access_token")


  connn = http.client.HTTPConnection("dev-d5hj6m6f3p5vaiiz.us.auth0.com")

  headers = { 'authorization': f'Bearer {access_token}' }

  connn.request("GET", "/", headers=headers)

  res = connn.getresponse()
  data = res.read()

  

  if st.button("Register"):
      # Check if passwords match
      if password == confirm_password and len(password)>10:

          given_name = firstname
          family_name = lastname
        
          url = "https://dev-d5hj6m6f3p5vaiiz.us.auth0.com/api/v2/users"

          payload = {
            "email": email,
            "user_metadata": {},
            "blocked": False,
            "email_verified": False,
            "app_metadata": {},
            "given_name": given_name,
            "family_name": family_name,
            "name": given_name,
            "nickname": given_name,
            #"picture": "string",
            "user_id": username,
            "connection": "Username-Password-Authentication",
            "password": password,
            "verify_email": False,
            
          }

          headers = {
              'Authorization': f'Bearer {access_token}',
              'Content-Type': 'application/json',
          }

          response = requests.post(url, headers=headers, data=json.dumps(payload))

          #return response.text
          print(response.text)
          if("error" in response.text):
            st.error(response.text)


      st.success('This is a success message!', icon="✅")
      st.sidebar.title("♻️ Recycle AI")
      st.sidebar.markdown("## Navigation")
      pages = ["Home", "About", "Login", "Register"]
      user_choice = st.sidebar.selectbox("Choose a page:", pages)
      st.session_state['logged_in'] = True
      st.session_state['username'] = username


      else:
          st.error("Passwords do not match or password is too weak. Please try again.")

# Main Streamlit app starts here


app()
