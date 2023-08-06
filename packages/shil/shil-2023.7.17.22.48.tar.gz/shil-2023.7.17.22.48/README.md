<table>
  <tr>
    <td colspan=2><strong>
    shil
      </strong>&nbsp;&nbsp;&nbsp;&nbsp;
      <small><small>
      </small></small>
    </td>
  </tr>
  <tr>
    <td width=15%><img src=img/icon.png style="width:150px"></td>
    <td>
    Shell-util library for python.  Includes helpers for subprocess invocation, shell-formatters / pretty-printers, and more.
    </td>
  </tr>
</table>

---------------------------------------------------------------------------------

  * [Overview](#overview)
    * [Features](#features)
  * [Installation](#installation)
  * [Usage](#usage)


---------------------------------------------------------------------------------

## Overview

The `shil` library provides various shell-utilities for python.

### Features

* Helpers for subprocess invocation
* Shell-formatters / pretty-printers
* A somewhat usable parser / grammer for bash
* Console support for [rich](https://rich.readthedocs.io/en/stable/index.html) & [rich protocols](https://rich.readthedocs.io/en/stable/protocol.html)


---------------------------------------------------------------------------------

## Installation

See [pypi](https://pypi.org/project/shil/) for available releases.

```
pip install shil
```

---------------------------------------------------------------------------------

## Usage

See also:

* [the unit-tests](tests/units) for some examples of library usage
* [the smoke-tests](tests/smoke/test.sh) for example usage of stand-alone scripts

```
import shil 
import json

# Working with models for Invocation/InvocationResponse:
req = cmd = shil.Invocation(command='ls /tmp')
resp = cmd()
print(resp.stdout)

# More functional approach:
resp = shil.invoke('ls /tmp')

# Loading data when command-output is JSON
req = cmd = shil.Invocation(command='echo {"foo":"bar"}')
resp = cmd()
print(resp.data)
assert type(resp.data)==type({})

# Uses pydantic, so serialization is straightforward
json.loads(resp.json())
json.loads(req.json())
for k,v in req.dict().items():
  assert getattr(resp,k)==v

# Pass in any loggers you want to use
import logging
logger = logging.getLogger()
shil.invoke('ls /tmp', command_logger=logger.critical, output_logger=logger.warning)

# Also works with rich-loggers
from rich.console import Console 
console = Console(stderr=True)
shil.invoke('ls /tmp', command_logger=console.log)

# Rich-console output for `Invocation` and `InvocationResponse`
import rich
rich.print(req)
rich.print(resp)


# Instantiate a `Runner` to stay DRY
console=Console(stderr=True)
runner = shil.Runner(
  output_logger=console.log,
  command_logger=console.log)
runner('ls /tmp')
```
