from __future__ import (
    absolute_import, division, print_function, with_statement,
)

import os, sys

from . import fmt, util

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
