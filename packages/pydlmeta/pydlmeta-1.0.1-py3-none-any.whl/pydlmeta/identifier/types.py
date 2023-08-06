from pathlib import Path
from enum import Enum, auto


class SrcType(Enum):
    OBJ = auto()
    FILE = auto()
    DIR = auto()


def get_src_type(path) -> SrcType:
    """
        Return type of path
        Return None if path is not a valid path
    """

    if isinstance(path, str):
        path = Path(path)
    elif isinstance(path, Path):
        path = path
    else:
        return SrcType.OBJ

    if path.is_dir():
        return SrcType.DIR
    elif path.is_file():
        return SrcType.FILE
    else:
        return None


class ModelFormat(Enum):
    NON_SPECIFIED = auto()

    PT_NN_MODULE = auto()
    TF_KERAS_MODEL = auto()
    KERAS_MODEL = auto()
    TF_SESSION = auto()

    H5 = auto()
    SAVED_MODEL = auto()
    PB = auto()
    ZIPPED_SAVED_MODEL = auto()
    TFLITE = auto()

    PTH = auto()
    ONNX = auto()
    TORCH_TRACED = auto()

    CKPT = auto()

    TRT_PLAN = auto()
    OPENVINO_IRDIR = auto()
    ZIPPED_OPENVINO_IRDIR = auto()

    CAFFE_DIR = auto()
    ZIPPED_CAFFE_DIR = auto()
    GRAPHDEF = auto()

    RELAYIR = auto()

    MLIR = auto()


TF_MODEL_FORMATS = [
    ModelFormat.TF_KERAS_MODEL, ModelFormat.KERAS_MODEL, ModelFormat.H5,
    ModelFormat.SAVED_MODEL, ModelFormat.PB, ModelFormat.TFLITE,
    ModelFormat.CKPT
]

PYTORCH_MODEL_FORMATS = [
    ModelFormat.PT_NN_MODULE, ModelFormat.PTH, ModelFormat.TORCH_TRACED
]


class ModelDataType(Enum):
    NON_SPECIFIED = 0
    FP32 = 1
    UINT8 = 2
    INT8 = 3
    UINT16 = 4
    INT16 = 5
    INT32 = 6
    INT64 = 7
    STR = 8
    BOOL = 9
    FP16 = 10
    FP64 = 11
    UINT32 = 12
    UINT64 = 14
    COMPLEX128 = 15
    BFLOAT16 = 16


class DatasetFormat(Enum):
    NON_SPECIFIED = 0
    UNKNOWN = 1
    NONE = 2

    NPY = 11
    NPYDIR = 12
    NPZ = 13
    NDARRAY = 14
    NP_MEMMAP = 15
    NPZ_OBJECT = 16

    PB = 17

    ONNC_DATASET = 51

    TORCH_DATASET = 100
    TORCH_DATALOADER = 101

    KERAS_DATASET = 200
    TFDS_PREFETCH = 201 # tensorflow.python.data.ops.dataset_ops.PrefetchDataset
