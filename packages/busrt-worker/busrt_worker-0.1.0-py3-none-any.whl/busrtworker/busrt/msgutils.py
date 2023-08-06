import msgpack
import zstd


def deserialize(data):
    if data is None:
        return None
    return msgpack.unpackb(zstd.decompress(data))


def serialize(data):
    if data is None:
        data={}
    return zstd.compress(msgpack.dumps(data))
