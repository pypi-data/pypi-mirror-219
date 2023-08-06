from typing import Any, List, Union, Dict
from abc import abstractmethod
from pathlib import Path

from loguru import logger

from onnc.bench.core.deployment import Deployment
from onnc.bench.core.model.model import Model
from onnc.bench.core.dataset.dataset import Dataset
from onnc.bench.core.compiler import Compilation


class IBuilder:

    BUILDER_NAME = ""

    def __init__(self):
        self.model_ids: List = []

    def prepare_model(
            self,
            model: Model,
            dataset: Dataset,
            inputs_as_nchw: Union[str, bool, None, List[str]] = None) -> int:
        """ Upload a model and its corresponding calibration dataset.
            And create a compilation.

        :param str model:
            A path to a model file
        :param str dataset:
            A path to a model file
        :rtype:
            int
        """

        compilation = Compilation(model, dataset, inputs_as_nchw)
        _internal_cid = id(model.src)
        self._compilations[_internal_cid] = compilation
        return _internal_cid

    @abstractmethod
    def build(self, target, converter_params: Dict = {}) -> Any:
        """build a project witch contains multiple models

        for model in model_ids:
            ...
        """
        pass

    @abstractmethod
    def save(self, output: Path) -> Union[Dict, Deployment]:
        pass

    @property
    def supported_devices(self) -> List[str]:
        pass

    def get_device_id(self, target):
        if target in self.supported_devices:
            return target
        else:
            logger.error(f'`{target}` is not a supported device/format.')
            logger.error(f'Supported devices/formats are: '
                         f'{str([x for x in self.supported_devices])} ')
            raise Exception(f'`{target}` is not supported')
