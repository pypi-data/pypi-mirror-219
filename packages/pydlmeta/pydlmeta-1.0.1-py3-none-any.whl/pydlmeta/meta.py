from typing import List, Union, Tuple, Dict
from abc import abstractmethod
import zipfile
import glob
from dataclasses import dataclass

from pydlmeta.identifier.types import ModelFormat
from pydlmeta.identifier.model  import identify
from pydlmeta.utils import get_temp_path
from pydlmeta.dtype_map import TF_map, ONNX_map, NP_map, OV_map
from pydlmeta.identifier.types import ModelDataType
import logging
logger = logging.getLogger(__name__)
PYTORCH_MSG_SKIP_SHAPE = "Set TensorMeta's shape to None since pytorch model input/output shape could be flexible."

@dataclass
class TensorMeta:
    name: str
    shape: Union[None, Tuple[int, ...]] = None
    dtype: ModelDataType = ModelDataType.NON_SPECIFIED

    def dump(self) -> Dict:
        _dtype =  ModelDataType.NON_SPECIFIED
        if self.dtype:
            _dtype = self.dtype
        return {"name": self.name, "shape": self.shape, "type": _dtype.name}


class MetadataRetriverRegistry(type):

    REGISTRY: List = []

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if name != "MetadataRetriver":
            cls.REGISTRY.append(new_cls)
        return new_cls


class ModelMeta:

    def __init__(self, inputs: List[TensorMeta], outputs: List[TensorMeta]):
        self.inputs = inputs
        self.outputs = outputs


class MetadataRetriver(metaclass=MetadataRetriverRegistry):

    FORMAT: ModelFormat = ModelFormat.NON_SPECIFIED

    @classmethod
    def is_me(cls, model_path) -> bool:
        return identify(model_path) == cls.FORMAT

    @abstractmethod
    def retrieve_inputs(self, model_path) -> List[TensorMeta]:
        raise NotImplementedError("`retrieve_inputs` has to be implemented")

    @abstractmethod
    def retrieve_outputs(self, model_path) -> List[TensorMeta]:
        raise NotImplementedError("`retrieve_outputs` has to be implemented")

    def retrieve(self, model_path) -> ModelMeta:
        inputs = self.retrieve_inputs(model_path)
        logger.debug(f"Inputs: {inputs}")
        outputs = self.retrieve_outputs(model_path)
        logger.debug(f"Outputs: {outputs}")
        return ModelMeta(inputs=inputs, outputs=outputs)


def retrieve_model_metadata(model_path) -> ModelMeta:
    for metadataretriever in MetadataRetriver.REGISTRY:
        if metadataretriever.is_me(model_path):
            return metadataretriever().retrieve(model_path)

    raise NotImplementedError(f"Unable to retrieve metadata of {model_path}")


class H5(MetadataRetriver):

    FORMAT = ModelFormat.H5


    def retrieve_inputs(self, model_path) -> List[TensorMeta]:
        from tensorflow import keras  # type: ignore[import]
        _model = keras.models.load_model(model_path)

        res = []
        for x in _model.inputs:
            shape = tuple(-1 if not s else s for s in x.shape)
            res.append(
                TensorMeta(name=x.name, shape=shape,
                       dtype=TF_map.map(x.dtype)))
        return res

    def retrieve_outputs(self, model_path) -> List[TensorMeta]:
        from tensorflow import keras  # type: ignore[import]
        _model = keras.models.load_model(model_path)

        res = []
        for x in _model.outputs:
            shape = tuple(-1 if not s else s for s in x.shape)
            res.append(
                TensorMeta(name=x.node.outbound_layer.name,
                       shape=shape,
                       dtype=TF_map.map(x.dtype)))

        return res


