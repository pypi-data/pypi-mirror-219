import numpy as np
import time

from onnc.bench import login, Project
from onnc.forest.core.runtime import Runtime
from onnc.forest import Options
from onnc.forest.proxies.profiler.runtime import ProfilerOptions, ProfilerProxy
from onnc.forest.proxies.batcher.runtime import BatcherOptions, BatcherProxy
from onnc.forest.proxies.zerorpc.runtime import ZeroRPCOptions, ZeroRPCProxy

from onnc.forest.utils.load_img import load_and_preprocess_img
from fixtures import RESNET18_OPENVINO_LOADABLE


def test_runtime_ov():
    runtime = Runtime()
    options = Options(loadable=RESNET18_OPENVINO_LOADABLE)
    runtime.launch(options)
    runtime.load(options)  # use loadable to select correct runtime
    runtime.bind_input(None, None)
    runtime.bind_output(None, None)
    runtime.materialize()
    img = np.random.randn(1, 3, 224, 224)

    runtime.write([img])
    runtime.run()
    res = runtime.read()

    assert isinstance(res[0], np.ndarray)
    

def test_runtime_call_ov():
    img = np.random.randn(1, 3, 224, 224)

    options = Options(loadable=RESNET18_OPENVINO_LOADABLE)
    runtime = Runtime(options)
    res = runtime([img])

    assert isinstance(res[0], np.ndarray)

def test_profiler():
    ov_options = Options(loadable=RESNET18_OPENVINO_LOADABLE)
    
    pf_options = ProfilerOptions(loadable=None)
    pf_options.settings.iter = 100
    pf_options.settings.warm_up = 100
    
    pf_options.encapsulate(ov_options)

    runtime = ProfilerProxy(pf_options)

    runtime.launch(pf_options)
    runtime.load(pf_options)  
    runtime.bind_input(None, None)
    runtime.bind_output(None, None)
    runtime.materialize()
    img = np.random.randn(1, 3, 224, 224)

    r1 = runtime.write([img])
    r2 = runtime.run()
    r3 = res = runtime.read()
    print(r1["wall_time"])
    print(r2["wall_time"])
    print(r3["wall_time"])


def test_batcher():
    ov_options = Options(loadable=RESNET18_OPENVINO_LOADABLE)
    
    bt_options = BatcherOptions(loadable=None)
    bt_options.settings.interval = 0.5
    
    bt_options.encapsulate(ov_options)

    runtime = BatcherProxy(bt_options)

    runtime.launch(bt_options)
    runtime.load(bt_options)  
    runtime.bind_input(None, None)
    runtime.bind_output(None, None)
    runtime.materialize()
    img = np.random.randn(1, 3, 224, 224)

    runtime.write([img])
    
    runtime.run()
    time.sleep(2)
    res = runtime.read()
    print(res)

    runtime.stop()


def __test_zerorpc():
    ov_options = Options(loadable=RESNET18_OPENVINO_LOADABLE)

    rpc_options = ZeroRPCOptions(loadable=None)
    rpc_options.settings.protocol = 'tcp'
    rpc_options.settings.host = '127.0.0.1'
    rpc_options.settings.port = 20000

    pf_options = ProfilerOptions(loadable=None)
    pf_options.settings.iter = 100
    pf_options.settings.warm_up = 100
    
    pf_options.encapsulate(rpc_options)
    rpc_options.encapsulate(ov_options)

    # breakpoint()
    runtime = ProfilerProxy(pf_options)

    runtime.launch(rpc_options)
    runtime.load(rpc_options)  
    runtime.bind_input(None, None)
    runtime.bind_output(None, None)
    runtime.materialize()
    img = np.random.randn(1, 3, 224, 224)

    runtime.write([img])
    
    runtime.run()
    res = runtime.read()
    print(res)

if __name__ == '__main__':
    test_runtime_ov()
    test_runtime_call_ov()
    test_profiler()
    test_batcher()
    # test_zerorpc()
