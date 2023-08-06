#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber
from FiberFusing.fiber_base_class import get_silica_index

micro = 1e-6


class CapillaryTube(GenericFiber):
    def __init__(self, wavelength: float,
                       radius: float,
                       index: float = None,
                       position: tuple = (0, 0)) -> None:

        super().__init__(wavelength=wavelength, position=position)
        self.radius = radius
        self._index = index
        self.initialize()

    @property
    def index(self) -> float:
        if self._index is None:
            raise ValueError("Index hasn't been defined for object")
        return self._index

    @index.setter
    def index(self, value: float) -> None:
        self._index = value
        self.initialize()

    def set_delta_n(self, value: float) -> None:
        self.index = self.pure_silica_index + value

    def initialize(self):
        self.structure_list = []

        self.add_air()

        self.add_next_structure_with_index(
            name='inner_clad',
            index=self.index,
            radius=self.radius
        )


class FluorineCapillaryTube(GenericFiber):
    def __new__(cls, wavelength: float, delta_n: float = -15e-3, **kwargs):
        silica_index = get_silica_index(wavelength=wavelength)
        return CapillaryTube(wavelength=wavelength, **kwargs, index=silica_index + delta_n)

# -
