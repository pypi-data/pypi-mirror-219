from __future__ import annotations

import os, glob
import zipfile
import inspect
from pathlib import Path
from typing import List, Union
from pydlmeta.identifier.types import get_src_type, ModelFormat, SrcType



class IdentifierRegistry(type):

    REGISTRY: List = []

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if name != "Identifier":
            cls.REGISTRY.append(new_cls)
        return new_cls


class Identifier(metaclass=IdentifierRegistry):

    FORMAT = ModelFormat.NON_SPECIFIED

    @classmethod
    def is_me(cls, model_path: Union[str, Path]) -> bool:
        pass


def identify(model_path: Union[str, Path]) -> ModelFormat:
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"{model_path} does not exist.")
    for identifier in Identifier.REGISTRY:
        if identifier.is_me(model_path):
            return identifier.FORMAT

    raise NotImplementedError(
        f"Unable to identify {model_path}. "
        f"Supported list: {[x.__name__ for x in Identifier.REGISTRY]}")


class H5(Identifier):
    """
    Use file extension and magic number to identify the file
    """
    FORMAT = ModelFormat.H5

    @classmethod
    def is_me(cls, model_path: Union[str, Path]) -> bool:
        if get_src_type(model_path) != SrcType.FILE:
            return False
        if str(model_path).lower().endswith('.h5'):
            return True
        with open(model_path, 'rb') as f:
            r = f.read(8) == bytes.fromhex('894844460d0a1a0a')
            return r


class ONNX(Identifier):
    """
    Use file extension and magic number to identify the file
    """
    FORMAT = ModelFormat.ONNX

    @classmethod
    def is_me(cls, model_path: Union[str, Path]):
        if get_src_type(model_path) != SrcType.FILE:
            return False
        if str(model_path).lower().endswith('.onnx'):
            return True
        import onnx
        try:
            onnx.checker.check_model(str(model_path))
        except onnx.onnx_cpp2py_export.checker.ValidationError:
            return False
        return True


class PTH(Identifier):
    """
    - PTH archives the model in zip format.
    - Model saved by torch.save.
    - constants.pkl is the main difference between PTH and TorchTraced
        - see https://github.com/pytorch/pytorch/blob/e9ebda29d87ce0916ab08c06ab26fd3766a870e5/torch/serialization.py#L1180
    """
    FORMAT = ModelFormat.PTH

    @classmethod
    def is_me(cls, model_path: Union[str, Path]):

        if get_src_type(model_path) != SrcType.FILE:
            return False

        with open(model_path, 'rb') as f:
            if not f.read(4) == bytes.fromhex('504b0304'):
                return False

        try:
            z = zipfile.ZipFile(model_path)
            file_names = '|'.join(z.namelist())
            return ('code/__torch__' not in file_names) and \
                   'data.pkl' in file_names and \
                   'data/' in file_names and \
                   'constants.pkl' not in file_names
        except OSError:
            return False


class TorchTraced(Identifier):
    """
    - Torchscript archives the model in zip format.
    - Model saved by torch.jit.save.
    - constants.pkl is the main difference between PTH and TorchTraced
        - see https://github.com/pytorch/pytorch/blob/e9ebda29d87ce0916ab08c06ab26fd3766a870e5/torch/serialization.py#L1180
    """
    FORMAT = ModelFormat.TORCH_TRACED

    @classmethod
    def is_me(cls, model_path: Union[str, Path]):

        if get_src_type(model_path) != SrcType.FILE:
            return False
        with open(model_path, 'rb') as f:
            if not f.read(4) == bytes.fromhex('504b0304'):
                return False
        try:
            z = zipfile.ZipFile(model_path)
            file_names = '|'.join(z.namelist())
            return 'code/__torch__' in file_names and \
                   'data.pkl' in file_names and \
                   'data/' in file_names and \
                   'constants.pkl' in file_names
        except OSError:
            return False


class PB(Identifier):
    """
    Use file extension and magic number to identify the file
    """

    FORMAT = ModelFormat.PB

    @classmethod
    def is_me(cls, model_path: Union[str, Path]):
        if get_src_type(model_path) != SrcType.FILE:
            return False
        # I dont find such pattern in:
        # 1. https://github.com/chen0040/java-tensorflow-samples/blob/master/audio-classifier/src/main/resources/tf_models/resnet-v2.pb
        # 2. https://github.com/bugra/putting-tensorflow-2-models-to-production/blob/master/models/resnet/1538687457/saved_model.pb
        # 3. https://github.com/U-t-k-a-r-s-h/Auto-Labeling-tool-using-Tensorflow/blob/master/Mobilenet.pb
        # 4. https://codechina.csdn.net/shy_201992/human-pose-estimation-opencv/-/blob/master/graph_opt.pb
        #
        # with open(path, 'rb') as f:
        #     if f.read(8) == 'PBDEMS2\0':
        #         return True

        # check if 'dtype' exists in the first 1k of the file.
        with open(model_path, 'rb') as f:
            if bytes.fromhex('0A05647479706512') in f.read(1024):
                return True

        return str(model_path).lower().endswith('.pb')


class TFLITE(Identifier):
    """
    Use file extension and magic number to identify the file
    """

    FORMAT = ModelFormat.TFLITE

    @classmethod
    def is_me(cls, model_path: Union[str, Path]):

        if get_src_type(model_path) != SrcType.FILE:
            return False

        if str(model_path).lower().endswith(".tflite"):
            return True

        with open(model_path, 'rb') as f:
            if bytes.fromhex('1C00000054464C33') in f.read(8):
                return True

        return False


