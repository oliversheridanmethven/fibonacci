from typing import Annotated, Literal
from annotated_types import Ge
PositiveInt = Annotated[int, Ge(0)]
Square2x2Matrix = Annotated[list[list[int]], Literal[2, 2]]