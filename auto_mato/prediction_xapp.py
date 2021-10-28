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
import queue

import numpy as np

from mdclogpy import Logger
from mdclogpy import Level
from ricxappframe.xapp_frame import Xapp

from auto_mato.common import _RMR_MONITOR_MSG_TYPE, _RMR_MSG_TYPE, _RMR_PORT
from model_handler import ModelHandler
from prediction import Predictor

_DATA_FOLDER = "/data"
_TIME_SERIES_RANGE = 150
_MODEL_SWITCH_TIME = 10.0

logger = Logger(name="Prediction")
logger.mdclog_format_init(configmap_monitor=False)


def generate_input_time_series() -> np.ndarray:
    time_point = itertools.cycle(range(_TIME_SERIES_RANGE))
    while True:
        yield np.array((next(time_point),)).reshape(-1, 1)


def entry(self):
    logger.info("Prediction xApp initialized")

    logger.info("Fetching available models")
    model_handler = ModelHandler()
    logger.info(f"Available models are: {model_handler.models}")

    # Load prediction model, TODO: remove the path and add a proper path in common.py
    model = model_handler.models[0]
    logger.info(f"\nFetching model {model}\n")
    yield model_handler.pull_model(model)
    predictor_slice1 = Predictor(os.path.join(os.getcwd(), _DATA_FOLDER, model))
    predictor_slice2 = Predictor(os.path.join(os.getcwd(), _DATA_FOLDER, model))

    # Time series data generator, this will be replaced by inbound simulation data
    data = generate_input_time_series()

    not_kill, start_time = True, time.time()
    while not_kill:
        # Healthcheck for RMR and SDL
        if not self.healthcheck():
            logger.error("Healthcheck failed. Terminating xApp.")
            not_kill = False

        try:
            message = self._rmr_loop.rcv_queue.get(block=True, timeout=1)
        except queue.Empty:
            message = None
            pass

        if message:
            (body, raw_message) = message
            logger.info("Message body is: {0}".format(body))
            if body["message type"] == _RMR_MONITOR_MSG_TYPE:
                logger.info(f"WE GOT DATA!!!!!!!!! {body['payload']}")

                # Send predicted values over RMR to decider_xapp
                predicted_value_slice1 = predictor_slice1.predict(next(data))
                predicted_value_slice2 = predictor_slice2.predict(next(data))
                predicted_value = [predicted_value_slice1, predicted_value_slice2]

                logger.info(f"Predicted values:  {predicted_value}")


                val = json.dumps({"prediction": predicted_value}).encode() #predicted value
                if not self.rmr_send(val, _RMR_MSG_TYPE):
                    logger.error("Error sending rmr message.")
            else:
                logger.info(f"NO DATA!!!!!!!!! {body}")
                continue  # We don't want to loop over 
            self.rmr_free(raw_message)

        current_time = time.time()
        # Time check to switch models (demo purposes)
        if current_time - start_time > _MODEL_SWITCH_TIME:
            start_time = current_time
            model_name = random.choice(model_handler.models)
            logger.info(f"\nFetching model {model_name}\n")
            model_handler.pull_model(model_name)
            predictor_slice1.switch_model(os.path.join(os.getcwd(), _DATA_FOLDER, model_name))
            predictor_slice2.switch_model(os.path.join(os.getcwd(), _DATA_FOLDER, model_name))


if __name__ == "__main__":
    logger.set_level(Level.INFO)
    xapp = Xapp(entrypoint=entry, rmr_port=_RMR_PORT, use_fake_sdl=True)
    xapp.run()
