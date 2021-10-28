# -*- coding: utf-8 -*-
"""
decision_xapp.py, Decision service.

@author: Team AutoMato
"""
import json
import queue

from mdclogpy import Logger
from mdclogpy import Level
from ricxappframe.xapp_frame import Xapp

from auto_mato.common import _RMR_MSG_TYPE, _RMR_PORT
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

        try:
            message = self._rmr_loop.rcv_queue.get(block=True, timeout=1)
        except queue.Empty:
            message = None
            pass

        if message:
            (body, raw_message) = message
            logger.info(f"Message body is: {body}")
            # Parse message
            if body["message type"] == _RMR_MSG_TYPE:
                decider_inputs = json.loads(body["payload"])

                # Call the decision function
                logger.info(f"\nDecider inputs (Estimated PRB utilization %): {decider_inputs}")
                _result = basic_decider(**decider_inputs)

            self.rmr_free(raw_message)


if __name__ == "__main__":
    logger.set_level(Level.INFO)
    xapp = Xapp(
        entrypoint=entry,
        rmr_port=_RMR_PORT,
        rmr_wait_for_ready=True,
        use_fake_sdl=True,
    )
    xapp.run()
