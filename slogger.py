import sys

# This is a very simple function for logging messages in a Terminal in near-realtime from a web application

def slogger(origin, message):
    """Log a message in the Terminal

    Args:
        str: The origin of the message, e.g. the name of a function
        str: The message itself, e.g. 'Query the database'
    Returns:
        None
    """
    print('\033[94m[SLOG] \u001b[36m|  \033[1m\u001b[33m{} \u001b[0m{}'.format(origin.upper(), message))
    sys.stdout.flush()