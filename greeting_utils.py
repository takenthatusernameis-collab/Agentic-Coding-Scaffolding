def format_greeting(name: str, greeting: str = "Hello") -> str:
    """Return a formatted greeting string for the given name.

    Args:
        name: The name to greet.
        greeting: The greeting word to use. Defaults to "Hello".

    Returns:
        A string of the form "{greeting}, {name}!".
    """
    return f"{greeting}, {name}!"


def format_names(names: list[str], greeting: str = "Hello") -> str:
    """Return a comma-separated list of formatted greetings.

    Args:
        names: The names to greet.
        greeting: The greeting word to use. Defaults to "Hello".

    Returns:
        A string of the form "{greeting}, {name1}! {greeting}, {name2}!".
    """
    return " ".join(format_greeting(name, greeting) for name in names)


def format_farewell(name: str, farewell: str = "Goodbye") -> str:
    """Return a formatted farewell string for the given name.

    Args:
        name: The name to farewell.
        farewell: The farewell word to use. Defaults to "Goodbye".

    Returns:
        A string of the form "{farewell}, {name}!".

    Raises:
        TypeError: If ``name`` or ``farewell`` is not a str.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a str")
    if not isinstance(farewell, str):
        raise TypeError("farewell must be a str")
    return f"{farewell}, {name}!"


def format_welcome(name: str, welcome: str = "Welcome") -> str:
    """Return a formatted welcome string for the given name.

    Args:
        name: The name to welcome.
        welcome: The welcome word to use. Defaults to "Welcome".

    Returns:
        A string of the form "{welcome}, {name}!".

    Raises:
        TypeError: If ``name`` or ``welcome`` is not a str.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a str")
    if not isinstance(welcome, str):
        raise TypeError("welcome must be a str")
    return f"{welcome}, {name}!"