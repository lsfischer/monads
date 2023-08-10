from typing import TypeVar, Generic, Callable

T = TypeVar("T")
E = TypeVar("E")
R = TypeVar("R")


class Result(Generic[T, E]):
    def or_else_throw(self) -> T:
        """
        If the result is successful, returns the value as Ok, otherwise raises NotImplementedError
        :return: The value in Ok
        :raises: NotImplemented error if the result contains an error value
        """
        raise NotImplementedError("Must be implemented by subclasses")

    def is_success(self) -> bool:
        """
        If the result is a failure, returns the value in Err, otherwise raises NotImplementedError
        :return: The value in Err
        :raises: NotImplementedError error if the result contains a successful value
        """
        raise NotImplementedError("Must be implemented by subclasses")

    def is_failure(self) -> bool:
        raise NotImplementedError("Must be implemented by subclasses")

    def failure_reason(self) -> E:
        raise NotImplementedError("Must be implemented by subclasses")

    def map(self, func: Callable[[T], R]) -> "Result[R, E]":
        raise NotImplementedError("Must be implemented by subclasses")

    def flat_map(self, func: Callable[[T], "Result[R, E]"]) -> "Result[R, E]":
        raise NotImplementedError("Must be implemented by subclasses")

    def recover(self, func: Callable[[E], T]) -> T:
        raise NotImplementedError("Must be implemented by subclasses")

    @staticmethod
    def error(err: E) -> "Result[T, E]":
        return Err(err)

    @staticmethod
    def ok(val: T) -> "Result[T, E]":
        return Ok(val)


class Ok(Result[T, E]):
    _val: T

    def __init__(self, val: T):
        self._val = val

    def or_else_throw(self) -> T:
        return self._val

    def get_failure_reason(self) -> E:
        raise NotImplementedError(
            f"No failure value present, but contains an object instead: {type(self._val).__name__}"
        )

    def is_success(self) -> bool:
        return True

    def is_failure(self) -> bool:
        return False

    def map(self, func: Callable[[T], R]) -> Result[R, E]:
        return Ok(func(self._val))

    def flat_map(self, func: Callable[[T], Result[R, E]]) -> Result[R, E]:
        return func(self._val)

    def recover(self, func: Callable[[E], T]) -> T:
        return self._val


class Err(Result[T, E]):
    _val: E

    def __init__(self, val: E):
        self._val = val

    def or_else_throw(self) -> T:
        raise NotImplementedError(
            f"No success value present, but contains an error instead: {self._val}"
        )

    def get_failure_reason(self) -> E:
        return self._val

    def is_success(self) -> bool:
        return False

    def is_failure(self) -> bool:
        return True

    def map(self, func: Callable[[T], R]) -> Result[R, E]:
        return Err(self._val)

    def flat_map(self, func: Callable[[T], Result[R, E]]) -> Result[R, E]:
        return Err(self._val)

    def recover(self, func: Callable[[E], T]) -> T:
        return func(self._val)
