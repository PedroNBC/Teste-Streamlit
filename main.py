import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Tela de login
try:
    authenticator.login()
except Exception as e:
    st.error(e)


if st.session_state['authentication_status']:
    authenticator.logout()
    
    st.write(f'Welcome *{st.session_state["name"]}*')
    x = st.session_state['roles']
    if x is not None:
        if 'admin' in x:
            st.write('Ola Admin')

    st.title('Some content')
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')
