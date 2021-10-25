# -*- coding: utf-8 -*-
"""
decision_xapp.py, Decision service.

@author: Team AutoMato
"""
import json
import time

from mdclogpy import Logger
from mdclogpy import Level
from ricxappframe.xapp_frame import Xapp

from auto_mato.common import _RMR_MONITOR_MSG_TYPE, _RMR_PORT

logger = Logger(name="Monitor")
logger.mdclog_format_init(configmap_monitor=False)


def entry(self):
    logger.info("Monitor xApp initialized.")
    print("Starting monitor_xapp loop")
    self.sdl_set("auto_mato", "test", json.dumps(42).encode())
    not_kill = True
    while not_kill:
        logger.info("Hello World")
        # Healthcheck for RMR and SDL
        if not self.healthcheck():
            logger.error("Healthcheck failed. Terminating xApp.")
            not_kill = False

        val = json.dumps({"hello": "world"}).encode()
        if not self.rmr_send(val, _RMR_MONITOR_MSG_TYPE):
            logger.error("Error sending rmr message.")
        else:
            pass  # No message received

        # RMR returned call from the prediction xApp
        for (summary, sbuf) in self.rmr_get_messages():
            logger.info("Returned call: {0}".format(summary))
            self.rmr_free(sbuf)

        time.sleep(2)


if __name__ == "__main__":
    logger.set_level(Level.INFO)
    xapp = Xapp(
        entrypoint=entry,
        rmr_port=_RMR_PORT,
        rmr_wait_for_ready=False,
        use_fake_sdl=False,
    )
    xapp.run()
