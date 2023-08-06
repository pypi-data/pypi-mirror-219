from dataclasses import dataclass
from pydlmeta.identifier.types import ModelDataType
from pydlmeta.utils import Singleton

@dataclass
class Base_map(metaclass=Singleton):
    _map = {}
    _inv_map = {}
    _inv_name_map = {}

    @classmethod
    def map(cls, key):
        return cls._map[key]

    @classmethod
    def inv_map(cls, key):
        return cls._inv_map[key]

    @classmethod
    def inv_name_map(cls, key):
        return cls._inv_name_map[key]

    @classmethod
    def str_map(cls, key):
        return cls._str_map[key]


@dataclass
class TORCH_map(Base_map):

    import torch
    _map = {
        torch.float: ModelDataType.FP32,
        torch.float16: ModelDataType.FP16,
        torch.float32: ModelDataType.FP32,
        torch.float64: ModelDataType.FP64,
        torch.uint8: ModelDataType.UINT8,
        torch.int8: ModelDataType.INT8,
        torch.int16: ModelDataType.INT16,
        torch.int32: ModelDataType.INT32,
        torch.int64: ModelDataType.INT64,
        torch.bool: ModelDataType.BOOL,
        torch.complex128: ModelDataType.COMPLEX128,
        torch.bfloat16: ModelDataType.BFLOAT16
    }
    _str_map = {str(k): v.name for k, v in _map.items()}
    _inv_map = {v: k for k, v in _map.items()}
    _inv_name_map = {v.name: k for k, v in _map.items()}


@dataclass
class TF_map(Base_map):

    import tensorflow as tf
    _map = {
        tf.float32: ModelDataType.FP32,
        tf.uint8: ModelDataType.UINT8,
        tf.int8: ModelDataType.INT8,
        tf.uint16: ModelDataType.UINT16,
        tf.int16: ModelDataType.INT16,
        tf.int32: ModelDataType.INT32,
        tf.int64: ModelDataType.INT64,
        tf.string: ModelDataType.STR,
        tf.bool: ModelDataType.BOOL,
        tf.float16: ModelDataType.FP16,
        tf.float64: ModelDataType.FP64,
        tf.uint32: ModelDataType.UINT32,
        tf.uint64: ModelDataType.UINT64,
        tf.complex128: ModelDataType.COMPLEX128,
        tf.bfloat16: ModelDataType.BFLOAT16
    }
    _str_map = {str(k): v.name for k, v in _map.items()}
    _inv_map = {v: k for k, v in _map.items()}
    _inv_name_map = {v.name: k for k, v in _map.items()}


@dataclass
class ONNX_map(Base_map):
    _map = {
        1: ModelDataType.FP32,
        2: ModelDataType.UINT8,
        3: ModelDataType.INT8,
        4: ModelDataType.UINT16,
        5: ModelDataType.INT16,
        6: ModelDataType.INT32,
        7: ModelDataType.INT64,
        8: ModelDataType.STR,
        9: ModelDataType.BOOL,
        10: ModelDataType.FP16,
        11: ModelDataType.FP64,
        12: ModelDataType.UINT32,
        14: ModelDataType.UINT64,
        15: ModelDataType.COMPLEX128,
        16: ModelDataType.BFLOAT16
    }
    _str_map = {str(k): v.name for k, v in _map.items()}
    _inv_map = {v: k for k, v in _map.items()}
    _inv_name_map = {v.name: k for k, v in _map.items()}


@dataclass
class NP_map(Base_map):
    import numpy as np
    _map = {
        np.float32: ModelDataType.FP32,
        np.uint8: ModelDataType.UINT8,
        np.int8: ModelDataType.INT8,
        np.uint16: ModelDataType.UINT16,
        np.int16: ModelDataType.INT16,
        np.int32: ModelDataType.INT32,
        np.int64: ModelDataType.INT64,
        str: ModelDataType.STR,
        bool: ModelDataType.BOOL,
        np.float16: ModelDataType.FP16,
        np.float64: ModelDataType.FP64,
        np.uint32: ModelDataType.UINT32,
        np.uint64: ModelDataType.UINT64,
        np.complex128: ModelDataType.COMPLEX128
    }
    _str_map = {str(k): v.name for k, v in _map.items()}
    _inv_map = {v: k for k, v in _map.items()}
    _inv_name_map = {v.name: k for k, v in _map.items()}


@dataclass
class OV_map(Base_map):
    """
    from openvino.runtime import Core
    ie = Core()
    classification_model_xml = "model.xml"
    model = ie.read_model(model=classification_model_xml)
    model.inputs[0].element_type.get_type_name()
    """
    _map = {
        'u8': ModelDataType.UINT8,
        'u16': ModelDataType.UINT16,
        'u32': ModelDataType.UINT32,
        'u64': ModelDataType.UINT64,
        'i8': ModelDataType.INT8,
        'i16': ModelDataType.INT16,
        'i32': ModelDataType.INT32,
        'i64': ModelDataType.INT64,
        'boolean': ModelDataType.BOOL,
        'f16': ModelDataType.FP16,
        'f32': ModelDataType.FP32,
        'f64': ModelDataType.FP64
    }
    _str_map = {str(k): v.name for k, v in _map.items()}
    _inv_map = {v: k for k, v in _map.items()}
    _inv_name_map = {v.name: k for k, v in _map.items()}


if __name__ == '__main__':

    np_map = NP_map
    import numpy as np
    print(np_map.map(np.float32))
