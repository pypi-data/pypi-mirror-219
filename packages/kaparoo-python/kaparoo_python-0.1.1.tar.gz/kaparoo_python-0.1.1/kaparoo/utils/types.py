# -*- coding: utf-8 -*-

from typing import TypeVar

# type variables
T = TypeVar("T")
U = TypeVar("U")
K = TypeVar("K")
V = TypeVar("V")

# covariant type variables
T_co = TypeVar("T_co", covariant=True)
U_co = TypeVar("U_co", covariant=True)
K_co = TypeVar("K_co", covariant=True)
V_co = TypeVar("V_co", covariant=True)
