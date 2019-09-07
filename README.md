# pyscription

Make Python commandline scripts as easy as they should be.
Python 2/3 compatible, no dependencies outside standard lib.

## Survey

A list of some of the more useful features.

### Easy command line arguments

One line to generate basic command line interfaces from Python functions.

```python
@run
@command
def main(x, y, zebra='something', monkey=True, rabbit=False):
    '''
    A docstring am I
    '''
    pass
```

```shell
$ ./my_script.py -h
usage: my_script.py [-h] [-z ZEBRA] [-m | --no-monkey] [-r | --no-rabbit] x y

A docstring am I

positional arguments:
  x
  y

optional arguments:
  -h, --help            show this help message and exit
  -z ZEBRA, --zebra ZEBRA
                        default: 'something'
  -m, --monkey          default: yes
  --no-monkey
  -r, --rabbit          default: no
  --no-rabbit
```

Even subcommands are easy (like `git fetch`, `git push`, etc.)

```python
@run
class git(Command):
    @command
    def add(*files):
        ...

    @command
    def pull(remote='origin/master'):
        ...

    class turtles(Command):
        class all(Command):
            @command
            def the(way='down'):
                ...
```

### Thin shell command wrappers

Slightly more convenient than `subprocess`, but still safe (not using `shell=True`.)

```python
shell.call('rm -rf /', display=False)
# vs.
devnull = open(os.devnull, 'r+b')
subprocess.check_call(['rm', '-rf', '/'], stdout=devnull, stderr=devnull)
```

Some little conveniences, like setting the working directory to be where your script lives.

```python
shell.cd_to_script_directory()
```

### Formatted logging and prompting

Basic output and interactive prompts.

```python
log.error('Something went terribly wrong', 6, 'times !')
log.prompt('Continue? [y/n]', one_char=True)
```

Easily customize logging format. As complex as you like - not templates, just Python!

```python
def boxed(s):
    lines = [''] + s.splitlines() + ['']
    width = max(map(len, lines))
    lines = [line + ' '*(width-len(line)) for line in lines]
    lines = ['| ' + line + ' |' for line in lines]
    bar = '='*len(lines[0])
    return '\n'.join([bar]+lines+[bar])

config.styles.warning = util.compose(
    fmt.purple,
    fmt.fill,
    boxed)

log.warn('''
    Why, hello there,
        world.
''')
# (in black text with purple background)
# =====================
# |                   |
# | Why, hello there, |
# |     world.        |
# |                   |
# =====================
```

### AWK-like text processing

A very small module to implement AWK-like condition-action processing,
except you can leverage the full power of Python.

```python
awk.Program(
    awk.Rule(
        awk.BEGIN,
        lambda ctx: print(r'\begin{pmatrix}', file=ctx.out_stream)),
    awk.Rule(
        awk.END,
        lambda ctx: print(r'\end{pmatrix}', file=ctx.out_stream)),
    awk.Rule(
        lambda line: line.strip() != '',
        lambda ctx: print(
            ' & '.join(ctx.line.split())+r' \\',
            file=ctx.out_stream))
).process('''

1 2 3

4 5 6

''')
# \begin{pmatrix}
# 1 & 2 & 3 \\
# 4 & 5 & 6 \\
# \end{pmatrix}
```

You also get the return value of the condition function,
very useful for regular expressions.

```python
awk.Program(
    awk.Rule(
        re.compile('= ([0-9]+)').search,
        lambda ctx: print(ctx.condition.group(1), file=ctx.out_stream))
).process('''
nothing here
a number 1 and a var x = 2
2 + 2 = 5
''')
# 2
# 5
```
