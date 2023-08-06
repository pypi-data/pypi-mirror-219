# PyDLmeta

Features: identify the model type belong to which deep learning framework
and extract the meta data if possible. The meta data includes input/output
name and shape of the model.

The supported formats are:

- Tensorflow: frozen model *.pb, *.h5, SavedModel directory, *.tflite

- Pytorch: *.pt, TorchScript

- ONNX: *.onnx

- Caffe model directory: *.caffemodel/ *.prototxt

- Openvino IR directory: *.xml/ *.bin

# Installation
- Create a Python 3.8 environment and activate it.
```
git clone --depth 1 -b develop --recursive https://github.com/skymizer/pydlmeta.git
(cd pydlmeta && python3 -m pip install -e .)
```

# Usage

— Retrieve the metadata of the model
```
from pydlmeta.meta import retrieve_model_metadata
res = retrieve_model_metadata("/path/to/your/model")
```

- Identify model format
```
from pydlmeta.identifier.model import identify
model_format = identify(model_path)
```