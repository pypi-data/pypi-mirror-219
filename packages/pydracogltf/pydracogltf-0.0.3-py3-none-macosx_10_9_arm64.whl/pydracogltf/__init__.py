__version__ = "0.0.3"

from .gltf_draco_encoder import encode_primitive_draco
from .gltf_draco_decoder import decode_primitive_draco

__all__ = [
    "__version__",
    "encode_primitive_draco",
    "decode_primitive_draco",
]
