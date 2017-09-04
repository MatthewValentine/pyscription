from __future__ import (
    absolute_import, division, print_function, with_statement,
)

import os, sys

from . import fmt, util

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

class Personalize(object):
    def __init__(self):
        user = paths.username
        if not user.startswith('__') and hasattr(self, user):
            getattr(self, user)()

class paths(util.Namespace):
    home_dir = os.path.expanduser('~')
    username = os.path.basename(home_dir)
    script_dir = util.get_script_dir()
    original_working_dir = os.getcwd()

class log(util.Namespace):
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
        log.write(*args, style=styles.info, **kwargs)

    def error(*args, **kwargs):
        log.write(*args, style=styles.error, error=True, **kwargs)

    def warn(*args, **kwargs):
        log.write(*args, style=styles.warning, error=True, **kwargs)

    def shell_command(*args, **kwargs):
        log.write(*args, style=styles.shell_command, trim=False, **kwargs)

class actions(util.Namespace):
    def prompt(*args, **kwargs):
        one_char = kwargs.pop('one_char', False)
        if one_char:
            log.write(*args, style=styles.one_char_prompt, **kwargs)
            return util.getch()
        else:
            log.write(*args, style=styles.prompt, **kwargs)
            return util.input()

class streams(util.Namespace):
    stdin = sys.stdin
    stdout = sys.stdout
    stderr = sys.stderr
    devnull = open(os.devnull, 'r+b')

class styles(util.Namespace):
    info = util.compose(
        fmt.prefix('  Info  \n', fmt.fill, fmt.blue),
        fmt.blue,
    )
    warning = util.compose(
        fmt.prefix('  Warning  \n', fmt.fill, fmt.yellow),
        fmt.yellow,
    )
    error = util.compose(
        fmt.prefix('  Error  \n', fmt.fill, fmt.red),
        fmt.red,
    )
    shell_command = util.compose(
        fmt.prefix('$ ', fmt.purple),
        fmt.purple,
    )
    prompt = util.compose(
        fmt.prefix('  Prompt  \n', fmt.fill, fmt.cyan),
        fmt.suffix('>>> ', fmt.cyan),
        fmt.cyan,
    )
    one_char_prompt = prompt
