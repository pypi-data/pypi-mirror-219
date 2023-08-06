from typing import TypeVar, Callable, Union, Coroutine, Any, Tuple

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
WrapperType = Callable[['Callable[..., T]'], 'Callable[..., T]']
ExpType = Union['type[Exception]', Tuple[type[Exception], ...]]
NumType = Union[int, float]
IntervalType = Union[NumType, Tuple[NumType, NumType, NumType], Tuple[NumType, NumType, Callable[[NumType], NumType]]]
AsyncFuncType = Callable[..., Coroutine[Any, Any, T]]
Exps = Union['type[Exception]', Tuple[type[Exception], ...]]

class ExpOccurred: pass
