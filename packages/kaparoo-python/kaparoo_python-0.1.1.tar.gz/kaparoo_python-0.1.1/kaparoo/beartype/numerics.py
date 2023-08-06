# -*- coding: utf-8 -*-

__all__ = (
    "PosInt",
    "NegInt",
    "NonPosInt",
    "NonNegInt",
    "PositiveInt",
    "NegativeInt",
    "NonPositiveInt",
    "NonNegativeInt",
)

from typing import Annotated, TypeAlias

from beartype.vale import Is

NegativeInt: TypeAlias = Annotated[int, Is[lambda x: x < 0]]
PositiveInt: TypeAlias = Annotated[int, Is[lambda x: x > 0]]
NonNegativeInt: TypeAlias = Annotated[int, Is[lambda x: x >= 0]]
NonPositiveInt: TypeAlias = Annotated[int, Is[lambda x: x <= 0]]

NegInt: TypeAlias = NegativeInt
PosInt: TypeAlias = PositiveInt
NonPosInt: TypeAlias = NonPositiveInt
NonNegInt: TypeAlias = NonNegativeInt
