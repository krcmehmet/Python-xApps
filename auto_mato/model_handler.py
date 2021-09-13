# -*- coding: utf-8 -*-
"""
model_handler.py, Fetches models from server.

@author: Team AutoMato
"""
import os
import requests
import urllib.request
from bs4 import BeautifulSoup

from .prediction_xapp import _DATA_FOLDER


# TODO: Fetch models from server
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
            urllib.request.urlretrieve("/" + model_name, os.path.join(_DATA_FOLDER, model_name))
        except Exception as err:
            print(f"Couldn't retrive model {model_name}, {err}")

    def switch_model(self, model_name):
        if model_name not in self._local_models:
            self.pull_model(model_name)

    @property
    def models(self):
        return self._models
