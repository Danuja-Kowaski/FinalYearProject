import streamlit as st
import json
import requests
from streamlit_option_menu import option_menu
import time

st.set_page_config(layout="wide")


def main():
    if "token" in st.session_state:
        nav()
    else:
        if "selected" in st.session_state:
            if st.session_state.selected == "register":
                signup()
            else:
                login()
        else:
            login()


def nav():
    selected = option_menu(
        menu_title=None,
        options=["Information Page", "Home"],
        icons=["info-circle-fill", "house-door-fill"],
        default_index=0,
        orientation="horizontal"
    )
    if selected == "Information Page":
        info()
    elif selected == "Home":
        home()


def signup():
    st.title("ASCSAS - An automated smart contract security auditing system")
    st.subheader("Create an Account")
    new_user = st.text_input('Username')
    new_email = st.text_input('Email')
    new_passwd = st.text_input('Password', type='password')
    if st.button('Login'):
        st.session_state.selected = "login"
        st.experimental_rerun()
    if st.button('SignUp'):
        url = 'http://127.0.0.1:8000/signup'
        data = {
            'username': new_user,
            'email': new_email,
            'password': new_passwd
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            st.success('User created successfully')
            url = 'http://127.0.0.1:8000/login'
            response = requests.post(url, json=data)
            if response.status_code == 200:
                st.session_state.token = response.json()['Token']
                st.experimental_rerun()
            else:
                st.error('Failed to authenticate user')
        else:
            st.error('Failed to create user')


def login():
    st.title("ASCSAS - An automated smart contract security auditing system")
    st.subheader("Login into Account")
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Signup'):
        st.session_state.selected = "register"
        print("work")
        st.experimental_rerun()
    if st.button('Login'):
        url = 'http://127.0.0.1:8000/login'
        data = {
            'username': username,
            'password': password
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            st.success('User logged in successfully')
            st.session_state.token = response.json()['Token']
            st.experimental_rerun()
        else:
            st.error('Failed to authenticate user')


def documentation_pg():
    if "token" in st.session_state:
        st.title("ASCSAS - An automated smart contract security auditing system")
        st.write(
            "Welcome to ASCSAS! This application is designed to help users detect vulnerabilities in smart contracts using deep learning techniques.")
        # Application features
        st.header("Application Features")
        st.subheader("Feature 1: Enter bytecode")
        st.write(
            "This feature allows users to enter a bytecode, update a bytecode, or delete a bytecode .")

        st.subheader("Feature 2: Detection result using Machine Learning")
        st.write(
            "The results of the detection can be seen after the bytecode of a contract is input with its relevant probability")

        # The pages of the application
        st.header("Pages")
        st.subheader("Login/Signin Page")
        st.write(
            "This page will allow users to either login or signin to the application")

        st.subheader("Info Page")
        st.write(
            "This page will provide an overview of the system and its relevant documentation")

        st.subheader("Upload Page")
        st.write(
            "This page will allow the user to enter a bytecode an save it if he/she desires to.")
    else:
        st.text("No access")


def home():
    if "token" in st.session_state:
        # url = 'http://127.0.0.1:8000/pub/contracts'
        # response = requests.get(url)
        # opcodes = response.json()
        # # Display the opcode values as radio buttons, showing only the bytecode1 and bytecode2 fields
        # selected_opcode = st.radio(
        #     "Select an opcode:",
        # )
        st.header("Welcome to ASCSAS!")
        st.text(
            """ASCSAS aims to detect vulnerabilities present in Smart Contract by utilizing deep learning techniques""")
        # st.subheader("Select a smart contract")
        st.subheader("Upload a smart contract")
        opcode = st.text_input('Enter bytecode: ', '0x6080')
        if st.button('Run'):
            url = 'http://127.0.0.1:8000/contract/predict'
            data = {
                'opcode': opcode,
                'Token': st.session_state.token
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                result = response.json().get('result')
                st.write('Result:', result)
                if result == 1:
                    st.warning('Contract is suspected to be vulnerable', icon="⚠️")
                elif result == 2:
                    st.warning('Contract is suspected to be vulnerable', icon="⚠️")
                else:
                    st.success('Contract is safe!', icon="✅")
            else:
                st.error('Failed to upload')
        if st.button('Save'):
            url = 'http://127.0.0.1:8000/contract/save'
            data = {
                'opcode': opcode,
                'Token': st.session_state.token
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                st.success("Successfully saved contract")
            else:
                st.error('Failed to upload')
    else:
        st.text("No access")


def info():
    if "token" in st.session_state:
        st.write(
            "Welcome to ASCSAS! This application is designed to help users detect vulnerabilities in smart contracts using deep learning techniques.")
        # Application features
        st.header("Vulnerabilities detected by ASCSAS")
        st.subheader("Greedy Contracts")
        st.write(
            "This feature allows users to enter a bytecode, update a bytecode, or delete a bytecode .")

        st.subheader("Suicidal Contracts")
        st.write(
            "The results of the detection can be seen after the bytecode of a contract is input with its relevant probability")

        # The pages of the application
        st.header("Other vulnerabilities")
        st.subheader("Reentrancy")
        st.write(
            "This page will allow users to either login or signin to the application")

        st.subheader("Arithmetic Issues")
        st.write(
            "This page will provide an overview of some of the latest vulnerabilities present in smart contracts")

        st.subheader("Access Control")
        st.write(
            "This page will allow the user to enter a bytecode an save it if he/she desires to.")
    else:
        st.text("No access")


# def detection_report():
#     with st.spinner('Wait for it...'):
#         time.sleep(5)
#     st.success('Done!')
#     return


# Set custom fonts
streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Roboto', sans-serif;
			}
			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)

# Disable footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
