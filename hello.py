import sys


def main(name: str = "World") -> None:
    """Print a greeting for the given name.

    Args:
        name: The name to greet. Defaults to "World".
    """
    print(f"Hello, {name}!")


if __name__ == "__main__":
    cli_name = sys.argv[1] if len(sys.argv) > 1 else "World"
    main(cli_name)
