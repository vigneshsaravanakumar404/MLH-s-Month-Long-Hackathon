import streamlit as st

def app():
    st.header("Scan")
    st.write("Scan items to recycle them correctly.")

    img_file_buffer = st.camera_input("Take a picture")
    