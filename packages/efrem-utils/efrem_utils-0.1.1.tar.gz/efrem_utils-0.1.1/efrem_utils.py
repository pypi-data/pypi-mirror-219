from typing import Callable, TypeVar, Iterable

T = TypeVar("T")
W = TypeVar("W")

def validated_input(
    msg: str | None = None,
    validators: Iterable[tuple[Callable[[T], bool], str | Callable[[T], str] | None]] | None = None,
    constructor: Callable[[T], W] = str,
    precomp: Callable[[str], T] | None = None,
    precomp_error: str | Callable[[str], str] | None = None
) -> Callable[[], W]:
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

    if msg is None:
        msg = f"Enter a {constructor}: "

    if validators is None:
        validators = [
            (lambda buffer: constructor(buffer) or True, lambda buffer: f"<{buffer}> is not a valid {constructor}")
        ]
    
    if precomp_error is None:
        precomp_error = "Precomputation failed at input == <{buffer}> :("
        
    def inner() -> W:
        while True:

            buffer: str = input(msg)

            if precomp is not None:
                try:
                    buffer: T = precomp(buffer)
                except:
                    print(precomp_error(buffer) if callable(precomp_error) else precomp_error.format(buffer=buffer))
                    continue

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

            else: # if no break happens in validation checking - return
                return constructor(buffer)
                
    return inner