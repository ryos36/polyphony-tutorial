from polyphony import testbench, module, is_worker_running
from polyphony.timing import clksleep
from polyphony.io import Port
from polyphony.typing import bit
from configs import Config

@module
class Blink:
    def __init__(self, interval):
        self.led = Port(bit, 'out')
        self.interval = interval
        self.append_worker(self.main)

    def main(self):
        led:bit = 1
        while is_worker_running():
            self.led(led)
            led = ~led
            self._wait()

    def _wait(self):
        for i in range(self.interval // 2):
            pass


blink = Blink(10)

@testbench
def test(blink):
    clksleep(100)

test(blink)
