import streamlit as st
import requests

with st.form("Personal Information"):

    st.text_input("First Name")
    st.text_input("Family Name")

    st.form_submit_button()


