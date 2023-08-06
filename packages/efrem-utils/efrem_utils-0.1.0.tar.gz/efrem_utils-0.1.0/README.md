# `efrem-utils`

A package with utility functions to abstract some logic. 

## `explanation`

### `validated_input` usage:

The `validated_input` exists to simplify getting a valid input from a user that passes some criterias.

Its signature/definition might be a bit hard to read, so a bit of an explanation:
```py
---
msg: A string / None (by default), will be used as the prompt for the input() calls.
If its None - it defaults to f"Enter a {constructor}: "
--- # After msg, all arguments are keyword-only
precomp(utational function): A function which has to take a string and return.. anything, pretty much.
Honourable mentions: str.strip, str.lower, str.split. Defaults to None so it doesnt mutate the input.
---
validators: An iterable with tuples (pairs) of function:error_message.

The functions needs to accept the same type that the precomp function returns.

The error_message is displayed when either an exception is raised during the attempt of validation [Which leads to a neat trick for getting a valid input of some type], or when the value it returns is falsy.

The error message can be either None (in this case it wont be displayed), or a static string, or a template-string [i.e "{buffer} is not an integer". Consider that `buffer` is the keyword for the users input here, which gets passed with a .format(buffer=buffer) call]

Defaults to None and gets replaced by a typecheck using the constructor and a short-circuit logic. [constructor(buffer) or True]
---
constructor: A function which needs to take the same type that the precomp function returns and it will be used to actually return the value once the input has been validated.

Defaults to str :D
---
The function returns another function so you can then call it with no arguments and get a validated input.
```

```py
# Some examples:

get_float = efrem_utils.validated_input(constructor=float) # Works because of validators defaulting to a float typecheck and msg defaulting to f"Enter a {float}"

choices = ["a", "bob", "yes"]
get_choice = efrem_utils.validated_input(
    msg=f"Enter your choice [Choose from <{','.join(choices)}>]: ",
    validators=[
        (lambda buffer: buffer in choices, "{buffer} is not a valid choice") # the {buffer} in the template string is important
    ],
    precomp=lambda buffer: buffer.lower().strip() # using lambda to combine multiple precomputation functions
)
```

**For more information check:** [`examples directory`](https://github.com/NikitaNightBot/efrem-utils/tree/main/examples)