import pytest
from pathlib import Path
import shutil
import os

import torchvision.models as models  # type: ignore[import]

# type: ignore[import]
from tensorflow.keras.applications.resnet50 import ResNet50

from onnc.bench.core.model import serializer
from onnc.bench.core.model.model import Model, Tensor
from pydlmeta.identifier.model import identify
from pydlmeta.identifier.types import ModelFormat, ModelDataType

model_files = {
    "H5": {
        "model": Path("resources/vww/models/model.h5"),
        "format": ModelFormat.H5,
        "serialized_format": ModelFormat.H5,
    },
    "H5_NO_EXT": {
        "model": Path("resources/h5_model"),
        "format": ModelFormat.H5,
        "serialized_format": ModelFormat.H5,
    },
    "PB": {
        "model": Path("resources/vww/models/frozen_graph.pb"),
        "format": ModelFormat.PB,
        "serialized_format": ModelFormat.PB,
    },
    "SAVED_MODEL": {
        "model": Path("resources/vww/models/savedmodel"),
        "format": ModelFormat.SAVED_MODEL,
        "serialized_format": ModelFormat.ZIPPED_SAVED_MODEL,
    },
    "ONNX": {
        "model": Path("resources/model.onnx"),
        "format": ModelFormat.ONNX,
        "serialized_format": ModelFormat.ONNX,
    },
    "ONNX_NO_EXT": {
        "model": Path("resources/onnx_model"),
        "format": ModelFormat.ONNX,
        "serialized_format": ModelFormat.ONNX,
    },
}

model_objects = {
    "PytorchModel": {
        "model": models.resnet18(pretrained=True),
        "format": ModelFormat.PT_NN_MODULE,
        "serialized_format": ModelFormat.TORCH_TRACED
    },
    "TFKerasModel": {
        "model": ResNet50(),
        "format": ModelFormat.KERAS_MODEL,
        "serialized_format": ModelFormat.H5
    },
}


@pytest.mark.parametrize("model_file", [model_files[x] for x in model_files])
def test_model_file_identifiers(model_file):
    model = Model(model_file["model"])
    model_format = model_file["format"]
    assert identify(model.src) == model_format


@pytest.mark.parametrize("model_file", [model_files[x] for x in model_files])
def test_model_file_serializers(model_file):

    model = Model(model_file["model"])
    model_format = model_file["serialized_format"]
    serialized_model = serializer.serialize(model, Path("/tmp/test"))
    assert identify(serialized_model.src) == model_format

    try:
        if os.path.isdir(serialized_model.src):
            shutil.rmtree(serialized_model.src)
        else:
            os.remove(serialized_model.src)
    except:
        pass


model_objs = [model_objects[x] for x in model_objects]


# @pytest.mark.parametrize("model_object", model_objs)
# def test_model_object_identifiers(model_object):
#     model = Model(model_object["model"])
#     model_format = model_object["format"]
#     assert identify(model.src) == model_format


# @pytest.mark.parametrize("model_object", model_objs)
# def test_model_object_serializers(model_object):
#     model = Model(model_object["model"])
#     model.reset_inputs([Tensor('input', (1, 3, 224, 224), float)])
#     serialized_format = model_object["serialized_format"]
#     serialized_model = serializer.serialize(model, Path("/tmp/test"))

#     assert identify(serialized_model.src) == serialized_format

#     try:
#         if os.path.isdir(serialized_model.src):
#             shutil.rmtree(serialized_model.src)
#         else:
#             os.remove(serialized_model.src)
#     except:
#         pass


def test_model_set_name():
    model = Model("/path/to/model")
    model.set_name('test')
    assert model.name == 'test'


def test_model_reset_inputs():
    model = Model("/path/to/model")
    model.reset_inputs([Tensor('t1', (1, 2, 3)), Tensor('t2', (1, 2, 3))])
    assert len(model.inputs) == 2


def test_model_reset_outputs():
    model = Model("/path/to/model")
    model.reset_outputs([Tensor('t1', (1, 2, 3)), Tensor('t2', (1, 2, 3))])
    assert len(model.outputs) == 2


def test_model_dump():
    model = Model("/path/to/model_1")
    model.reset_inputs([Tensor('t1', (1, 2, 3), ModelDataType.FP32)])
    model.reset_outputs([Tensor('t2', (1, 2, 3), ModelDataType.FP32)])
    md = model.dump()
    assert md['src'] == '/path/to/model_1'
    assert md['name'] == 'model_1'
    assert md['inputs'] == {
        't1': {
            'name': 't1',
            'shape': (1, 2, 3),
            'type': 'FP32'
        }
    }
    assert md['outputs'] == {
        't2': {
            'name': 't2',
            'shape': (1, 2, 3),
            'type': 'FP32'
        }
    }
    assert md['format'] == 'NON_SPECIFIED'
