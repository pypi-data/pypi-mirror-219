from onnc.bench.core.compiler import Compilation
from onnc.bench.core.model.model import Model
from onnc.bench.core.dataset.dataset import Dataset


def test_compilation():
    model_path = ""
    dataset_path = ""
    model_meta = {}
    dataset_m = {}
    m = Model("/tmp/dummy")
    d = Dataset("/test/dummy")
    compilation = Compilation(m, d)
    compilation.model_path = model_path
    compilation.sample_path = dataset_path
    compilation.model_meta = model_meta
    compilation.sample_meta = dataset_m

    assert isinstance(compilation.model_path, str)
    assert isinstance(compilation.sample_path, str)
    assert isinstance(compilation.model_meta, dict)
    assert isinstance(compilation.sample_meta, dict)
