from base64 import b16decode
from math import ceil
from ipython_genutils.py3compat import buffer_to_bytes
from requests import HTTPError
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
from dateutil.parser import parse
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
from torch import true_divide


def embaladeira_dash():
    dataset_url = 'https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv'

    # Dessa forma, evito o download do conjunto de dados repetidas vezes !!! ## NAO IMPOTA O QUE EU FAÇA A BASE SEMPRE VAI SER A MESMA, ELA FICA ARMAZENADA
    # POSSO UTIIZAR ESSA LOGICA PARA IMPORTAR AS BASES DE DADOS DOS HISTORICOS DE QUALIDADE E CALIBRES DO TALHAO
    # IMPORTO SOMENTE UMA VEZ E ELA FICA SALVA

    @st.experimental_memo
    def get_data() -> pd.DataFrame:
        return pd.read_csv(dataset_url)

    df = get_data()
    df

    test_input = st.number_input('Digite um valor:',value = 2)
    st.write(test_input)


    st.title("Real-Time / Live Data Science Dashboard")


    job_filter = st.selectbox("Select the Job", pd.unique(df["job"]))   ### ESSA LOGICA SERVE TAMVBEM PARA  FILTRO DE ITENS EM UMA COLUNA DE UMA BASE

    df = df[df["job"] == job_filter]
    df

    for seconds in range(10):
        
        df["age_new"] = df["age"] * np.random.choice(range(1, 5))
        df["balance_new"] = df["balance"] * np.random.choice(range(1, 5))
        time.sleep(1)

    placeholder = st.empty()

    with placeholder.container():

        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label="Age ⏳",
            value=round(np.mean(df['age'])),
            delta=round(np.mean(df['age'])) - 10,
        )

        fig_col1, fig_col2 = st.columns(2)
        
        with fig_col1:
            st.markdown("### First Chart")
            fig = px.density_heatmap(
                data_frame=df, y="age_new", x="marital"
            )
            st.write(fig)
            
        with fig_col2:
            st.markdown("### Second Chart")
            fig2 = px.histogram(data_frame=df, x="age_new")
            st.write(fig2)

        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)

    st.write('Em desenvolvimento..')
            