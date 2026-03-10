import streamlit as st
import requests

st.title("My Greate App")

peronal_data: dict[str,str|None] = {
    "first_name":None,
    "family_name": None,
    "gender":None,
    "hobbies":None
}

with st.form("Personal Information"):

    peronal_data["first_name"] = st.text_input("First Name")
    peronal_data["family_name"] = st.text_input("Family Name")
    with st.expander("Additional Information"):
        c1,c2 =  st.columns(2)
        with c1: 
            peronal_data["gender"] = st.selectbox("Gender",["Male","Female","Other"])
        
        with c2: 
            peronal_data["hobbies"] = st.selectbox("Hobbies",["Movies","Books","Music"])

    submit = st.form_submit_button()
    if submit:
        if not (peronal_data["first_name"] and peronal_data["family_name"]):
            st.warning("The Name Fildes are Mandatory")
        else:
            for key,value in peronal_data.items():
                st.write(f"{key}: {value}")



