# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 22:23:00 2021

@author: dtayli
"""
import json
import random
import time

from ricxappframe.xapp_frame import Xapp

from auto_mato.common import _RMR_MSG_TYPE, _RMR_PORT

from .prediction import basic_predictor  # TODO: This will be implemented the in file prediction.py


#def basic_predictor() -> float:
#    return random.random()


def entry(self):
    print("Starting prediction_xapp loop")
    not_kill = True
    while not_kill:
        # Healthcheck for RMR and SDL
        if not self.healthcheck():
            self.logger.error("Healthcheck failed. Terminating xApp.")
            not_kill = False

        # Send predicted values over RMR to decider_xapp
        predicted_value = basic_predictor()

        print(f"Predicted value: {predicted_value}")

        val = json.dumps({"prediction": predicted_value}).encode()
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
