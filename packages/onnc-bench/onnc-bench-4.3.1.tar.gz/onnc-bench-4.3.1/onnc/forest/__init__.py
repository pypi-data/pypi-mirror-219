from .core.options import Options

# Options initialize is required for OptionsRegistry to work properly
from onnc.forest.runtimes.openvino.runtime import OpenvinoOptions
from onnc.forest.runtimes.onnx.runtime import ONNXOptions
from onnc.forest.runtimes.tensorrt.runtime import TensorRTOptions
