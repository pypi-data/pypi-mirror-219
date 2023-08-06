# OASIS-API-CLIENT

OASIS:
- SaaS for ONNC (Open neural network compiler)

## Installation

### Developer install
```
python3 -m pip install -e .
```

### Using pip

```
pip install oasis-api-client
```

## Python API Example

Here is an example to show how to use OASIS python API

```
from oasis.bench import login, Project
# Setup your OASIS API key
api_key = "Your API KEY"
login(api_key)

# Instantiate a projct
project = Project('experiment-1')

# Add a model and its coresponding calibration samples
project.add_model('path/to/model', 'path/to/samples')

# Compile the model and optmize to `CMSIS-NN` backend
project.compile(target='CMSIS-NN-DEFAULT')


# Save the compiled model
deployment = project.save('./output')

```

Please Check https://docs-tinyonnc.skymizer.com/index.html for the full documents.
