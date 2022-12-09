import time
import pexpect
import subprocess
import sys
import logging

logger = logging.getLogger("btctl")

class Bluetoothctl:
    def __init__(self):
        subprocess.check_output("rfkill unblock bluetooth", shell=True)
        self.process = pexpect.spawnu("bluetoothctl", echo=False)
    def powercycle(self):
        try:
            self.send("power off", 0.2)
            self.send("power on", 0.5)
        except Exception as e:
            logger.error(e)
            return False
    def send(self, command, pause=0):
        self.process.send(f"{command}\n")
        time.sleep(pause)
        if self.process.expect(["bluetooth", pexpect.EOF]):
            raise Exception(f"failed after {command}")
    def prepare(self, mac_address):
        connect(mac_address)
        access_commands()
    def connect(self, mac_address):
        try:
            self.send(f"connect {mac_address}", 2)
        except Exception as e:
            logger.error(e)
            return False
        else:
            res = self.process.expect(
                ["Failed to connect", "Connection successful", pexpect.EOF]
            )
            return res == 1
    def access_commands(self):
        try:
            self.send(f"menu gatt")
        except Exception as e:
            logger.error(e)
            return False