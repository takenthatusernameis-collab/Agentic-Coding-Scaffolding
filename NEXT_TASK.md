# Task for Next Agent

Modify hello.py to accept an optional command line argument for a name to greet, defaulting to 'World' if no argument is provided.

Requirements:
1. Update the main() function to accept an optional name parameter
2. If no command line argument is provided, default to greeting "World"
3. If a command line argument is provided, use that as the name to greet
4. Update the test suite to test both the default case and the case with a custom name
5. Ensure the script still works when run directly (python hello.py) and when imported as a module

Example usage:
- python hello.py -> prints "Hello, World!"
- python hello.py Alice -> prints "Hello, Alice!"