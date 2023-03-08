# -*- coding: utf-8 -*-
"""
decision_xapp.py, Decision service.

@author: Team AutoMato
"""
import json

from ricxappframe.xapp_frame import Xapp

from auto_mato.common import _RMR_PORT
from decision import basic_decider


def parse_decision_message(message: dict) -> dict:
    return message


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
            for (message, raw_message) in messages:
                # Need to free the raw_message to prevent memory leaks
                if message:
                    print(f"Received message: {message}")

                    # Parse message
                    decider_inputs = parse_decision_message(
                        json.loads(message["payload"])
                    )

                    # Call the decision function
                    print(f"\nDecider inputs (Estimated PRB utilization %): {decider_inputs}")
                    _result = basic_decider(**decider_inputs)

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
