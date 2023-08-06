from dataclasses import dataclass, field
from typing import List
import numpy as np
from importlib import import_module

from onnc.forest.core.runtime import AbstractRuntimeImplementation
from onnc.forest.core.options import Options, RuntimeSettings
from pydlmeta.identifier.types import ModelFormat


@dataclass
class TensorRTSettings(RuntimeSettings):
    pass


class TensorRTOptions(Options):
    model_format = ModelFormat.TRT_PLAN

    def __init__(self, loadable):
        self.settings: TensorRTSettings = TensorRTSettings()
        self.devices: List = []
        self.loadable = loadable


class TensorRTRuntime(AbstractRuntimeImplementation):

    @staticmethod
    def is_me(options: Options) -> bool:
        return isinstance(options, TensorRTOptions)

    def __init__(self):
        self.__pycuda = import_module('pycuda.driver')
        """"
        WARNING!!! DO NOT REMOVE pycuda.autoinit even if this module
        is not written in the code.
        """
        import_module('pycuda.autoinit')
        self._context = None
        self._inputs: List = []
        self._outputs: List = []
        self._bindings: List = []

    def launch(self, options):
        pass

    def load(self, options):
        import tensorrt as trt

        model_path = str(options.loadable.src)
        TRT_LOGGER = trt.Logger(trt.Logger.INFO)
        with open(model_path, "rb") as f, \
            trt.Runtime(TRT_LOGGER) as runtime:
            self._cuda_engine = runtime.deserialize_cuda_engine(f.read())

    def bind_input(self, input, object):
        # object: and HostDeviceMem object or tuple(host_mem, device_mem)
        from onnc.forest.runtimes.tensorrt.utils import HostDeviceMem

        if isinstance(object, HostDeviceMem):
            self._inputs.append(object)
            self._bindings.append(object.device)
        else:
            assert type(object) in [tuple, list]
            assert len(object) == 2
            assert type(object[0]) is int and type(object[1]) is int
            self._inputs.append(HostDeviceMem(*object))
            self._bindings.append(object[1])

    def bind_output(self, output, object):
        # object: and HostDeviceMem object or tuple(host_mem, device_mem)
        from onnc.forest.runtimes.tensorrt.utils import HostDeviceMem

        if isinstance(object, HostDeviceMem):
            self._outputs.append(object)
            self._bindings.append(object.device)
        else:
            assert type(object) in [tuple, list]
            assert len(object) == 2
            assert type(object[0]) is int and type(object[1]) is int
            self._outputs.append(HostDeviceMem(*object))
            self._bindings.append(object[1])

    def bind_all_inputs(self):
        from onnc.forest.runtimes.tensorrt.utils import allocate_buffers

        self._inputs, self._outputs, self._bindings, _ = \
            allocate_buffers(self._cuda_engine)

    def bind_all_outputs(self):
        pass

    def materialize(self):
        self._context = self._cuda_engine.create_execution_context()

    def write(self, data):
        for i, d in enumerate(data):
            np.copyto(self._inputs[i].host, d.ravel())
        for inp in self._inputs:
            self.__pycuda.memcpy_htod(inp.device, inp.host)

    def run(self):
        if self._context is None:
            raise RuntimeError("Please run materialize before running infer")

        self._context.execute_v2(bindings=self._bindings)

    def read(self):
        for out in self._outputs:
            self.__pycuda.memcpy_dtoh(out.host, out.device)

        return [out.host for out in self._outputs]
