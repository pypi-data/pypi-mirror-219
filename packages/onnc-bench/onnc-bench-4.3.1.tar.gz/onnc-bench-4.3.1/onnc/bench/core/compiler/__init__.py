from pathlib import Path
from typing import Any, List, Union, Dict
from onnc.bench.core.model.model import Model
from onnc.bench.core.dataset.dataset import Dataset
from onnc.bench.core.dataset.layout import DataLayout


class Compilation:

    @classmethod
    def get_model_meta(cls, model: Model, inputs_as_nchw):
        return {
            "batch_dim": model.batch_dim,
            "inputs": [x.dump() for x in model.inputs],
            "inputs_as_nchw": inputs_as_nchw,
            "outputs": [x.dump() for x in model.outputs],
            "format": model.format.name
        }

    @classmethod
    def get_dataset_meta(cls, dataset: Dataset):

        dataset_meta = {"shape": dataset.shape, "format": dataset.format.name}

        if isinstance(dataset.layout, DataLayout):
            dataset_meta["layout"] = dataset.layout.dump()

        return dataset_meta

    def __init__(self,
                 model: Model,
                 dataset: Dataset,
                 inputs_as_nchw: Union[str, bool, None, List[str]] = None):
        if not (isinstance(model.src, str) or isinstance(model.src, Path)):
            raise TypeError("model.src should be str or path, "
                            f"not {type(model.src)}")
        if not (isinstance(dataset.src, str) or isinstance(dataset.src, Path)):
            raise TypeError("dataset.src should be str or path, "
                            f"not {type(dataset.src)}")
        self.compilation_id: str  # SaaS compilation_id
        self.model_path = model.src
        self.sample_path = dataset.src
        self.model_meta = self.get_model_meta(model, inputs_as_nchw)
        self.sample_meta = self.get_dataset_meta(dataset)


from .onnc_saas import ONNCSaaSBuilder
from .nnuxe import NNUXEBuilder
from .nnuxe_docker import NNUXEDockerBuilder
