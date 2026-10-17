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
