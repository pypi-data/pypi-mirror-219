from typing import List
from importlib import import_module
from dataclasses import dataclass
from onnc.forest.core.runtime import AbstractRuntimeImplementation

from onnc.forest.core.options import Options, RuntimeSettings
from onnc.bench.core.model.model import Model
from pydlmeta.identifier.types import ModelFormat

@dataclass
class ONNXSettings(RuntimeSettings):
    ep_list = ['CPUExecutionProvider']
    intra_op_num_threads = 0


class ONNXOptions(Options):
    model_format = ModelFormat.ONNX

    def __init__(self, loadable):
        self.settings: ONNXSettings = ONNXSettings()
        self.devices: List = ["CPU"]
        self.loadable: Model = loadable


class ONNXRuntime(AbstractRuntimeImplementation):

    @staticmethod
    def is_me(options: Options) -> bool:
        return isinstance(options, ONNXOptions)


    def __init__(self):
        self.__ort = import_module('onnxruntime')

    def launch(self, options: ONNXOptions):
        pass

    def load(self, options: ONNXOptions):
        sess_options = self.__ort.SessionOptions()
        sess_options.intra_op_num_threads = (
            options.settings.intra_op_num_threads)
        model_path = str(options.loadable.src)
        self._sess = self.__ort.InferenceSession(
            model_path,
            sess_options=sess_options,
            providers=options.settings.ep_list)
        self._inputs_name = [input.name for input in self._sess.get_inputs()]
        self._outputs_name = [
            output.name for output in self._sess.get_outputs()
        ]

    def bind_input(self, name, obj):
        pass

    def bind_output(self, name, obj):
        pass

    def bind_all_inputs(self):
        pass

    def bind_all_outputs(self):
        pass

    def materialize(self):
        pass

    def write(self, data):
        self._input_data = data

    def run(self):
        self.out_buf = self._sess.run(self._outputs_name, {
            name: data
            for name, data in zip(self._inputs_name, self._input_data)
        })

    def read(self):
        return self.out_buf
