from __future__ import (
    absolute_import, division, print_function, with_statement,
)

import argparse, functools, inspect

_command_counter = 0

def run(main):
    main()

class Command(object):
    def __init__(self, superparser=None, used_short=None):
        global _command_counter
        _command_counter += 1

        name = self.__class__.__name__
        desc = inspect.getdoc(self)
        if superparser is not None:
            parser = superparser.add_parser(name, description=desc)
        else:
            parser = argparse.ArgumentParser(description=desc)
            used_short = {'h'}

        self._key = '__subcommand_' + str(_command_counter)
        subparser = parser.add_subparsers(dest=self._key)
        try:
            # Bug in Python 3 makes subparsers optional
            subparser.required = True
        except:
            pass

        self._handlers = {}
        for attr in sorted(dir(self)):
            if attr.startswith('_'):
                continue

            self._handlers[attr] = getattr(self, attr)(subparser, used_short)

        if superparser is None:
            self(parser.parse_args())

    def __call__(self, parsed_args):
        subcommand = getattr(parsed_args, self._key)
        self._handlers[subcommand](parsed_args)

def command(fn):
    try:
        spec = inspect.getfullargspec(fn)
        kwonly, kwdefault = spec.kwonlyargs or [], spec.kwonlydefaults or {}
    except AttributeError:
        spec = inspect.getargspec(fn)
        kwonly, kwdefault = [], {}

    args, defaults = spec.args or [], spec.defaults or []

    n_without_defaults = len(args) - len(defaults)
    without_defaults, with_defaults = args[:n_without_defaults], args[n_without_defaults:]

    name = fn.__name__
    desc = inspect.getdoc(fn)

    @functools.wraps(fn)
    def wrapper(self=None, superparser=None, used_short=None):
        if superparser is not None:
            parser = superparser.add_parser(name, description=desc)
        else:
            parser = argparse.ArgumentParser(description=desc)
            used_short = {'h'}

        def shorten(arg):
            for char in (arg[0].lower(), arg[0].upper()):
                if char not in used_short:
                    used_short.add(char)
                    return char
            return None

        for arg in without_defaults:
            parser.add_argument(arg)

        if spec.varargs:
            parser.add_argument(spec.varargs, nargs='*')

        def add_arg_with_default(arg, default):
            variants = ['--{}'.format(arg)]
            short = shorten(arg)
            if short is not None:
                variants.insert(0, '-{}'.format(short))

            if isinstance(default, bool):
                no_variant = '--no-{}'.format(arg)
                help_message = 'default: yes' if default else 'default: no'

                group = parser.add_mutually_exclusive_group()
                group.add_argument(
                    *variants, dest=arg, action='store_const', const=True, default=default,
                    help=help_message
                )
                group.add_argument(
                    no_variant, dest=arg, action='store_const', const=False, default=default
                )
            elif isinstance(default, int):
                parser.add_argument(
                    *variants, type=int, default=default,
                    help='default: {!r}'.format(default)
                )
            elif isinstance(default, float):
                parser.add_argument(
                    *variants, type=float, default=default,
                    help='default: {!r}'.format(default)
                )
            elif not default:
                parser.add_argument(*variants, default=default)
            else:
                parser.add_argument(
                    *variants, default=default,
                    help='default: {!r}'.format(default)
                )

        for (arg, default) in zip(with_defaults, defaults):
            add_arg_with_default(arg, default)

        for kw in kwonly:
            add_arg_with_default(kw, kwdefault[kw])

        def run(parsed_args):
            positional = []
            for arg in args:
                positional.append(getattr(parsed_args, arg))
            if spec.varargs:
                positional.extend(getattr(parsed_args, spec.varargs) or ())

            keyword = {}
            for arg in kwonly:
                keyword[arg] = getattr(parsed_args, arg)

            fn(*positional, **keyword)

        if superparser is None:
            run(parser.parse_args())
        else:
            return run

    return wrapper
