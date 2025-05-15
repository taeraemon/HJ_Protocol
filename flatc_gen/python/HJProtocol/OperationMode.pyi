from __future__ import annotations

import flatbuffers
import numpy as np

import flatbuffers
import typing

uoffset: typing.TypeAlias = flatbuffers.number_types.UOffsetTFlags.py_type

class OperationMode(object):
  UNKNOWN: int
  INIT: int
  IDLE: int
  DIAG: int
  ARMED: int
  FLIGHT: int
  KILL: int
  RECOVERY: int

