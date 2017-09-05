from __future__ import (
    absolute_import, division, print_function, with_statement,
)

import os, shlex, subprocess, sys

from . import config, util

DEVNULL = open(os.devnull, 'r+b')

def parse_command(cmd):
    if isinstance(cmd, util.string_types):
        return shlex.split(cmd)
    else:
        return cmd

def output(
    cmd,
    include_stderr=False,
    display=False,
    display_stderr=None,
    display_command=None,
):
    display_stderr = util.default(display_stderr, display)
    display_command = util.default(display_command, display)

    cmd = parse_command(cmd)
    if display_command:
        config.log.shell_command(util.list2cmdline(cmd))

    output = subprocess.check_output(
        cmd,
        stderr=subprocess.STDOUT if include_stderr
            else config.streams.stderr if display_stderr
            else config.streams.devnull,
    )

    if display:
        config.log.simple(output)

    return output

def call(cmd, interactive=True, display=True, display_stderr=None, display_command=None):
    interactive = util.default(interactive, display)
    display_stderr = util.default(display_stderr, display)
    display_command = util.default(display_command, display)

    cmd = parse_command(cmd)
    if display_command:
        config.log.shell_command(util.list2cmdline(cmd))

    return subprocess.check_call(
        cmd,
        stdin=config.streams.stdin if interactive
            else config.streams.devnull,
        stdout=config.streams.stdout if display
            else config.streams.devnull,
        stderr=config.streams.stderr if display_stderr
            else config.streams.devnull,
    )

def unchecked_call(cmd, interactive=True, display=True, display_stderr=None, display_command=None):
    interactive = util.default(interactive, display)
    display_stderr = util.default(display_stderr, display)
    display_command = util.default(display_command, display)

    cmd = parse_command(cmd)
    if display_command:
        config.log.shell_command(util.list2cmdline(cmd))

    return subprocess.call(
        cmd,
        stdin=config.streams.stdin if interactive
            else config.streams.devnull,
        stdout=config.streams.stdout if display
            else config.streams.devnull,
        stderr=config.streams.stderr if display_stderr
            else config.streams.devnull,
    )
