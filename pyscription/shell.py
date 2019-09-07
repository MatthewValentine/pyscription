from __future__ import (
    absolute_import, division, print_function, with_statement,
)

import os, shlex, subprocess, sys

from . import config, log, util

def cd(directory=None):
    os.chdir(os.path.expanduser(directory) if directory is not None else config.paths.home)

def cd_to_script_directory():
    os.chdir(config.paths.script_dir)

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
    env=None,
):
    display_stderr = util.default(display_stderr, display)
    display_command = util.default(display_command, display)

    cmd = parse_command(cmd)
    if display_command:
        log.shell_command(util.list2cmdline(cmd))

    output = subprocess.check_output(
        cmd,
        stderr=subprocess.STDOUT if include_stderr
            else log.streams.stderr if display_stderr
            else log.streams.devnull,
        env=dict(os.environ, **{k: str(v) for k, v in env.items()}) if env else None,
    )

    if display:
        log.simple(output)

    return output

def call(cmd, interactive=True, display=True, display_stderr=None, display_command=None, env=None):
    interactive = util.default(interactive, display)
    display_stderr = util.default(display_stderr, display)
    display_command = util.default(display_command, display)

    cmd = parse_command(cmd)
    if display_command:
        log.shell_command(util.list2cmdline(cmd))

    return subprocess.check_call(
        cmd,
        stdin=log.streams.stdin if interactive
            else log.streams.devnull,
        stdout=log.streams.stdout if display
            else log.streams.devnull,
        stderr=log.streams.stderr if display_stderr
            else log.streams.devnull,
        env=dict(os.environ, **{k: str(v) for k, v in env.items()}) if env else None,
    )

def unchecked_call(cmd, interactive=True, display=True, display_stderr=None, display_command=None, env=None):
    interactive = util.default(interactive, display)
    display_stderr = util.default(display_stderr, display)
    display_command = util.default(display_command, display)

    cmd = parse_command(cmd)
    if display_command:
        log.shell_command(util.list2cmdline(cmd))

    return subprocess.call(
        cmd,
        stdin=log.streams.stdin if interactive
            else log.streams.devnull,
        stdout=log.streams.stdout if display
            else log.streams.devnull,
        stderr=log.streams.stderr if display_stderr
            else log.streams.devnull,
        env=dict(os.environ, **{k: str(v) for k, v in env.items()}) if env else None,
    )
