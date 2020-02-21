import platform
import sys


def print(*args):
    msg = ''
    for d in args:
        msg += str(d)

    if (platform.system().__eq__("Windows")):
        msg += "\n"
    else:
        msg += "\r\n"

    msg += " "*8191
    sys.stdout.write(msg)