class ONNX(MetadataRetriver):

    FORMAT = ModelFormat.ONNX

    def retrieve_inputs(self, model_path) -> List[TensorMeta]:
        import onnx
        onnx_model = onnx.load(model_path)

        input_all = [node.name for node in onnx_model.graph.input]
        input_initializer = [node.name for node in onnx_model.graph.initializer]
        net_feed_input = list(set(input_all) - set(input_initializer))

        res = []

        for input in onnx_model.graph.input:

            shape = tuple(
                xx.dim_value for xx in input.type.tensor_type.shape.dim)
            shape = tuple(-1 if int(s) == 0 else s for s in shape)

            if input.name in net_feed_input:
                res.append(
                    TensorMeta(input.name, shape,
                           ONNX_map.map(input.type.tensor_type.elem_type)))

        return res

    def retrieve_outputs(self, model_path) -> List[TensorMeta]:
        import onnx
        model = onnx.load(model_path)
        res = []
        for model_output in model.graph.output:
            shape = tuple(
                s.dim_value for s in model_output.type.tensor_type.shape.dim)
            shape = tuple(-1 if int(s) == 0 else s for s in shape)
            res.append(
                TensorMeta(
                    model_output.name, shape,
                    ONNX_map.map(model_output.type.tensor_type.elem_type)))
        return res


class PTH(MetadataRetriver):

    FORMAT = ModelFormat.PTH

    def retrieve_inputs(self, model_path) -> List[TensorMeta]:
        import torch
        logger.warning(PYTORCH_MSG_SKIP_SHAPE)
        _model = torch.load(model_path)
        tensor = list(_model.parameters())[  # type: ignore[union-attr]
            0].detach()
        t_name = tensor.name
        tensor = tensor.numpy()
        return [
            TensorMeta(t_name, None, NP_map.map(tensor.dtype.type))
        ]

    def retrieve_outputs(self, model_path) -> List[TensorMeta]:
        import torch
        logger.warning(PYTORCH_MSG_SKIP_SHAPE)
        _model = torch.load(model_path)
        # type: ignore[union-attr]
        tensor = list(_model.parameters())[-1].detach()
        t_name = tensor.name
        tensor = tensor.numpy()
        return [
            TensorMeta(t_name, None, NP_map.map(tensor.dtype.type))
        ]


class PB(MetadataRetriver):

    FORMAT = ModelFormat.PB

    # https://stackoverflow.com/questions/43517959/given-a-tensor-flow-model-graph-how-to-find-the-input-node-and-output-node-name
    def _load_graph(self, frozen_graph_filename):
        import tensorflow as tf
        with tf.io.gfile.GFile(frozen_graph_filename, "rb") as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def)

        ops = graph.get_operations()
        return ops

    def retrieve_inputs(self, model_path) -> List[TensorMeta]:
        import tensorflow as tf
        ops = self._load_graph(model_path)
        inputs = []
        for op in ops:
            if len(op.inputs) == 0 and op.type != 'Const':
                inputs.append(op)

        res = []
        """
        Eliminating "/" in the name is still under experiment
        This bug happens when converting bert-squad-384.pb which's input
        should be "logits" but is "import/logits" in the graph
        """
        for x in inputs:
            res.append(
                TensorMeta(name=x.name.split("/")[-1],
                       shape=tuple(
                           xx if xx else -1 for xx in x.outputs[0].shape),
                       dtype=TF_map.map(x.outputs[0].dtype)))
        return res
        """
        >>> [x.size for x in graph_def.node[0].attr['shape'].shape.dim]
        [-1, 96, 96, 3]
        """

    def retrieve_outputs(self, model_path) -> List[TensorMeta]:
        import tensorflow as tf
        ops = self._load_graph(model_path)
        inputs = []
        outputs_set = set(ops)

        for op in ops:
            if len(op.inputs) == 0 and op.type != 'Const':
                inputs.append(op)
            else:
                for input_tensor in op.inputs:
                    if input_tensor.op in outputs_set:
                        outputs_set.remove(input_tensor.op)

        outputs = list(outputs_set)
        res = []
        """
        Eliminating "/" in the name is still under experiment
        This bug happens when converting bert-squad-384.pb which's input
        should be "logits" but is "import/logits" in the graph
        """
        for x in outputs:
            res.append(
                TensorMeta(name=x.name.split("/")[-1],
                       shape=tuple(
                           xx if xx else -1 for xx in x.outputs[0].shape),
                       dtype=TF_map.map(x.outputs[0].dtype)))
        return res


