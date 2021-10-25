# -*- coding: utf-8 -*-
"""
decision_xapp.py, Decision service.

@author: Team AutoMato
"""
import json
import time

from ricxappframe.xapp_frame import Xapp

from auto_mato.common import _RMR_MONITOR_MSG_TYPE, _RMR_PORT


def entry(self):
    print("Starting decision_xapp loop")
    not_kill = True
    while not_kill:
        # Healthcheck for RMR and SDL
        if not self.healthcheck():
            print("Healthcheck failed. Terminating xApp.")
            not_kill = False

        val = json.dumps({"hello": "world"}).encode()
        if not self.rmr_send(val, _RMR_MONITOR_MSG_TYPE):
            print("Error sending rmr message.")
        else:
            pass  # No message received

        # RMR returned call from the prediction xApp
        for (summary, sbuf) in self.rmr_get_messages():
            print("Returned call: {0}".format(summary))
            self.rmr_free(sbuf)

        time.sleep(2)


if __name__ == "__main__":
    xapp = Xapp(
        entrypoint=entry,
        rmr_port=_RMR_PORT,
        rmr_wait_for_ready=False,
        use_fake_sdl=False,
    )
    xapp.run()
