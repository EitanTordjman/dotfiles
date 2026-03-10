import streamlit as st
import requests

st.title("My Greate App")

peronal_data: dict[str,list[str]| str | None] = {
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
            peronal_data["gender"] = st.radio("Gender",["Male","Female","Other"])
        
        with c2: 
            peronal_data["hobbies"] = st.multiselect("Hobbies",["Movies","Books","Music","Sports"])

    submit = st.form_submit_button()
    if submit:
        if not all(peronal_data.values()):
            st.warning("Please Fill Out All Fildes")
        else:
            response = requests.post("http://127.0.0.1:8000/print_data/",json=peronal_data)
            st.write(response.content)



