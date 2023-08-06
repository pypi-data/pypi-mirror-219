from typing import Any, Callable, Coroutine, Sequence, TypeVar, cast

Func = TypeVar("Func", bound=Callable[..., Any])
AsyncFunc = TypeVar("AsyncFunc", bound=Callable[..., Coroutine[Any, Any, Any]])
AnyType = TypeVar("AnyType")
IntFloatStr = TypeVar("IntFloatStr", int, float, str)

Null = cast(Any, None)
Function = Callable[..., Any]
Some = set[AnyType] | Sequence[AnyType]
