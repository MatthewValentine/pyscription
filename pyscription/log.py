from __future__ import (
    absolute_import, division, print_function, with_statement,
)

import sys

from . import config, fmt, util

class streams(util.Namespace):
    stdin = sys.stdin
    stdout = sys.stdout
    stderr = sys.stderr
    devnull = open(os.devnull, 'r+b')

def simple(*args, **kwargs):
    print(*args, **kwargs)

def write(*args, **kwargs):
    style = kwargs.pop('style', fmt.none)
    trim = kwargs.pop('trim', True)
    error = kwargs.pop('error', False)

    stream = streams.stdout if not error else streams.stderr

    message = util.print_to_string(*args, **kwargs)
    if trim: message = fmt.trim(message) + kwargs.get('end', '\n')
    print(style(message), file=stream, end='')
    if hasattr(stream, 'flush'):
        stream.flush()

def info(*args, **kwargs):
    write(*args, style=config.styles.info, **kwargs)

def error(*args, **kwargs):
    write(*args, style=config.styles.error, error=True, **kwargs)

def warn(*args, **kwargs):
    write(*args, style=config.styles.warning, error=True, **kwargs)

def shell_command(*args, **kwargs):
    write(*args, style=config.styles.shell_command, trim=False, **kwargs)

def prompt(*args, **kwargs):
    one_char = kwargs.pop('one_char', False)
    if one_char:
        write(*args, style=config.styles.one_char_prompt, **kwargs)
        return util.getch()
    else:
        write(*args, style=config.styles.prompt, **kwargs)
        return util.input()

def exit(*args, code=1, **kwargs):
    if args or kwargs:
        error(*args, **kwargs)
    sys.exit(code)
