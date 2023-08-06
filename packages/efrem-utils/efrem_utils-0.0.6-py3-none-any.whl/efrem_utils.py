from typing import Callable, TypeVar, Iterable

T = TypeVar("T") # To typehint that the function returns the same type as the constructor

def get_validated_input(*, msg: str = "", validators: Iterable[tuple[Callable[[str], bool], str | Callable[[str], str] | None]] | None = None, constructor: Callable[[str], T] = str, precomp: Callable[[str], str] | None = None) -> Callable[[], T]:
    """
    An attempt at abstracting the case of using input() repeatedly until it is valid;
    Returns a function (to use instead of input()), but the message is specified at the part of calling this function,
    not the function you get itself, mostly because the error messages in the validator argument should be related to the input message.

    When validators aren't specified, it uses the constructor as the validator. I.e, if you use constructor=int, the validator will check if the input is an integer.

    If an error is raised during the process of validation, it will count as a fail of validation, so 
    you can use this to make easy typechecks by using something like:
    `lambda buffer: float(buffer) or True` as a validator function.

    The precomp(utation) function will be applied to the input before validation `and` when it will be passed to a constructor. [ It applies to the value of input() ]
    """

    if validators is None:
        validators = [
            (lambda buffer: constructor(buffer) or True, lambda buffer: f"<{buffer}> is not a valid {constructor}")
        ]
    def inner() -> T:
        while True:
            buffer: str = precomp(input(msg)) if precomp is not None else input(msg)
            for validator, err_msg in validators:
                result: bool
                try:
                    result = validator(buffer)
                except:
                    result = False

                if not result:
                    if err_msg is not None:
                        print(err_msg(buffer) if callable(err_msg) else err_msg.format(buffer=buffer))
                    break

            else:
                return constructor(buffer)
                
    return inner