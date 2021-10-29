# -*- coding: utf-8 -*-
"""
model_handler.py, Fetches models from server.

@author: Team AutoMato
"""
import os
import requests
import urllib.request
from bs4 import BeautifulSoup
import json



# Parse Intent  from Winest Team to read URLs


#with open('/data/source_api.json') as f:  # to be updated and entegrated
#  data_url = json.load(f)
  
_DATA_FOLDER = "./data/"  
  
#with open('/data/model_api.json') as f:  # to be updated and entegrated
#  models_url = json.load(f)

_FILE_SERVER = "http://[::1]:8080"


class ModelHandler:
    def __init__(self):
        self.retrive_model_names()
        self._local_models = []

    def retrive_model_names(self):
        response = requests.get(_FILE_SERVER)
        soup = BeautifulSoup(response.content, "html.parser")
        self._models = [file["href"].strip("/") for file in soup.find_all("a", class_="file", href=True) if file["href"].endswith(".pkl")]
        print(f"The following models are available: {self._models}")

    def pull_model(self, model_name):
        try:
            urllib.request.urlretrieve(os.path.join(_FILE_SERVER, model_name), os.path.join(_DATA_FOLDER, model_name))
        except Exception as err:
            print(f"Couldn't retrive model {model_name}, {err}")

    def switch_model(self, model_name) -> str:
        if model_name not in self._local_models:
            self.pull_model(model_name)
        return model_name

    @property
    def models(self):
        return self._models
