from __future__ import (
    absolute_import, division, print_function, with_statement,
)

import os, subprocess, sys

PY3 = (sys.version_info >= (3,))
PY2 = not PY3

if PY3:
    string_types = (str,)
    from io import StringIO
    input = input
else:
    string_types = (basestring,)
    from StringIO import StringIO
    input = raw_input

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    class NamespaceMeta(type):
        def __new__(meta, name, bases, dct):
            return super(NamespaceMeta, meta).__new__(
                meta, name, bases, {k: staticmethod(v) for k, v in dct.items()},
            )
        def __setattr__(cls, key, value):
            super(NamespaceMeta, cls).__setattr__(key, staticmethod(value))

    class Namespace(object):
        __metaclass__ = NamespaceMeta

def identity(x): return x

def default(current_value, default_value):
    return current_value if current_value is not None else default_value

def print_to_string(*args, **kwargs):
    s = StringIO()
    print(*args, file=s, **kwargs)
    return s.getvalue()

def compose(*fns):
    if not fns:
        return identity

    fns = list(reversed(fns))
    def composed(*args, **kwargs):
        iterator = iter(fns)
        val = next(iterator)(*args, **kwargs)
        for fn in iterator:
            val = fn(val)
        return val

    return composed

try:
    from subprocess import list2cmdline
except ImportError:
    def list2cmdline(seq):
        result = []
        needquote = False
        for arg in seq:
            bs_buf = []

            # Add a space to separate this argument from the others
            if result:
                result.append(' ')

            needquote = (" " in arg) or ("\t" in arg) or not arg
            if needquote:
                result.append('"')

            for c in arg:
                if c == '\\':
                    # Don't know if we need to double yet.
                    bs_buf.append(c)
                elif c == '"':
                    # Double backslashes.
                    result.append('\\' * len(bs_buf)*2)
                    bs_buf = []
                    result.append('\\"')
                else:
                    # Normal char
                    if bs_buf:
                        result.extend(bs_buf)
                        bs_buf = []
                    result.append(c)

            # Add remaining backslashes, if any.
            if bs_buf:
                result.extend(bs_buf)

            if needquote:
                result.extend(bs_buf)
                result.append('"')

        return ''.join(result)

# Modified from StackOverflow user jfs
# https://stackoverflow.com/questions/3718657/how-to-properly-determine-current-script-directory-in-python/22881871#22881871
def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        #path = inspect.getabsfile(get_script_dir)
        path = os.path.abspath(sys.argv[0])
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

# From StackOverflow user Louis
# https://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch

getch = _find_getch()
