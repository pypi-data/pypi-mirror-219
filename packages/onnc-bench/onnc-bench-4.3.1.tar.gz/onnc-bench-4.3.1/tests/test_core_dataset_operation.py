
import pytest
from pathlib import Path

import numpy as np

from onnc.bench.core.dataset.dataset import ONNCDataset
from onnc.bench.core.dataset.operation import (ONNCDatasetOperation,
                                               ONNCImageDatasetOperation)
from onnc.bench.core.dataset.transformer import (ONNCDatasetToNumpy,
                                                 DatasetTransformer)


IMAGES_BASE = 'resources/imgs/dogs'
IMAGES = [
    'resources/imgs/dogs/1.jpeg',
    'resources/imgs/dogs/2.jpeg',
    'resources/imgs/dogs/3.jpeg'
]


def test_onnc_dataset_append_path():
    dataset = ONNCDataset()
    operation = ONNCDatasetOperation(dataset)
    for i in IMAGES:
        operation.append(i)
    print([x for x in operation])
    assert len(operation) == len(IMAGES)

    operation.append_dir(Path('resources/imgs/dogs'))
    print([x for x in operation])
    assert len(operation) == len(IMAGES) * 2


def test_onnc_dataset_load():
    dataset = ONNCDataset()
    operation = ONNCImageDatasetOperation(dataset)
    operation.append_dir(Path('resources/imgs/dogs'))
    assert len(operation) == len(IMAGES)
    operation.load()
    for i in operation:
        assert isinstance(i, np.ndarray)


def test_ONNCDatasetToNumpy():
    dataset = ONNCDataset()
    operation = ONNCImageDatasetOperation(dataset)
    operation.append_dir(Path('resources/imgs/dogs'))
    operation.load()
    dataset.shape = (3, 3, 224, 224)

    t = ONNCDatasetToNumpy()
    dataset = t.transform(dataset)

    assert isinstance(dataset.src, np.ndarray)
    assert dataset.shape == (3, 3, 224, 224)


def test_transformer_set_transform():
    def dummy_transform_func(dataset):
        return dataset

    dataset = ONNCDataset()
    operation = ONNCImageDatasetOperation(dataset)
    operation.append_dir(Path('resources/imgs/dogs'))
    operation.load()
    dataset.shape = (3, 3, 224, 224)

    t = DatasetTransformer()
    t.set_transform(dummy_transform_func, ['__DATASET__'])
    dataset = t.transform(dataset)

    assert isinstance(dataset, ONNCDataset)
    assert dataset.shape == (3, 3, 224, 224)
    assert b'transformer' in t.dump()


if __name__ == '__main__':
    test_transformer_set_transform()
