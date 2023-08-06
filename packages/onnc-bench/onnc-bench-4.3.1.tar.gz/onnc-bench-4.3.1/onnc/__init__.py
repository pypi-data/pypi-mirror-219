import os
import pkg_resources
from packaging import version
from loguru import logger

protobuf_ver = pkg_resources.get_distribution("protobuf").version
if version.parse(protobuf_ver) > version.parse('3.20.3'):
    if not os.environ.get('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'):
        os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = "python"
        logger.warning(
            "Set environment variable: "
            "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python. Reason: protobuf "
            f"version {protobuf_ver} is found in your system, however, onnx "
            "only supports protobuf package == 3.20.x or lower. The "
            "environment variable makes onnx use pure-Python to parse protobuf "
            "format and will be much slower. Alternatively, you can downgrade "
            "the protobuf package to 3.20.x or lower.)")
