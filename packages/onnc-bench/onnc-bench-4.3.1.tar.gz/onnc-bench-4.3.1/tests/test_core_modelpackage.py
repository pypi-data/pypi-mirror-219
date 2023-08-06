import pytest
import json
import os
from pathlib import Path

from onnc.bench.core import modelpackage
from onnc.bench.core.common import get_tmp_path
from fixtures import (vww_model_files, vww_dataset_files, img_net_model_objects,
                      img_net_dataset_objects)

# model_objs = [img_net_model_objects[x] for x in img_net_model_objects]
# dataset_objs = [img_net_dataset_objects[x] for x in img_net_dataset_objects]


# @pytest.mark.parametrize("model_object", model_objs)
# @pytest.mark.parametrize("dataset_object", dataset_objs)
# def test_img_net_object(model_object, dataset_object):

#     if "inputs" in model_object:
#         mp = modelpackage.ModelPackage(model_object["model"],
#                                        dataset_object["dataset"],
#                                        model_inputs=model_object["inputs"])
#     else:
#         mp = modelpackage.ModelPackage(model_object["model"],
#                                        dataset_object["dataset"])

#     model_path = Path(get_tmp_path())
#     dataset_path = Path(get_tmp_path())

#     mp.serialize(model_path, dataset_path)

#     assert model_path.stat().st_size > 0
#     assert dataset_path.stat().st_size > 0

#     os.remove(model_path)
#     os.remove(dataset_path)

#     data = mp.dump()
#     assert isinstance(data, dict)
#     jstring = json.dumps(data)


# assert isinstance(jstring, str)

model_files = [vww_model_files[x] for x in vww_model_files]
dataset_files = [vww_dataset_files[x] for x in vww_dataset_files]


@pytest.mark.parametrize("model_file", model_files)
@pytest.mark.parametrize("dataset_file", dataset_files)
def test_vww(model_file, dataset_file):
    mp = modelpackage.ModelPackage(model_file["model"], dataset_file["dataset"])
    data = mp.dump()
    assert isinstance(data, dict)
    assert data['model']['format'] == mp.model.format.name
    assert ('input_1'
            in data['model']['inputs']) or ('import/input_1'
                                            in data['model']['inputs'])
    if 'input_1' in data['model']['inputs']:
        input_name = 'input_1'
    elif 'import/input_1' in data['model']['inputs']:
        input_name = 'import/input_1'
    assert data['model']['inputs'][input_name]['shape'] == (-1, 96, 96, 3)
    # assert data['model']['inputs'][input_name]['type'] == 'float32'
    # assert 'dense/Softmax:0' in data['model']['outputs']
    # assert data['model']['outputs']['dense/Softmax:0']['shape'] == (None, 2)
    # assert data['model']['outputs']['dense/Softmax:0']['type'] == 'float32'

    assert data['dataset']['format'] == mp.dataset.format.name
    jstring = json.dumps(data)
    assert isinstance(jstring, str)


# mp = modelpackage.ModelPackage(model_files[1]["model"],
#                                dataset_files[0]["dataset"])
# data = mp.dump()
# print(data)
"""
{'model':{
    'src': 'resources/vww/models/model.h5',
    'name': 'model',
    'inputs': {
        'input_1': {'shape': (None, 96, 96, 3), 'type': 'float32'}},
    'outputs': {
        'dense/Softmax:0': {'shape': (None, 2), 'type': 'float32'}},
    'format': 'NON_SPECIFIED'},
'dataset': {
    'src': 'resources/vww/samples/coco_11x96x96x3.pb',
    'y_label': OrderedDict(),
    'shape': None,
    'layout': None,
    'format': 'PB'},
    'evaluators': [],
    'model_transformers': [],
    'dataset_transformers': []
    }
}
"""
