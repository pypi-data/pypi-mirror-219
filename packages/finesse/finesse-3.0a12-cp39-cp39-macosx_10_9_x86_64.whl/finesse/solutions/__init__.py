"""Outputs from a simulation / analysis run.

Listed below are all the sub-modules of the ``solutions`` module with a brief
description of the contents of each.
"""
from finesse.solutions.base import BaseSolution
from finesse.solutions.array import ArraySolution
from finesse.solutions.beamtrace import (
    ABCDSolution,
    PropagationSolution,
    AstigmaticPropagationSolution,
    BeamTraceSolution,
)


class SimpleSolution(BaseSolution):
    """Simple solution object that can just be called and various results added to
    it."""

    pass


__all__ = (
    "BaseSolution",
    "ArraySolution",
    "ABCDSolution",
    "PropagationSolution",
    "AstigmaticPropagationSolution",
    "BeamTraceSolution",
)
