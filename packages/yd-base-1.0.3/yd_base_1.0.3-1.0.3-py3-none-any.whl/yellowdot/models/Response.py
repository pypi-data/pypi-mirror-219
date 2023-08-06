from dataclasses import dataclass
from typing import Union, Optional


@dataclass(init=True, repr=True, eq=True, unsafe_hash=True, frozen=True)
class YDResponseModel:
    """YellowDot API Response Model"""
    code: int
    message: Optional[str] = None
    payload: Optional[Union[dict, list]] = None
