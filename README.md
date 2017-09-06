# pyscription

Utilities to make replacing shell scripts with Python as easy as it should be.
Python 2/3 compatible, no dependencies outside standard lib.

## Survey

A non-exhaustive list of some of the more useful features

### Easy command line arguments

One line to generate basic command line interfaces from Python functions. Nothing super fancy, just easy.

```python
@util.command
def main(x, y, zebra='something', monkey=True, rabbit=False):
    '''
    A docstring am I
    '''
    pass
```

```shell
$ ./my_script.py -h
usage: my_script.py [-h] [--zebra ZEBRA] [--monkey | --no-monkey]
                    [--rabbit | --no-rabbit]
                    x y

A docstring am I

positional arguments:
  x
  y

optional arguments:
  -h, --help            show this help message and exit
  --zebra ZEBRA, -z ZEBRA
                        Defaults to 'something'
  --monkey, -m          (default yes)
  --no-monkey
  --rabbit, -r          (default no)
  --no-rabbit
```

### Simple but handy utils

Set the working directory to be where your script lives

```python
util.cd_to_script_directory()
```

Read a single character off input without waiting for enter

```python
util.getch()
```

Get Python `print` output as a string

```python
util.print_to_string(1, 'squid', sep='&', end='nugget')
# '1&squidnugget'
```

Compose some functions, if you'd like

```python
util.compose(lambda x: x*6, lambda x: x+1)(5)
# 36
```

### Thin shell command wrappers

Very slightly more convenient than `subprocess`, but still safe (not using `shell=True`.)

```python
shell.call('rm -rf /', display=False)
# vs.
devnull = open(os.devnull, 'r+b')
subprocess.check_call(['rm', '-rf', '/'], stdout=devnull, stderr=devnull)
```

### Formatted logging and prompting

Some nice default styles. (subjective)
Easily customizable, since it's just Python.
Comes with a bunch of the terminal color & style escape codes.

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

More functionality is of course available.
