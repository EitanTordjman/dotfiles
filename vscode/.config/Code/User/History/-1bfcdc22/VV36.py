import streamlit as st
import requests

with st.form("Personal Information"):

    st.text_input("First Name")
    st.text_input("Family Name")
    with st.expander("Additional Information"):
        c1,c2 =  st.columns(2)
        with c1: 
            st.radio("Gender",["Male","Female","Other"])
        
        with c2: 
            st.radio("Diatry Restrictions",["Vegetarian","Vegan"])

    st.form_submit_button()


