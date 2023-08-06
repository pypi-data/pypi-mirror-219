### abi_parser

A simple way to parse your ABIs in Python.

### Installation

```bash
pip install abi_parser
```

```python
from abi_parser import ContractABI
abi = ContractABI('<PATH TO ABI JSON'>)

# name
name = abi.name

# functions
functions = abi.functions

# events - todo
# events = abi.events

# get function by name
function = abi.get_function('<function_name>')

# bytecode - todo
# bytecode = abi.bytecode

# get function by signature - todo
# function = abi.get_function_by_signature('<function_signature>')
```