class SavedModel(Identifier):
    """
    Use directory pattern to identify the file
    """

    FORMAT = ModelFormat.SAVED_MODEL

    @classmethod
    def is_me(cls, model_path: Union[str, Path]):

        if get_src_type(model_path) != SrcType.DIR:
            return False

        return (os.path.exists(os.path.join(model_path, 'saved_model.pb')) and
                os.path.exists(os.path.join(model_path, 'variables')))


class ZippedSavedModel(Identifier):
    """
    Use directory pattern to identify the file
    """

    FORMAT = ModelFormat.ZIPPED_SAVED_MODEL

    @classmethod
    def is_me(cls, model_path: Union[str, Path]) -> bool:

        if get_src_type(model_path) != SrcType.FILE:
            return False
        try:
            z = zipfile.ZipFile(model_path)
            file_names = '|'.join(z.namelist())
            return 'saved_model.pb' in file_names and 'variables' in file_names
        except Exception:
            return False

# def _check_object_type(expect_type_str, obj):
#     type_str = ""
#     try:
#         type_str += str(inspect.getmro((obj)))
#     except:
#         type_str += ""
#     type_str += "|"
#     type_str += str(type(obj))
#     return expect_type_str in type_str


# class TFKerasModel(Identifier):
#     ''' Use python MRO to check if it contains specific str
#     '''

#     FORMAT = ModelFormat.TF_KERAS_MODEL

#     @classmethod
#     def is_me(cls, model_path: Union[str, Path]):
#         if get_src_type(model_path) != SrcType.OBJ:
#             return False
#         return _check_object_type('tensorflow.python.keras', model_path)


# class TFSession(Identifier):
#     ''' Use python MRO to check if it contains specific str
#     '''
#     FORMAT = ModelFormat.TF_SESSION

#     @classmethod
#     def is_me(cls, model_path: Union[str, Path]):
#         if get_src_type(model_path) != SrcType.OBJ:
#             return False
#         return _check_object_type('tensorflow.python.client.session.Session',
#                                   model_path)


# class KerasModel(Identifier):
#     '''Use python MRO to check if it contains specific str
#     Keras 2.5.0 Serializer
#     '''

#     FORMAT = ModelFormat.KERAS_MODEL

#     @classmethod
#     def is_me(cls, model_path: Union[str, Path]):
#         if get_src_type(model_path) != SrcType.OBJ:
#             return False
#         return _check_object_type('keras.', model_path)


# class PytorchModel(Identifier):
#     """Use python MRO to check if it contains specific str"""

#     FORMAT = ModelFormat.PT_NN_MODULE

#     @classmethod
#     def is_me(cls, model_path: Union[str, Path]):

#         if get_src_type(model_path) != SrcType.OBJ:
#             return False

#         return (_check_object_type('torch.nn.module', model_path) or
#                 _check_object_type('torchvision.models.', model_path))


class OpenvinoIRDir(Identifier):
    FORMAT = ModelFormat.OPENVINO_IRDIR

    @classmethod
    def is_me(cls, model_path: Union[str, Path]):
        if get_src_type(model_path) != SrcType.DIR:
            return False
        files = glob.glob(f"{model_path}/*")

        return (any([f.endswith(".xml") for f in files]) and
                any([f.endswith(".bin") for f in files]) and
                any([f.endswith(".mapping") for f in files]))


class TensorrtPLAN(Identifier):
    FORMAT = ModelFormat.TRT_PLAN

    @classmethod
    def is_me(cls, model_path: Union[str, Path]):
        if get_src_type(model_path) != SrcType.FILE:
            return False
        return str(model_path).endswith(".plan") or str(
            model_path).endswith(".engine")


class CaffeDir(Identifier):
    FORMAT = ModelFormat.CAFFE_DIR

    @classmethod
    def is_me(cls, model_path: Union[str, Path]):
        if get_src_type(model_path) != SrcType.DIR:
            return False
        files = glob.glob(f"{model_path}/*")

        return (any([f.endswith(".caffemodel") for f in files]) and
                any([f.endswith(".prototxt") for f in files]))


class ZippedCaffeDir(Identifier):
    """
    Use directory pattern to identify the file
    """

    FORMAT = ModelFormat.ZIPPED_CAFFE_DIR

    @classmethod
    def is_me(cls, model_path: Union[str, Path]) -> bool:

        if get_src_type(model_path) != SrcType.FILE:
            return False
        try:
            z = zipfile.ZipFile(model_path)
            files = z.namelist()
            return (any([f.endswith(".caffemodel") for f in files]) and
                    any([f.endswith(".prototxt") for f in files]))
        except Exception:
            return False


class ZippedOpenvinoIRDir(Identifier):

    FORMAT = ModelFormat.ZIPPED_OPENVINO_IRDIR

    @classmethod
    def is_me(cls, model_path: Union[str, Path]) -> bool:

        if get_src_type(model_path) != SrcType.FILE:
            return False
        try:
            z = zipfile.ZipFile(model_path)
            files = z.namelist()
            return (any([f.endswith(".xml") for f in files]) and
                    any([f.endswith(".bin") for f in files]) and
                    any([f.endswith(".mapping") for f in files]))
        except Exception:
            return False