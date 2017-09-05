from __future__ import (
    absolute_import, division, print_function, with_statement,
)

from . import util

class Program(object):
    def __init__(self, *rules):
        self.rules = rules

    def process(self, text):
        result = util.StringIO()
        self.process_stream(util.StringIO(text), result)
        return result.getvalue()

    def process_stream(self, in_stream, out_stream):
        for ctx in Context.contexts_from_streams(in_stream, out_stream):
            for rule in self.rules:
                new_ctx = rule(ctx)
                if new_ctx is not None:
                    ctx = new_ctx

class Context(object):
    @classmethod
    def contexts_from_streams(cls, in_stream, out_stream):
        yield Context(begin=True, out_stream=out_stream)
        for line in in_stream:
            yield Context(line=line, out_stream=out_stream)
        yield Context(end=True, out_stream=out_stream)

    def __init__(self, out_stream, line=None, begin=False, end=False, condition=None):
        self.out_stream = out_stream
        self.line = line
        self.begin = begin
        self.end = end
        self.condition = condition

    def __repr__(self):
        return 'Context(line={line!r}, condition={condition!r}, begin={begin!r}, end={end!r}, out_stream={out_stream!r})'.format(**vars(self))

    def print(self, text):
        self.out_stream.write(text)
    write = print

def print(ctx):
    ctx.print(ctx.line)
write = print

match_anything = lambda line: True

# BEGIN and END are special values matched by identity ('is'), so they must be separate objects.
# They don't match lines in any normal conditions, so they always return False.
BEGIN = lambda line: False
END = lambda line: False

class Rule(object):
    def __init__(self, condition=match_anything, action=print):
        self.condition = condition
        self.action = action

    def __call__(self, ctx):
        cond = False
        if ctx.begin and self.condition is BEGIN:
            cond = True
        elif ctx.end and self.condition is END:
            cond = True
        elif ctx.line is not None:
            cond = self.condition(ctx.line)

        if not cond:
            return

        ctx.condition = cond
        new_line = self.action(ctx)
        if new_line is not None:
            ctx.line = new_line

        return ctx
