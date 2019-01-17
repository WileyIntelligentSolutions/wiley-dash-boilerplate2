import sys


def slogger(origin, message):
    print('\033[94m[SLOG] \u001b[36m|  \033[1m\u001b[33m{} \u001b[0m{}'.format(origin.upper(), message))
    sys.stdout.flush()