import streamlit as st
import requests

API_URL = "http://localhost:8000"

def signup():
    st.title("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        response = requests.post(f"{API_URL}/signup", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("User created successfully")
        else:
            st.error("Error creating user")

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
        if response.status_code == 200:
            token = response.json().get("access_token")
            st.session_state["token"] = token
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

def create_todo():
    st.title("Create To-Do")
    title = st.text_input("Title")
    description = st.text_input("Description")
    if st.button("Create"):
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        response = requests.post(f"{API_URL}/todos/", json={"title": title, "description": description}, headers=headers)
        if response.status_code == 200:
            st.success("To-Do created successfully")
        else:
            st.error("Error creating To-Do")

def view_todos():
    st.title("View To-Dos")
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{API_URL}/todos/", headers=headers)
    if response.status_code == 200:
        todos = response.json()
        for todo in todos:
            st.write(f"Title: {todo['title']}")
            st.write(f"Description: {todo['description']}")
            st.write("---")
    else:
        st.error("Error fetching To-Dos")

if "token" not in st.session_state:
    login()
else:
    st.sidebar.title("Menu")
    menu = st.sidebar.selectbox("Menu", ["Create To-Do", "View To-Dos", "Logout"])

    if menu == "Create To-Do":
        create_todo()
    elif menu == "View To-Dos":
        view_todos()
    elif menu == "Logout":
        st.session_state.pop("token")
        st.experimental_rerun()
