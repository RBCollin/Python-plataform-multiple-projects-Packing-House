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
from PIL import Image
import random



def meta_ph():
    placeholder = st.empty()
    start_button = st.empty()








    def radar_chart():  
        df = pd.DataFrame(dict(
        r=[random.randint(0,22),
        random.randint(0,22),
        random.randint(0,22),
        random.randint(0,22),
        random.randint(0,22)],
        theta=['processing cost','mechanical properties','chemical stability',
            'thermal stability', 'device integration']))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        placeholder.write(fig)


    if start_button.button('Start',key='start'):

        start_button.empty()
        if st.button('Stop',key='stop'):
            pass
        while True:
            radar_chart()
            time.sleep(10)