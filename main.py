import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import plotly.express as px
import pandas as pd

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

            # plotando gráfico simples
            # df = px.data.gapminder().query("year == 2007")
            # fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent",
            # hover_name="country", log_x=True, size_max=60)
            # st.plotly_chart(fig)

        try:
            # carregando o csv do banco de dados
            df = pd.read_csv(
                'data/BASE_UTILIZACAO_PHARMA_E_2017_2021.csv',
                encoding='ISO-8859-1',
                sep=';',
                names=['Comp_Atendimento', 'Data Atendimento', 'NR_ASSOCIADO', 'CID', 'Descrição do CID', 'Grupo Serviço', 'Sub Grupo Serviço',
                       'Cód. Serviço', 'Descrição do Serviço', 'COD_PRESTADOR', 'Sgl_UF_Prestador', 'Especialidade', 'QTD', 'Custo'],
                nrows=10000
            )

            # Exibindo algumas informações do dataset
            st.write('Informações do dataset')
            st.dataframe(df)

        except Exception as e:
            st.error(f"Erro ao tentar abrir o csv: {e}")

elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')
