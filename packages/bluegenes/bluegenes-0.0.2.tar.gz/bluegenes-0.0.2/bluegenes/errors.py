from typing import Any

def tert(condition: bool, message: str) -> None:
    if condition:
        return
    raise TypeError(message)

def typert(thing: Any, cls: type|list[type], name: str) -> None:
    if type(cls) is list:
        tert(type(thing) in cls,
             f"{name} must be instance of one of {[c.__name__ for c in cls]}")
    else:
        tert(isinstance(thing, cls), f"{name} must be instance of {cls.__name__}")

def vert(condition: bool, message: str) -> None:
    if condition:
        return
    raise ValueError(message)
