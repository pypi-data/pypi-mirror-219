from pathlib import Path
from typing import Dict, Union, List
from typing_extensions import Literal
from pathlib import Path
import os
import json
import shutil
import logging

from loguru import logger
from onnc.bench.core.deployment import Deployment
from .builder import IBuilder
from onnc.bench.core.common import get_tmp_path
from . import Compilation


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


class NNUXEBuilder(IBuilder):
    BUILDER_NAME = "NNUXEBuilder"

    def __init__(self):
        self._compilations: Dict[int, Compilation] = {}
        self.output_path: str = ""
        self._builder_log_level = 'DEBUG'

    def set_builder_log_level(self, level: Literal['DEBUG', 'INFO', 'WARN',
                                                   'ERROR', 'CRITICAL']):
        if level not in ('DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'):
            return self._builder_log_level
        self._builder_log_level = self._builder_log_level
        if level == "DEBUG":
            self._builder_log_level = logging.DEBUG
        elif level == "INFO":
            self._builder_log_level = logging.INFO
        elif level == "WARN":
            self._builder_log_level = logging.WARN
        elif level == "ERROR":
            self._builder_log_level = logging.ERROR
        elif level == "CRITICAL":
            self._builder_log_level = logging.CRITICAL

    def _compile(self,
                 model_name,
                 model_path: str,
                 sample_path: str,
                 params_path: str,
                 output_path: str,
                 local_nnuxe: bool = True):

        from nnuxe.drivers.compiler import compile as nnuxe_compile
        from nnuxe.core.report import CompileReport
        report = CompileReport()
        nnuxe_compile(model_path,
                      sample_path,
                      params_path,
                      os.path.join(output_path, model_name),
                      report,
                      local_nnuxe=local_nnuxe,
                      log_level=self._builder_log_level)
        return report

    def build(self, target: str, converter_params={}) -> Dict:

        output_path = get_tmp_path()
        os.makedirs(output_path, exist_ok=True)

        # Upload files and create compilation
        res = {}

        for idx, iternal_cid in enumerate(self._compilations):
            params = {}
            compilation = self._compilations[iternal_cid]
            params["target"] = target
            params["model_meta"] = compilation.model_meta
            params["sample_meta"] = compilation.sample_meta
            params["converter_params"] = converter_params
            model_path = compilation.model_path
            sample_path = compilation.sample_path
            params_path = get_tmp_path()
            open(params_path, 'w').write(json.dumps(params))
            report = self._compile(f'model_{idx}', model_path, sample_path,
                                   params_path, output_path)
            res[f'model_{idx}'] = report
            report.dump_json(
                os.path.join(output_path, f'model_{idx}', "report.json"))

            os.remove(params_path)

            logger.debug(params)

        self.output_path = output_path

        return res

    def save(self, output: Path) -> Deployment:
        shutil.rmtree(output, ignore_errors=True)
        shutil.copytree(self.output_path, output)
        return Deployment(output)

    @property
    def supported_devices(self) -> List[str]:
        return [
            'CMSIS-NN',
            'ANDES-LIBNN',
            'NVDLA-NV-SMALL',
            'NVDLA-NV-LARGE',
            'NVDLA-NV-FULL',
            'CMSIS-NN-DEFAULT',
            'NVDLA-NV-SMALL-DEFAULT',
            'NVDLA-NV-LARGE-DEFAULT',
            'NVDLA-NV-FULL-DEFAULT',
            'NVIDIA-TENSORRT-FP32',
            'NVIDIA-TENSORRT-FP16',
            'NVIDIA-TENSORRT-INT8',
            'RELAYIR',
            "INTEL-OPENVINO-CPU-FP32",
            "ONNC-IN2O3",
            "GenericONNC",
            "PTH",
            "TORCH_SCRIPT",
            "SAVED_MODEL",
            "ONNX",
            "FIXED_ONNX",
            "PB",
            "TFLITE",
            "H5",
            "OPENVINO",
            "CAFFE_DIR",
        ]