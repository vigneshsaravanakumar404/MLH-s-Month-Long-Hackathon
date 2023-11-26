import streamlit as st
import hmac
import time
import toml

def app():
    st.header("Register for Recycle AI")
    st.write("Create an account to use Recycle AI.")


def check_password():
  """Returns `True` if the user had a correct password."""
  

  def login_form():
      """Form with widgets to collect user information"""
      with st.form("Credentials"):
          st.text_input("Username", key="username")
          st.text_input("Password", type="password", key="password")
          st.text_input("Confirm Password", type="password", key="cp")
          st.form_submit_button("Sign Up", on_click=password_entered)

  def password_entered():
      """Checks whether a password entered by the user is correct."""
      secrets_file_path = ".streamlit/secrets.toml"
      with open(secrets_file_path, "r") as f:
        secrets = toml.load(f)
      new_secret_name = st.session_state["username"]
      new_secret_value = st.session_state["password"]
      secrets[new_secret_name] = new_secret_value

      with open(secrets_file_path, "w") as f:
          st.secrets.dump(secrets, f)
    
      if st.session_state["username"] in st.secrets[
          "passwords"
      ] and hmac.compare_digest(
          st.session_state["password"],
          st.secrets.passwords[st.session_state["username"]],
      ):
          st.session_state["password_correct"] = True
          del st.session_state["password"]  # Don't store the username or password.
          del st.session_state["username"]
      else:
          st.session_state["password_correct"] = False

  # Return True if the username + password is validated.
  if st.session_state.get("password_correct", False):
      return True

  # Show inputs for username + password.
  login_form()
  if "password_correct" in st.session_state:
      st.error("😕 User not known or password incorrect")
  return False


if not check_password():
  st.stop()

# TODO: by Aryan
# Use https://docs.streamlit.io/library/api-reference for reference
# You need to use auth0 to register new uersers
# Idk how auth0 works, but if you need to store any data (not already stored in auth0) then you should try to use a JSON file
# ...or one of the sponsors
# CREATE A NEW BRANCH
# DO NOT PUSH TO MAIN
# Make the page look good. Use other examples on the website for reference.
