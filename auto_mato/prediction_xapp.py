# -*- coding: utf-8 -*-
"""
prediction_xapp.py, Prediction service.

@author: Team AutoMato
"""
import itertools
import json
import os
import time
import random

import numpy as np
from ricxappframe.xapp_frame import Xapp

from auto_mato.common import _RMR_MSG_TYPE, _RMR_PORT
from model_handler import ModelHandler
from prediction import Predictor

_DATA_FOLDER = "/data"
_TIME_SERIES_RANGE = 250
_MODEL_SWITCH_TIME = 10.0
_PREDCTION_START = 50


def generate_input_time_series() -> np.ndarray:
    time_point = itertools.cycle(range(_PREDCTION_START, _TIME_SERIES_RANGE))
    while True:
        yield np.array((next(time_point),)).reshape(-1, 1)


def entry(self):
    print("Starting prediction_xapp loop")

    print("Fetching available models")
    model_handler = ModelHandler()
    print(f"Available models are: {model_handler.models}")

    # Load prediction model, TODO: remove the path and add a proper path in common.py
    model = model_handler.models[0]
    print(f"\nFetching model {model}\n")
    model_handler.pull_model(model)
    predictor_slice1 = Predictor(os.path.join(os.getcwd(), _DATA_FOLDER, model))
    predictor_slice2 = Predictor(os.path.join(os.getcwd(), _DATA_FOLDER, model))

    # Time series data generator, this will be replaced by inbound simulation data
    data = generate_input_time_series()

    not_kill, start_time = True, time.time()
    while not_kill:
        # Healthcheck for RMR and SDL
        if not self.healthcheck():
            self.logger.error("Healthcheck failed. Terminating xApp.")
            not_kill = False

        current_time = time.time()
        # Time check to switch models (demo purposes)
        if current_time - start_time > _MODEL_SWITCH_TIME:
            start_time = current_time
            model_name = random.choice(model_handler.models)
            print(f"\nFetching model {model_name}\n")
            model_handler.pull_model(model_name)
            predictor_slice1.switch_model(os.path.join(os.getcwd(), _DATA_FOLDER, model_name))
            predictor_slice2.switch_model(os.path.join(os.getcwd(), _DATA_FOLDER, model_name))

        # Send predicted values over RMR to decider_xapp
        new_prediction_time = next(data)
        print(f"NEW PREDICTION TIME: {new_prediction_time}")
        
        predicted_value_slice1 = predictor_slice1.predict(new_prediction_time)
        predicted_value_slice2 = predictor_slice2.predict(new_prediction_time)
        

        print(f"Predicted PRB util. for Slice 1: {predicted_value_slice1}")
        print(f"Predicted PRB util. for Slice 2: {predicted_value_slice2}")

        predicted_value = [predicted_value_slice1, predicted_value_slice2]

        val = json.dumps({"prediction": predicted_value}).encode() #predicted value  liste seklşinde gonder iki deger icin
        if not self.rmr_send(val, _RMR_MSG_TYPE):
            print("Error sending rmr message.")

        # RMR returned call from the decision xApp
        for (summary, sbuf) in self.rmr_get_messages():
            print("Returned call: {0}".format(summary))
            self.rmr_free(sbuf)

        time.sleep(2)


if __name__ == "__main__":
    # TODO: We are currently using the fake sdl for development. This should be replaced with redis.
    xapp = Xapp(entrypoint=entry, rmr_port=_RMR_PORT, use_fake_sdl=True)
    xapp.run()
