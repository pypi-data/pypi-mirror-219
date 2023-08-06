from functools import singledispatch
from onnc.forest.runtimes.tensorrt.runtime import TensorRTRuntime
from onnc.forest.runtimes.openvino.runtime import OpenvinoRuntime


def auto_bind(runtime):
    for rt in runtime.loaded_runtimes:
        try:
            _auto_bind(rt)
        except:
            pass


@singledispatch
def _auto_bind(runtime):
    raise NotImplementedError(f"Runtime {runtime} not support auto_bind")


@_auto_bind.register
def _(runtime: TensorRTRuntime):
    from onnc.forest.runtimes.tensorrt.utils import allocate_buffers
    runtime._inputs, runtime._outputs, runtime._bindings, _ = \
        allocate_buffers(runtime._cuda_engine)

@_auto_bind.register
def _(runtime: OpenvinoRuntime):
    runtime.bind_input(None,None)