class SavedModel(MetadataRetriver):

    FORMAT = ModelFormat.SAVED_MODEL

    def retrieve_inputs(self, model_path) -> List[TensorMeta]:
        from tensorflow import keras  # type: ignore[import]
        _model = keras.models.load_model(model_path)
        return [
            TensorMeta(name=x.name,
                   shape=tuple(xx if xx else -1 for xx in x.shape),
                   dtype=TF_map.map(x.dtype)) for x in _model.inputs
        ]

    def retrieve_outputs(self, model_path) -> List[TensorMeta]:

        from tensorflow import keras  # type: ignore[import]
        _model = keras.models.load_model(model_path)

        return [
            TensorMeta(name=x.name,
                   shape=tuple(xx if xx else -1
                               for xx in x.shape),
                   dtype=TF_map.map(x.dtype))
            for x in _model.inputs
            for x in _model.outputs
        ]



class TFKerasModel(MetadataRetriver):

    FORMAT = ModelFormat.TF_KERAS_MODEL


    def retrieve_inputs(self, model_path) -> List[TensorMeta]:
        return [
            TensorMeta(name=x.name,
                   shape=tuple(xx if xx else -1 for xx in x.shape),
                   dtype=TF_map.map(x.dtype)) for x in model_path.inputs
        ]

    def retrieve_outputs(self, model_path) -> List[TensorMeta]:
        return [
            TensorMeta(name=x.name,
                   shape=tuple(xx if xx else -1 for xx in x.shape),
                   dtype=TF_map.map(x.dtype)) for x in model_path.outputs
        ]


class KerasModel(MetadataRetriver):
    '''
    Keras 2.5.0 Serializer
    '''

    FORMAT = ModelFormat.KERAS_MODEL

    def retrieve_inputs(self, model_path) -> List[TensorMeta]:
        return [
            TensorMeta(name=x.name,
                   shape=tuple(xx if xx else -1 for xx in x.shape),
                   dtype=TF_map.map(x.dtype)) for x in model_path.inputs
        ]  # type: ignore[union-attr]

    def retrieve_outputs(self, model_path) -> List[TensorMeta]:
        return [
            TensorMeta(name=x.name,
                   shape=tuple(xx if xx else -1 for xx in x.shape),
                   dtype=TF_map.map(x.dtype)) for x in model_path.outputs
        ]  # type: ignore[union-attr]


class PytorchModel(MetadataRetriver):
    """Use python MRO to check if it contains specific str"""

    FORMAT = ModelFormat.PT_NN_MODULE

    def retrieve_inputs(self, model_path) -> List[TensorMeta]:
        logger.warning(PYTORCH_MSG_SKIP_SHAPE)
        _model = model_path
        tensor = list(_model.parameters())[  # type: ignore[union-attr]
            0].detach()
        t_name = tensor.name
        tensor = tensor.numpy()
        return [
            TensorMeta(t_name,None,
                   NP_map.map(tensor.dtype.type))
        ]

    def retrieve_outputs(self, model_path) -> List[TensorMeta]:
        logger.warning(PYTORCH_MSG_SKIP_SHAPE)
        _model = model_path
        # type: ignore[union-attr]
        tensor = list(_model.parameters())[-1].detach()
        t_name = tensor.name
        tensor = tensor.numpy()
        return [
            TensorMeta(t_name, None,
                   NP_map.map(tensor.dtype.type))
        ]


class TorchTracedModel(MetadataRetriver):

    FORMAT = ModelFormat.TORCH_TRACED

    def retrieve_inputs(self, model_path) -> List[TensorMeta]:
        import torch
        logger.warning(PYTORCH_MSG_SKIP_SHAPE)
        _model = torch.jit.load(model_path)
        tensor = list(_model.parameters())[  # type: ignore[union-attr]
            0].detach()
        t_name = tensor.name
        tensor = tensor.numpy()
        return [
            TensorMeta(t_name, None,
                   NP_map.map(tensor.dtype.type))
        ]

    def retrieve_outputs(self, model_path) -> List[TensorMeta]:
        import torch
        logger.warning(PYTORCH_MSG_SKIP_SHAPE)
        _model = torch.jit.load(model_path)
        # type: ignore[union-attr]
        tensor = list(_model.parameters())[-1].detach()
        t_name = tensor.name
        tensor = tensor.numpy()
        return [
            TensorMeta(t_name, None,
                   NP_map.map(tensor.dtype.type))
        ]


