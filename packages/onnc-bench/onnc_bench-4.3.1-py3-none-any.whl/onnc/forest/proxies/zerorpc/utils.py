import msgpack
import msgpack_numpy as m
import numpy as np

def np_to_bytes(payload: np.array)->bytes:
    """
    to_bytes takes a numpy.array as a single argument and serializes it to bytes.
    """
    return msgpack.packb(payload, default=m.encode)


def np_from_bytes(payload:bytes) -> np.array:
    """
    from_bytes recovers a numpy.array from a bytes array that was produced via numpy_serializer.to_bytes.
    """ 
    return msgpack.unpackb(payload, object_hook=m.decode)