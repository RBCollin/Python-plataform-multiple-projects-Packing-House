import pandas as pd
from time import time
from requests import HTTPError

import requests

data2 = requests.get("http://177.52.21.58:3000/backend/maf/percentuaisCalibre")
json_data2 = data2.json()
dataset_MAF = pd.DataFrame.from_dict(json_data2)


def consulta_maf():
    while True:
        url_percentual_MAF = 'http://177.52.21.58:3000/backend/maf/percentuaisCalibre'
        dataset_MAF = pd.read_json(url_percentual_MAF)
        return dataset_MAF