class TFLiteModel(MetadataRetriver):
    """Use python MRO to check if it contains specific str"""

    FORMAT = ModelFormat.TFLITE
    _dtype_map = NP_map

    def retrieve_inputs(self, model_path) -> List[TensorMeta]:

        try:
            import tflite_runtime.interpreter as tflite
            interpreter = tflite.Interpreter(model_path=str(model_path))
        except ModuleNotFoundError:
            import tensorflow as tf
            interpreter = tf.lite.Interpreter(model_path=str(model_path))

        res = []
        for i in interpreter.get_input_details():
            res.append(
                TensorMeta(i["name"],
                       tuple(-1 if not s else int(s) for s in i["shape"]),
                       self._dtype_map.map(i['dtype'])))
        return res

    def retrieve_outputs(self, model_path) -> List[TensorMeta]:
        try:
            import tflite_runtime.interpreter as tflite
            interpreter = tflite.Interpreter(model_path=str(model_path))
        except ModuleNotFoundError:
            import tensorflow as tf
            interpreter = tf.lite.Interpreter(model_path=str(model_path))

        res = []
        for i in interpreter.get_output_details():
            res.append(
                TensorMeta(i["name"],
                       tuple(-1 if not s else int(s) for s in i["shape"]),
                       self._dtype_map.map(i['dtype'])))
        return res


class CaffeDir(MetadataRetriver):
    FORMAT = ModelFormat.CAFFE_DIR

    def retrieve_inputs(self, model_path) -> List[TensorMeta]:
        return []

    def retrieve_outputs(self, model_path) -> List[TensorMeta]:
        return []


class OpenvinoIRDir(MetadataRetriver):
    FORMAT = ModelFormat.OPENVINO_IRDIR

    def get_io_meta(self, inputs_or_outputs):
        res = []
        for x in inputs_or_outputs:
            res.append(
                TensorMeta(x.names.pop(), tuple(x for x in x.shape),
                       OV_map.map(x.element_type.get_type_name())))
        return res

    def retrieve_inputs(self, model_path) -> List[TensorMeta]:
        from openvino.runtime import Core
        ie = Core()
        xmls = list(glob.glob(f"{model_path}/*.xml"))
        if len(xmls) != 1:
            raise RuntimeError(f"Unable to find xml file in {model_path}, "
                               "or model than one xml found.")
        model = ie.read_model(model=xmls[0])
        return self.get_io_meta(model.inputs)

    def retrieve_outputs(self, model_path) -> List[TensorMeta]:
        from openvino.runtime import Core
        ie = Core()
        xmls = list(glob.glob(f"{model_path}/*.xml"))
        if len(xmls) != 1:
            raise RuntimeError(f"Unable to find xml file in {model_path}, "
                               "or model than one xml found.")
        model = ie.read_model(model=xmls[0])
        return self.get_io_meta(model.outputs)


class ZippedModel(MetadataRetriver):
    FORMAT: ModelFormat = ModelFormat.NON_SPECIFIED
    base_retriver: MetadataRetriver() = None
    def retrieve_inputs(self, model_path) -> List[TensorMeta]:
        temp = get_temp_path()
        with zipfile.ZipFile(model_path,
                             'r') as zip_ref:  # type: ignore[arg-type]
            zip_ref.extractall(temp)
        return self.base_retriver.retrieve_inputs(model_path)

    def retrieve_outputs(self, model_path) -> List[TensorMeta]:
        temp = get_temp_path()
        with zipfile.ZipFile(model_path,
                             'r') as zip_ref:  # type: ignore[arg-type]
            zip_ref.extractall(temp)
        return self.base_retriver.retrieve_outputs(model_path)

class ZippedSavedModel(ZippedModel):
    FORMAT = ModelFormat.ZIPPED_SAVED_MODEL
    base_retriver = SavedModel()

class ZippedCaffeModel(ZippedModel):
    FORMAT = ModelFormat.ZIPPED_CAFFE_DIR
    base_retriver = CaffeDir()

class ZippedOpenvinoIRModel(ZippedModel):
    FORMAT = ModelFormat.ZIPPED_OPENVINO_IRDIR
    base_retriver = OpenvinoIRDir()
