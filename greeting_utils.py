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


def format_thanks(name: str, thanks: str = "Thanks") -> str:
    """Return a formatted thanks string for the given name.

    Args:
        name: The name to thank.
        thanks: The thanks word to use. Defaults to "Thanks".

    Returns:
        A string of the form "{thanks}, {name}!".

    Raises:
        TypeError: If ``name`` or ``thanks`` is not a str.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a str")
    if not isinstance(thanks, str):
        raise TypeError("thanks must be a str")
    return f"{thanks}, {name}!"


def format_congrats(name: str, congrats: str = "Congratulations") -> str:
    """Return a formatted congratulations string for the given name.

    Args:
        name: The name to congratulate.
        congrats: The congratulations word to use. Defaults to "Congratulations".

    Returns:
        A string of the form "{congrats}, {name}!".

    Raises:
        TypeError: If ``name`` or ``congrats`` is not a str.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a str")
    if not isinstance(congrats, str):
        raise TypeError("congrats must be a str")
    return f"{congrats}, {name}!"


def format_apology(name: str, apology: str = "Sorry") -> str:
    """Return a formatted apology string for the given name.

    Args:
        name: The name to apologize to.
        apology: The apology word to use. Defaults to "Sorry".

    Returns:
        A string of the form "{apology}, {name}!".

    Raises:
        TypeError: If ``name`` or ``apology`` is not a str.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a str")
    if not isinstance(apology, str):
        raise TypeError("apology must be a str")
    return f"{apology}, {name}!"


def format_birthday_wish(name: str, wish: str = "Happy Birthday") -> str:
    """Return a formatted birthday wish for the given name.

    Args:
        name: The name to wish.
        wish: The wish phrase to use. Defaults to "Happy Birthday".

    Returns:
        A string of the form "{wish}, {name}!".

    Raises:
        TypeError: If ``name`` or ``wish`` is not a str.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a str")
    if not isinstance(wish, str):
        raise TypeError("wish must be a str")
    return f"{wish}, {name}!"


def multi_greet(names: list[str], greeting: str = "Hello") -> dict[str, str]:
    """Return a dictionary mapping names to their greetings.

    Args:
        names: The names to greet.
        greeting: The greeting word to use. Defaults to "Hello".

    Returns:
        A dict mapping each name to ``format_greeting(name, greeting)``.

    Raises:
        TypeError: If ``names`` is not a list or contains non-str elements,
            or if ``greeting`` is not a str.
    """
    if not isinstance(names, list):
        raise TypeError("names must be a list")
    if not isinstance(greeting, str):
        raise TypeError("greeting must be a str")
    for name in names:
        if not isinstance(name, str):
            raise TypeError("names must contain only str elements")
    return {name: format_greeting(name, greeting) for name in names}
