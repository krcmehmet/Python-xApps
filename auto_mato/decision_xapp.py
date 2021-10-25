# -*- coding: utf-8 -*-
"""
decision_xapp.py, Decision service.

@author: Team AutoMato
"""
import json

from mdclogpy import Logger
from mdclogpy import Level
from ricxappframe.xapp_frame import Xapp

from auto_mato.common import _RMR_PORT
from decision import basic_decider

logger = Logger(name="Decision")
logger.mdclog_format_init(configmap_monitor=False)


def entry(self):
    logger.info("Decision xApp initialized")
    not_kill = True
    while not_kill:
        # Healthcheck for RMR and SDL
        if not self.healthcheck():
            logger.error("Healthcheck failed. Terminating xApp.")
            not_kill = False

        messages = self.rmr_get_messages()

        if messages:
            # We are only concerned with the last message.
            for (message, raw_message) in messages:
                # Need to free the raw_message to prevent memory leaks
                if message:
                    logger.info(f"Received message: {message}")

                    # Parse message
                    decider_inputs = json.loads(message["payload"])

                    # Call the decision function
                    logger.info(f"\nDecider inputs (Estimated PRB utilization %): {decider_inputs}")
                    _result = basic_decider(**decider_inputs)

                    # TODO: Set changes downstream
                self.rmr_free(raw_message)

        else:
            pass  # No message received


if __name__ == "__main__":
    logger.set_level(Level.INFO)
    xapp = Xapp(
        entrypoint=entry,
        rmr_port=_RMR_PORT,
        rmr_wait_for_ready=False,
        use_fake_sdl=True,
    )
    xapp.run()
