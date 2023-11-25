import streamlit as st  

def app():
    st.header(f"{st.session_state['username']}'s Profile")
    st.write("Profile details and settings.")


# TODO: by Aryan
# Use https://docs.streamlit.io/library/api-reference for reference
# You need to use some blockchain thingy to store the number of items recycled by each user. Ill store everything in a JSON file
# and you just need to like make calls to the blockchain thingy each time this page is loaded. So if the person has 15 items recycled. 
# and the last time the blockchain thingy was updated was with 10 items, then you need to add 5 to the blockchain things.
# The profile should have a graph of the number of items recycled per day. And some other cool stats. Its really easy to make graphs
# with streamlit. Just look at the examples. Make it look good. 