from .core.options import Options

# Options initialize is required for OptionsRegistry to work properly
from oasis.forest.runtimes.openvino.runtime import OpenvinoOptions
from oasis.forest.runtimes.onnx.runtime import ONNXOptions
from oasis.forest.runtimes.tensorrt.runtime import TensorRTOptions
