from __future__ import (
    absolute_import, division, print_function, with_statement,
)

import os, sys

from . import config, fmt, util

class streams(util.Namespace):
    stdin = sys.stdin
    stdout = sys.stdout
    stderr = sys.stderr
    devnull = open(os.devnull, 'r+b')

def simple(*args, **kwargs):
    print(*args, file=streams.stdout, **kwargs)

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
    valid = kwargs.pop('valid', lambda response: True)

    while True:
        if one_char:
            write(*args, style=config.styles.one_char_prompt, **kwargs)
            response = util.getch()
            simple()
        else:
            write(*args, style=config.styles.prompt, **kwargs)
            response = util.input()

        if valid(response):
            break
        else:
            error('{!r} is not a valid response.'.format(response))

    return response

def exit(*args, **kwargs):
    code = kwargs.pop('code', 1)
    if args or kwargs:
        error(*args, **kwargs)
    sys.exit(code)
