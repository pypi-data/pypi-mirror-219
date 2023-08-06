import sys
import pycuda.driver as cuda
import pycuda.autoinit
import time
import tensorrt as trt


class HostDeviceMem(object):
    def __init__(self, host_mem, device_mem):
        self.host = host_mem
        self.device = device_mem

    def __str__(self):
        return "Host:\n" + str(self.host) + "\nDevice:\n" + str(self.device)

    def __repr__(self):
        return self.__str__()


def allocate_buffers(engine):
    """Allocates host and device buffer for TRT engine inference.
    This function is similair to the one in common.py, but
    converts network outputs (which are np.float32) appropriately
    before writing them to Python buffer. This is needed, since
    TensorRT plugins doesn't support output type description, and
    in our particular case, we use NMS plugin as network output.
    Args:
        engine (trt.ICudaEngine): TensorRT engine
    Returns:
        inputs [HostDeviceMem]: engine input memory
        outputs [HostDeviceMem]: engine output memory
        bindings [int]: buffer to device bindings
        stream (cuda.Stream): cuda stream for engine inference synchronization
    """
    inputs = []
    outputs = []
    bindings = []
    stream = cuda.Stream()

    for binding in engine:
        size = trt.volume(engine.get_binding_shape(binding)) * engine.max_batch_size
        dtype = trt.nptype(engine.get_binding_dtype(binding))
        # Allocate host and device buffers
        """
         pagelocked means memory won't be swap with the secondary memory
         such as harddrive, but here we only use pagelocked_empty to
         calculate the size to allocate
        """
        host_mem = cuda.pagelocked_empty(size, dtype)
        device_mem = cuda.mem_alloc(host_mem.nbytes)
        # Append the device buffer to device bindings.
        bindings.append(int(device_mem))
        # Append to the appropriate list.
        if engine.binding_is_input(binding):
            inputs.append(HostDeviceMem(host_mem, device_mem))
        else:
            outputs.append(HostDeviceMem(host_mem, device_mem))
    return inputs, outputs, bindings, stream

# This function is generalized for multiple inputs/outputs.
# inputs and outputs are expected to be lists of HostDeviceMem objects.
def do_inference(context, bindings, inputs, outputs, stream,use_sync=False):
    # Transfer input data to the GPU.
    [cuda.memcpy_htod_async(inp.device, inp.host, stream) for inp in inputs]

    # Run inference.
    if use_sync:
        context.execute_v2(
                bindings=bindings)
    else:
        context.execute_async_v2(
            bindings=bindings,
            stream_handle=stream.handle)

    # Transfer predictions back from the GPU.
    [cuda.memcpy_dtoh_async(out.host, out.device, stream) for out in outputs]
    # Blocks until stream has completed all operations
    stream.synchronize()
    # Return only the host outputs.
    return [out.host for out in outputs]
