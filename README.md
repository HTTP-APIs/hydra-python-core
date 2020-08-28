# hydra-python-core
This library provides the core functions to implement Hydra Official Specification in Python.

Currently the library mainly consists of 2 modules `doc_writer` and `doc_maker` which help hydrus generalise a lot of things. The documentation is available at
https://hydra-python-core.readthedocs.io/en/develop/

-> `doc_writer` creates a new API Documentation as well as a `HydraDoc` object while,
-> `doc_maker` uses an existing API Documentation to create a `HydraDoc` object 



### Installation

To install the library:

```bash
pip install git+https://github.com/HTTP-APIs/hydra-python-core.git#egg=hydra_python_core
```

**Note :-** If using hydrus, the library doesn't need to be installed separately as it is already a part of `requirements.txt` for hydrus.



### Usage

To import the modules:

```python
from hydra_python_core import doc_writer
from hydra_python_core import doc_maker
```

*Porting out from hydrus the hydraspecs directory*
