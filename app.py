import streamlit as kd
kd.title("Login Page")
username = kd.text_input("Username")
password = kd.text_input("Password", type="password")
valid_username = "kavin"
valid_password = "kavin@123"
if kd.button("Login"):
    if username == valid_username and password == valid_password:
        kd.success(" Login successful! Welcome, " + username)
    else:
        kd.error("Invalid username or password")
