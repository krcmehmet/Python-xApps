# -*- coding: utf-8 -*-
"""
decision_xapp.py, Decision service.

@author: Team AutoMato
"""
import json
import queue
import time

from mdclogpy import Logger
from mdclogpy import Level
from ricxappframe.xapp_frame import Xapp

from auto_mato.common import _RMR_MONITOR_MSG_TYPE, _RMR_PORT

logger = Logger(name="Monitor")
logger.mdclog_format_init(configmap_monitor=False)


def entry(self):
    logger.info("Monitor xApp initialized.")
    self.sdl_set("auto_mato", "test", json.dumps(42).encode())
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

        if message:  # We currently are not concerned with message in the monitor xApp
            (body, raw_message) = message
            logger.info(f"Message body is: {body}")
            self.rmr_free(raw_message)

        val = self.sdl_get("auto_mato", "test")
        if not self.rmr_send(val, _RMR_MONITOR_MSG_TYPE):
            logger.error("Error sending rmr message.")
        time.sleep(1)


if __name__ == "__main__":
    logger.set_level(Level.INFO)
    xapp = Xapp(
        entrypoint=entry,
        rmr_port=_RMR_PORT,
        rmr_wait_for_ready=False,
        use_fake_sdl=False,
    )
    xapp.run()
