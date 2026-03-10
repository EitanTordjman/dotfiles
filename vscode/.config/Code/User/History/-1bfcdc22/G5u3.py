import streamlit as st
import requests

st.title("My Greate App")

peronal_data: dict[str,str|None] = {
    "first_name":None,
    "family_name": None,
    "gender":None,
    "diatery_restrictions":None
}

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
    if submit:
        if not (peronal_data["first_name"] and peronal_data["family_name"]):
            st.warning("The Name Fildes are Mandatory")
        else:
            requests



