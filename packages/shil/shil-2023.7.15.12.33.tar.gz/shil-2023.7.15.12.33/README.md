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
* Support or [rich protocols](#placeholder)

---------------------------------------------------------------------------------

## Installation

See [pypi](https://pypi.org/project/shil/) for available releases.

```
pip install shil
```

---------------------------------------------------------------------------------

## Usage

---------------------------------------------------------------------------------

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

# Rich console output for Invocations and InvocationResponse
import rich
rich.print(resp)
```
