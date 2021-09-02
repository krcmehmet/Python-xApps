# -*- coding: utf-8 -*-
"""
prediction_xapp.py, Prediction service.

@author: Team AutoMato
"""
import itertools
import json
import os
import time

import numpy as np
from ricxappframe.xapp_frame import Xapp

from auto_mato.common import _RMR_MSG_TYPE, _RMR_PORT
from prediction import Predictor

_TIME_SERIES_RANGE = 150


def generate_input_time_series() -> np.ndarray:
    time_point = itertools.cycle(range(_TIME_SERIES_RANGE))
    while True:
        yield np.array((next(time_point),)).reshape(-1, 1)


def entry(self):
    print("Starting prediction_xapp loop")

    # Load prediction model, TODO: remove the path and add a proper path in common.py
    predictor_slice1 = Predictor(os.path.join(os.getcwd(), "/data/basic_prediction_model.pkl"))
    predictor_slice2 = Predictor(os.path.join(os.getcwd(), "/data/basic_prediction_model.pkl"))

    # Time series data generator, this will be replaced by inbound simulation data
    data = generate_input_time_series()

    not_kill = True
    while not_kill:
        # Healthcheck for RMR and SDL
        if not self.healthcheck():
            self.logger.error("Healthcheck failed. Terminating xApp.")
            not_kill = False

        # Send predicted values over RMR to decider_xapp
        predicted_value_slice1 = predictor_slice1.predict(next(data))
        predicted_value_slice2 = predictor_slice2.predict(next(data))

        print(f"Predicted value for Slice 1: {predicted_value_slice1}")
        print(f"Predicted value for Slice 2: {predicted_value_slice2}")
        
        predicted_value = [predicted_value_slice1, predicted_value_slice2]

        val = json.dumps({"prediction": predicted_value}).encode() #predicted value  liste seklşinde gonder iki deger icin
        if not self.rmr_send(val, _RMR_MSG_TYPE):
            print("Error sending rmr message.")

        # RMR returned call from the decision xApp
        for (summary, sbuf) in self.rmr_get_messages():
            print("Retuned call: {0}".format(summary))
            self.rmr_free(sbuf)

        time.sleep(2)


if __name__ == "__main__":
    # TODO: We are currently using the fake sdl for development. This should be replaced with redis.
    xapp = Xapp(entrypoint=entry, rmr_port=_RMR_PORT, use_fake_sdl=True)
    xapp.run()
