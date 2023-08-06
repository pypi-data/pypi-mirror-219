import os, glob
from dataclasses import dataclass
from typing import List

import numpy as np
import copy
from importlib import import_module
from onnc.forest.core.runtime import AbstractRuntimeImplementation

from onnc.forest.core.options import Options, RuntimeSettings
from pydlmeta.identifier.types import ModelFormat


@dataclass
class OpenvinoSettings(RuntimeSettings):
    pass


class OpenvinoOptions(Options):
    model_format = ModelFormat.OPENVINO_IRDIR

    def __init__(self, loadable):
        self.settings: OpenvinoSettings = OpenvinoSettings()
        self.devices: List = ["CPU"]
        self.loadable = loadable


class OpenvinoRuntime(AbstractRuntimeImplementation):

    @staticmethod
    def is_me(options: Options) -> bool:
        return isinstance(options, OpenvinoOptions)

    @staticmethod
    def _get_xml_from_loadable(loadable):
        # If input type is OpenvinoIRDir, search for xml file inside it
        if os.path.isdir(loadable.src):
            xmls = list(
                filter(lambda x: x.endswith(".xml"),
                       glob.glob(f"{loadable.src}/*")))
            if len(xmls) != 1:
                raise RuntimeError(
                    f"OpenvinoIRDir should contain one xml file, found {len(xmls)}"
                )
            return xmls[0]
        if not loadable.src.endswith(".xml"):
            raise RuntimeError(f"OpenvinoRuntime's input file should be .xml, "
                               f"got {loadable.src}")
        return loadable.src

    def __init__(self):
        self.out_buf = None
        self._infer_request = None
        self._compiled_model = None
        self.__ov_runtime = import_module('openvino.runtime')

    def launch(self, options):
        self.core = self.__ov_runtime.Core()
        self.device = options.devices[0]

    def load(self, options):

        xml_path = self._get_xml_from_loadable(options.loadable)
        self._output_names = [
            output.dump()["name"] for output in options.loadable.outputs
        ]
        assert xml_path.endswith(".xml")
        model = self.core.read_model(xml_path)

        # This step is belong to `materialize`
        # However, bind_input() need to use compiled_model
        # to create InferRequest, so, it is a workaround
        # and materialize the model in the step `load`
        self._compiled_model = self.core.compile_model(model, self.device)

    def create_infer_request(self):

        infer_request = self._compiled_model.create_infer_request()
        return infer_request

    def _create_infer_request(self):
        from openvino.runtime.ie_api import InferRequest
        if isinstance(self._infer_request, InferRequest):
            return
        self._infer_request = self._compiled_model.create_infer_request()

    def bind_input(self, input, object):
        self._create_infer_request()

    def bind_output(self, output, object):
        self._create_infer_request()

    def bind_all_inputs(self):
        self._create_infer_request()

    def bind_all_outputs(self):
        self._create_infer_request()

    def materialize(self):
        pass

    def write(self, data):
        if not hasattr(self, '_compiled_model'):
            raise RuntimeError("Please run materialize before running infer")

        if not self._infer_request:
            raise RuntimeError("Please bind inputs and outputs")

        # self._infer_request = self._compiled_model.create_infer_request()
        # for all input node, copy input data
        for i, d in enumerate(data):
            input_tensor = self._infer_request.get_input_tensor(i)
            np.copyto(input_tensor.data, d)

    def run(self):
        if not self._infer_request:
            raise RuntimeError("Please call write() before run")
        self._infer_request.infer()

    def read(self):
        if self._output_names:
            return [
                self._infer_request.get_tensor(
                    self._compiled_model.output(name)).data
                for name in self._output_names
            ]
        # self._infer_request.get_tensor( self._compiled_model.output("bboxes")).data
        return copy.deepcopy(
            [output.data for output in self._infer_request.outputs])


# class OpenvinoAsyncRuntime(AbstractAsyncRuntimeImplementation):

#     def __init__(self):
#         pass

#     def launch(self, settings, devices):
#         pass

#     def load(self, model_path):
#         pass

#     def bind_input(self):
#         pass

#     def bind_output(self):
#         pass

#     def materialize(self):
#         pass

#     def submit(self, data):
#         pass

#     def wait(self):
#         """
#         Nothing to do here since start_async already implements this for us
#         """
#         pass

#     def outcome(self):
#         pass
