import time
from typing import List
from importlib import import_module
from dataclasses import dataclass
import pickle

import zerorpc

from onnc.forest.core.options import Options, RuntimeSettings
from onnc.forest.core.runtime import make_runtime

from onnc.bench.core.model.model import Model
from onnc.forest.core.runtime import make_runtime
from onnc.forest.proxies import RuntimeProxy
from onnc.forest.proxies.zerorpc.utils import np_to_bytes, np_from_bytes


@dataclass
class ZeroRPCServerSettings(RuntimeSettings):
    protocol = 'tcp'
    host = '0.0.0.0'
    port = 20000


class ZeroRPCServerOptions(Options):
    def __init__(self, loadable):
        self.settings: ZeroRPCServerSettings = ZeroRPCServerSettings()
        self.devices: List = []
        self.loadable: Model = loadable
        self._encapsulation: List = []

    @staticmethod
    def is_me(format) -> bool:
        return False # This runtime should be used manually


class ZeroRPCServerProxy(RuntimeProxy):
    def __init__(self, options):
        pass

    def init(self, options):
        options = pickle.loads(options)
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
        data = np_from_bytes(data)
        self._runtime_.write(data)

    def rpcrun(self):
        self._runtime_.run()

    def run(self):
        raise Exception('ZeroRPC cannot use `run` as method name')

    def read(self):
        return np_to_bytes(self._runtime_.read())

if __name__ == "__main__":
    opt = ZeroRPCServerOptions(None)
    s = zerorpc.Server(ZeroRPCServerProxy(opt))
    s.bind(f"{opt.settings.protocol}://{opt.settings.host}:{opt.settings.port}")
    s.run()