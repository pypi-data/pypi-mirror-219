from typing import List
from dataclasses import dataclass
from onnc.forest.core.runtime import AbstractRuntimeImplementation
from onnc.forest.core.options import Options, RuntimeSettings
from onnc.forest.core.runtime import make_runtime

from onnc.bench.core.model.model import Model
import time

@dataclass
class ProxySettings(RuntimeSettings):
    pass


class ProxyOptions(Options):

    def __init__(self, loadable):
        self.settings: ProxySettings = ProxySettings()
        self.devices: List = []
        self.loadable: Model = loadable
        self._encapsulation: List = []

    @staticmethod
    def is_me(format) -> bool:
        return False # This runtime should be used manually


class RuntimeProxy(AbstractRuntimeImplementation):

    def __init__(self, options):
        self.options = options
        self._options_ = self.options._encapsulation[0]
        self._runtime_ = make_runtime(self._options_)

    def launch(self, options: Options):
        self._runtime_.launch(self._options_)

    def load(self, options: Options):
        self._runtime_.load(self._options_)

    def bind_input(self, *args, **kwargs):
        self._runtime_.bind_input(*args, **kwargs)

    def bind_output(self, *args, **kwargs):
        self._runtime_.bind_output(*args, **kwargs)

    def bind_all_inputs(self):
        self._runtime_.bind_all_inputs()

    def bind_all_outputs(self):
        self._runtime_.bind_all_outputs()

    def materialize(self):
        self._runtime_.materialize()

    def write(self, data):
        self._runtime_.write(data)

    def run(self):
        self._runtime_.run()

    def read(self):
        self._runtime_.read()
