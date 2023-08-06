`def` your CLIs.

Use `@subcommand` on any function to add a subcommand to your cli. The
function's arguments become the arguments to the subcommand. Uses argparse
behind the scenes.

```python
import defcli

@defcli.subcommand
def positional_integer(num: int):
    print(f"I like to add five: {num + 5}")

defcli.run()
```

```
$ python3 main.py positional_integer 7
I like to add five: 12
```

Or use named arguments.

```python
import defcli

@defcli.subcommand
def named_string(*, name):
    print(f"Hello, {name}!")

defcli.run()
```

```
$ python3 main.py named_string --name Fred
Hello, Fred!
```

Named booleans are automatically converted to flags.

```python
import defcli

@defcli.subcommand
def named_bool(has_something=False):
    if has_something:
        print("Got it!")
    else:
        print("We're empty-handed")

# Pass arguments to defcli.run instead of parsing sys.argv
defcli.run(["named_bool", "--has_something"])
```

```
$ python3 main.py
Got it!
```

## Future
 - [ ] Allow `@subcommand` to take a parameter to allow the same program to
       define multiple CLI's.
 - [ ] Fix bugs (there are many...)
