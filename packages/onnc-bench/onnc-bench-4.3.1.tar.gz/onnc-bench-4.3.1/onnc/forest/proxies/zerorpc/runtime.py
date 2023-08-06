from typing import List
from dataclasses import dataclass

import zerorpc
import pickle

from onnc.forest.core.options import Options, RuntimeSettings

from onnc.bench.core.model.model import Model
from onnc.forest.proxies import RuntimeProxy
from onnc.forest.proxies.zerorpc.utils import np_to_bytes, np_from_bytes


@dataclass
class ZeroRPCSettings(RuntimeSettings):
    protocol = 'tcp'
    host = '127.0.0.1'
    port = 20000


class ZeroRPCOptions(Options):

    def __init__(self, loadable):
        self.settings: ZeroRPCSettings = ZeroRPCSettings()
        self.devices: List = []
        self.loadable: Model = loadable
        self._encapsulation: List = []

    @staticmethod
    def is_me(format) -> bool:
        return False  # This runtime should be used manually


class ZeroRPCProxy(RuntimeProxy):

    @staticmethod
    def is_me(options: Options) -> bool:
        return isinstance(options, ZeroRPCOptions)

    def __init__(self):
        pass

    def launch(self, options: Options):
        self._runtime_ = zerorpc.Client()
        self._runtime_.connect(
            f"{options.settings.protocol}://{options.settings.host}:{options.settings.port}"
        )
        self.options = options
        self._runtime_.init(pickle.dumps(options))

        options = pickle.dumps(options)
        self._runtime_.launch(options)

    def load(self, options: Options):
        options = pickle.dumps(options)
        self._runtime_.load(options)

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
        self._runtime_.write(np_to_bytes(data))

    def run(self):
        self._runtime_.rpcrun()

    def read(self):
        return np_from_bytes(self._runtime_.read())
