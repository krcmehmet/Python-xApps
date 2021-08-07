# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 22:23:00 2021

@author: dtayli
"""
import json

from ricxappframe.xapp_frame import Xapp

from auto_mato.common import _RMR_PORT

#from decision import basic_decider  # TODO: This will be implemented the in file decider.py


T = 100  #Total PRBs of the system


def basic_decider(prediction: float):
    allocated_PRB_to_ES = T- (prediction/100)*T
    print(f"\n Estimated PRB usage of other slice: {(prediction/100)*T}")
    print(f"\n Allocated PRB to Emergency Slice : {allocated_PRB_to_ES }")


def parse_decision_message(input: dict) -> dict:
    return input


def entry(self):
    print("Starting decision_xapp loop")
    not_kill = True
    while not_kill:
        # Healthcheck for RMR and SDL
        if not self.healthcheck():
            print("Healthcheck failed. Terminating xApp.")
            not_kill = False

        messages = self.rmr_get_messages()

        if messages:
            # We are only concerned with the last message.
            message = None
            for (message, raw_message) in messages:
                # Need to free the raw_message to prevent memory leaks
                if message:
                    print(f"Received message: {message}")

                    # Parse message
                    decider_inputs = parse_decision_message(
                        json.loads(message["payload"])
                    )

                    # Call the decision function
                    result = basic_decider(**decider_inputs)
                    print(f"\nDecider inputs: {decider_inputs}")
                    print(f">>> Decider result is: {result}\n")

                    # TODO: Set changes downstream
                self.rmr_free(raw_message)

        else:
            pass  # No message received


if __name__ == "__main__":
    # TODO: We are currently using the fake sdl for development. This should be replaced with redis.
    xapp = Xapp(
        entrypoint=entry,
        rmr_port=_RMR_PORT,
        rmr_wait_for_ready=False,
        use_fake_sdl=True,
    )
    xapp.run()
