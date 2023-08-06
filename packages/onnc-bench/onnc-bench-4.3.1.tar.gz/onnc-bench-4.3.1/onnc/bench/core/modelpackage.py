from typing import Dict, List, Union, Type, Iterable, Any, Tuple, Optional
from pathlib import Path

from loguru import logger

from .common import get_tmp_path

from .evaluator import Evaluator
from .evaluator import Metric

from .dataset.dataset import Dataset
from .dataset.transformer import DatasetTransformer
from .dataset import serializer as dataset_serializer

from .model import serializer as model_serializer

from .model.model import Model, Tensor
from .model.transformer import ModelTransformer

from pydlmeta.identifier.dataset import identify as identify_dataset
from pydlmeta.identifier.model import identify as identify_model
from pydlmeta.identifier.types import ModelFormat, DatasetFormat, ModelDataType, PYTORCH_MODEL_FORMATS


class ModelPackage:
    """Contain all data and controllers

    Data include: model and dataset
    Controllers include: evaluators, model_transformer and dataset_transformer

    model: Model CANNOT be type MODEL otherwise we won't know the priority
           of model.format and model_format
    dataset: same concept as model
    """

    def __init__(
            self,
            model: Union[str, Path],
            dataset: Union[str, Path] = None,
            model_format: ModelFormat = ModelFormat.NON_SPECIFIED,
            sample_format: DatasetFormat = DatasetFormat.NON_SPECIFIED,
            #  [name: str, shape:Tuple, dtype:ModelDataType]
            model_inputs: List[Union[List, Tuple, Tensor]] = None,
            #  [name: str, shape:Tuple, dtype:ModelDataType]
            model_outputs: List[Union[List, Tuple, Tensor]] = None,
            batch_dim: Optional[int] = 0):

        model_inputs = model_inputs if model_inputs else []
        model_outputs = model_outputs if model_outputs else []

        self.evaluators: List[Evaluator] = []
        self.model_transformers: List[ModelTransformer] = []
        self.dataset_transformers: List[DatasetTransformer] = []
        self.model = self.__encapsulate_model(model, model_format, model_inputs,
                                              model_outputs, batch_dim)
        self.dataset = self.__encapsulate_dataset(dataset, format=sample_format)

    def __encapsulate_model(self, model: Union[str, Path], model_format,
                            model_inputs, model_outputs, batch_dim) -> Model:
        """
        Do not put these code in Model.__init__(). Make sure
        (MVC) control and model are separated.
        """

        from pydlmeta.meta import retrieve_model_metadata

        def inputs_outputs_to_tensors(data: List[Union[List, Tuple, Tensor]]):
            res = []
            for i in data:
                if isinstance(i, list) or isinstance(i, tuple):
                    assert len(i) > 0
                    name = i[0]
                    shape = i[1] if len(i) >= 2 else tuple()
                    dtype = i[2] if len(i) >= 3 else ModelDataType.NON_SPECIFIED
                    if not dtype:
                        dtype = ModelDataType.NON_SPECIFIED
                    tensor = Tensor(name, shape, dtype)
                elif isinstance(i, Tensor):
                    tensor = i
                res.append(tensor)
            return res

        res_model = Model(model, batch_dim=batch_dim)
        if model_format == ModelFormat.NON_SPECIFIED:
            res_model.format = identify_model(res_model.src)
        else:
            res_model.format = model_format

        meta = retrieve_model_metadata(res_model.src)
        meta_input_names = set([x.name for x in meta.inputs])
        meta_output_names = set([x.name for x in meta.outputs])
        if len(model_inputs) == 0:
            if res_model.format in PYTORCH_MODEL_FORMATS:
                logger.error("Please specify model_inputs in "
                             "Project.add(model, model_inputs="
                             "[[input_name, shape, type]])."
                             "For example, Project.add(model, "
                             "model_inputs=[['input_1', [1, 3, 224, 224], "
                             "float]])")
                raise Exception(
                    "Parameter `model_inputs` is required for Pytorch formats")
            res_model.reset_inputs(meta.inputs)
        else:
            tensors = inputs_outputs_to_tensors(model_inputs)
            for tensor in tensors:
                if tensor.name not in meta_input_names:
                    logger.warning(f"It seems input tenosr({tensor.name}) "
                                   f"does not match with model input schema "
                                   f"({meta_input_names}).")
            res_model.reset_inputs(tensors)

        if len(model_outputs) == 0:
            res_model.reset_outputs(meta.outputs)
        else:
            tensors = inputs_outputs_to_tensors(model_outputs)
            for tensor in tensors:
                if tensor.name not in meta_output_names:
                    logger.warning(f"It seems output tenosr({tensor.name}) "
                                   f"does not match with model output schema "
                                   f"({meta_output_names}).")
            res_model.reset_outputs(tensors)
        return res_model

    def __encapsulate_dataset(self, dataset: Union[str, Path],
                              format: DatasetFormat) -> Dataset:
        dataset = Dataset(dataset, format)
        if format == DatasetFormat.NON_SPECIFIED:
            dataset.format = identify_dataset(dataset.src)
        return dataset

    def serialize(
            self,
            model_path: Union[str, Path, None] = None,
            dataset_path: Union[str, Path,
                                None] = None) -> Tuple[Model, Dataset]:
        if model_path is None:
            model_path = get_tmp_path()
        if dataset_path is None:
            dataset_path = get_tmp_path()
        model = model_serializer.serialize(self.model, Path(model_path))
        dataset = dataset_serializer.serialize(self.dataset, Path(dataset_path))

        # need to get the meta again after serialization
        return (self.__encapsulate_model(model.src, ModelFormat.NON_SPECIFIED,
                                         self.model.inputs, self.model.outputs,
                                         self.model.batch_dim),
                self.__encapsulate_dataset(dataset.src,
                                           DatasetFormat.NON_SPECIFIED))

    def evaluate(self, model, dataset) -> List[Metric]:
        return [e.evaluate(model, dataset) for e in self.evaluators]

    def add_model_transformer(self, model_transformer: ModelTransformer):
        self.model_transformers.append(model_transformer)

    def add_dataset_transformer(self, ds_transformer: DatasetTransformer):
        self.dataset_transformers.append(ds_transformer)

    def add_evaluator(self, evaluator: Evaluator):
        self.evaluators.append(evaluator)

    def dump(self) -> Dict:
        data = {
            "model":
                self.model.dump(),
            "dataset":
                self.dataset.dump(),
            "evaluators": [x.dump() for x in self.evaluators],
            "model_transformers": [x.dump() for x in self.model_transformers],
            "dataset_transformers": [
                x.dump() for x in self.dataset_transformers
            ]
        }
        return data

    def load(self, data: Dict):
        pass
