from __future__ import annotations

import flatbuffers
import numpy as np

import flatbuffers
import typing

uoffset: typing.TypeAlias = flatbuffers.number_types.UOffsetTFlags.py_type

class NavStatus(object):
  UNKNOWN: int
  UNALIGNED: int
  COARSE_ALIGN: int
  FINE_ALIGN: int
  ALIGNED: int

