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
import requests


def get_data_ritmo():
    data = requests.get("http://177.52.21.58:3000/backend/maf/buscarRitmoProducao")
    json_data = data.json()
    df_piv_2=pd.json_normalize(json_data)
    df_piv_2 = pd.DataFrame.from_dict(df_piv_2)

    df = pd.DataFrame(df_piv_2)

    return df


